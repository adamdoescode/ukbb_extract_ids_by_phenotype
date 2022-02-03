'''
Inputs:
fields of interest, always includes 'eid' implicitly as index column
data table of interest

The reason I do it like this is because I can't keep the whole table in memory. Easier to iterate through in a processor intensive manner

1. read in file as iterator
2. read in a single line
   1. format as a `dict` with column headers from line1 as keys
3. filter line for just the columns I want (need to keep eid so I know which individual I am looking at)
4. look at each column for what I want
5. if positive, extract the eid plus the columns of interest into a dict
6. when done perform QC:
   1. Check all rows have at least one positive hit for the code you want
7. convert results dict to dataframe and export to tsv
'''

import sys
import argparse
import pandas as pd

#useful function to print to stderr
#thanks to: https://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def input_parsing():
    global ukb_pheno_file
    global fields_of_interest
    global fields_of_interest_no_eid
    global code
    global ukb_pheno_file
    global print_to_stdout
    global flag_for_all_columns_of_field
    global output

    parser = argparse.ArgumentParser(
        description = 'Extracts rows from UKBB phenotype files containing the right code in the right field(s)'
    )
    parser.add_argument('--field', '-F', dest = 'fields', type=str, required=True,
        help = 'Space seperated list of field numbers you are using to define your phenotype'
    )
    parser.add_argument('--code', '-uc', dest = 'code', type=str, required=True,
        help = 'A single code (e.g F20) to look for in the file'
    )
    parser.add_argument('--ukbb_file', '-uf', dest = 'ukbb_file', type=str, required=True,
        help = 'Full path of the ukbb subsetted file to use.\ne.g: /home/control/data/UKBB_July_2021_version/Subsetted_phenotype_fields/Longitudinal_medical_history_UKBB_July_2021_Freeze.txt'
    )
    parser.add_argument('--stdout', '-C', dest = 'stdout', action = 'store_true', required=False,
        help = 'include this flag to print results to stdout instead of to file'
    )
    parser.add_argument('--out', '-o', dest='output', type=str, required=False, default = 'extracted.rows.from.ukbb.fields.tsv',
        help = 'output filename. Default filename used if not used. This argument is ignored if printing to stdout.'
    )
    parser.add_argument('--all_columns_of_field', '-all', dest='flag_for_all_columns_of_field', action='store_true',
        help = 'By default this script only select columns that are an exact match to your input field (e.g 40002-0.1 and NOT 40002-0.11). Include this flag to find all columns where the field code appears *including as a substring*. \n example: -all False'
    )
    args = parser.parse_args()
    #list of fields to include
    fields_of_interest = ['eid'] + args.fields.split(' ')
    fields_of_interest_no_eid = args.fields.split(' ')
    #code of interest
    code = args.code
    #UKBB phenotype file to include
    #make sure to include full path name!
    ukb_pheno_file = args.ukbb_file
    #flag for printing results to stdout
    #default is false
    print_to_stdout = args.stdout
    #output name
    output = args.output
    #flag for how to search for each column using the user inputted field codes
    flag_for_all_columns_of_field = args.flag_for_all_columns_of_field
    #debug prints of variables
    eprint('Inputs are:')
    eprint('fields_of_interest:', fields_of_interest)
    eprint('code:', code)
    eprint('ukb_pheno_file:', ukb_pheno_file)
    eprint('print_to_stdout:', print_to_stdout)
    eprint('flag_for_all_columns_of_field:', flag_for_all_columns_of_field)

def get_columns_and_find_rows():
    #need to identify what columns to use by index
    with open(ukb_pheno_file, 'r') as ukbb_pheno:
        #read in header
        head_string = ukbb_pheno.readline().split("\t")
        #test for whether any user fields are actually in the header
        flag_if_fields_valid = any([any([y in x for y in fields_of_interest_no_eid]) for x in head_string])
        eprint("Do user input fields match with any fields in phenotype file:", flag_if_fields_valid)
        if flag_if_fields_valid == False:
            eprint("ERROR: no user input fields match those in the header of the ukb phenotype file you provided, have you made sure you are using the right file?")
            sys.exit()
        #this line looks for field_from_userinput within each field_from_pheno extracted from the header.
        #then it returns true for each field that is present
        #finally, it zips this with the header string and converts to a dict
        if flag_for_all_columns_of_field == True:
            eprint("testing all columns of field")
            #get general matches
            header = pd.Series(dict(zip([x+1 for x in range(len(head_string))],
                [any([field_from_userinput == field_from_pheno.split("-")[0] for field_from_userinput in fields_of_interest]) for field_from_pheno in head_string])))
        elif flag_for_all_columns_of_field == False:
            eprint("testing specific columns only")
            #only get exact matches
            header = pd.Series(dict(zip([x+1 for x in range(len(head_string))],
                [any([field_from_userinput == field_from_pheno for field_from_userinput in fields_of_interest]) for field_from_pheno in head_string])))
        else:
            eprint("flag_for_all_columns_of_field is not set! This is an error and you should report this to A.Graham adam.graham@uon.edu.au")
            sys.exit()
        #this is the index of the columns that hold information we care about, want as a space seperate string to pass it into a bash
        header_index_of_interest = list(header[header == True].index)
    #all the reading steps happen inside this with clause
    with open(ukb_pheno_file, 'r') as ukbb_pheno:
        #keep only the rows we want for the header
        head_string = [head_string[x-1] for x in header_index_of_interest]
        results_list = []
        counter = 0
        eprint("processing rows:")
        for row in ukbb_pheno:
            row = row.split("\t")
            #we only want columns that are the fields we are interested in
            #minus 1 the index to get the python count from zero
            row_subset = [row[x-1] for x in header_index_of_interest]
            #this checks if the code of interest is present in the fields of interest columns
            #this will fail if F20 and F200 are different codes because there is no way to robustly distinguish between them
            # without being specific with user input!
            if any([code in row_code for row_code in row_subset]) == True:
                results_list.append(row_subset)
            counter += 1
            if counter % 50000 == 0:
                eprint(counter)
    return results_list, head_string

def format_and_save_output(results_list, head_string):
    #make a dict
    #requires try except for empty list
    try:
        results_dict = dict(zip(head_string, [[x] for x in results_list[0]]))
    except:
        eprint("Your code did not appear in the phenotype file! Did you use the right code and the right phenotype file?")
        sys.exit()
    
    #this cycles through each row in results_list, coverts to dict, and then appends it to results_dict
    #this breaks if there is only one row?
    for row in results_list[1:]:
        temp_row_dict = dict(zip(head_string,row))
        #indentation error here which is now fixed
        for key in results_dict:
            results_dict[key].append(temp_row_dict[key])

    #covert results_dict to dataframe and export to tsv
    filtered_table = pd.DataFrame(results_dict)
    if print_to_stdout == False:
        filtered_table.to_csv(output, index=False, sep="\t")
    else:
        #this needs fixing...
        for row in filtered_table:
            print(row)

    eprint('Done, exiting')
    sys.exit()

def main():
    input_parsing()
    results_list, head_string = get_columns_and_find_rows()
    format_and_save_output(results_list, head_string)

if __name__ == "__main__":
    main()
