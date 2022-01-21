'''
This script simply finds all the columns you want and returns them as a new tsv or straight to stdout
-all flag allows the user to select all columns that match the field code
'''

import sys
import argparse
import pandas as pd

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def input_parsing():
    '''
    Parse input flags etc return a few globals for use in next few functions
    '''
    global fields_of_interest
    global ukb_pheno_file
    global output
    global flag_for_all_columns_of_field
    global fields_of_interest_no_eid
    #parser
    parser = argparse.ArgumentParser(
        description = 'Extracts rows from UKBB phenotype files containing the right code in the right field(s)'
    )
    parser.add_argument('--field', '-F', dest = 'fields', type=str, required=True,
        help = 'Space seperated list of field numbers you are using to define your phenotype'
    )
    parser.add_argument('--ukbb_file', '-uf', dest = 'ukbb_file', type=str, required=True,
        help = 'Full path of the ukbb subsetted file to use.\ne.g: /home/control/data/UKBB_July_2021_version/Subsetted_phenotype_fields/Longitudinal_medical_history_UKBB_July_2021_Freeze.txt'
    )
    parser.add_argument('--out', '-o', dest='output', type=str, required=True, default = 'extracted.rows.from.ukbb.fields.tsv',
        help = 'output filename. Default filename used if not used. This argument is ignored if printing to stdout.'
    )
    parser.add_argument('--all_columns_of_field', '-all', dest='flag_for_all_columns_of_field', action='store_true',
        help = 'By default this script only select columns that are an exact match to your input field (e.g 40002-0.1 and NOT 40002-0.11). Include this flag to find all columns where the field code appears *including as a substring*. \n example: -all False'
    )
    args = parser.parse_args()
    #list of fields to include
    fields_of_interest = ['eid'] + args.fields.split(' ')
    fields_of_interest_no_eid = args.fields.split(' ')
    #UKBB phenotype file to include
    #make sure to include full path name!
    ukb_pheno_file = args.ukbb_file
    #output name
    output = args.output
    #flag for how to search for each column using the user inputted field codes
    flag_for_all_columns_of_field = args.flag_for_all_columns_of_field
    #debug prints
    eprint('Inputs are:')
    eprint('fields_of_interest:', fields_of_interest)
    eprint('ukb_pheno_file:', ukb_pheno_file)
    eprint('flag_for_all_columns_of_field:', flag_for_all_columns_of_field)

def select_columns():
    '''
    based on input, selects columns and pulls them, row by row, into a pandas dataframe
    '''
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
                [any([field_from_userinput in field_from_pheno for field_from_userinput in fields_of_interest]) for field_from_pheno in head_string])))
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
    eprint(header_index_of_interest)
    return header_index_of_interest, head_string

def print_columns(header_index_of_interest, head_string):
    '''
    print results to tsv (or stdout?)
    '''
    with open(ukb_pheno_file, 'r') as ukbb_pheno:
        #skip header row by iterating once
        ukbb_pheno.readline()
        #temp list for all rows, could get pretty big...
        results_list = []
        for row in ukbb_pheno:
            row = row.split("\t")
            #we only want columns that are the fields we are interested in
            #minus 1 the index to get the python count from zero
            row_subset = [row[column_index-1] for column_index in header_index_of_interest]
            results_list.append(row_subset)
        results_dict = dict(zip(head_string, [[x] for x in results_list[0]]))
        for row in results_list[1:]:
            temp_row_dict = dict(zip(head_string,row))
        #indentation error here which is now fixed
            for key in results_dict:
                results_dict[key].append(temp_row_dict[key])
    
    #covert results_dict to dataframe and export to tsv
    filtered_table = pd.DataFrame(results_dict)
    filtered_table.to_csv(output, index=False, sep="\t")

def main():
    input_parsing()
    header_index_of_interest, head_string = select_columns()
    print_columns(header_index_of_interest, head_string)

if __name__ == "__main__":
    main()
    sys.exit()
