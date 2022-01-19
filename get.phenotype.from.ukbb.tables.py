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

TODO
- DONE make inputs sys.arg inputs from script call
- DONE option to print to stdout
- DONE (kinda, but it doesn't flush properly and I don't know why) print to stderr not stdout
- DONE x`make output filename a sys.arg input
- test with other files and codes
'''

import pandas as pd
import sys
import argparse

#useful function to print to stderr
#thanks to: https://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

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
args = parser.parse_args()

#list of fields to include
fields_of_interest = ['eid'] + args.fields.split(' ')
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

#debug prints of variables
eprint('Inputs are:')
eprint('fields_of_interest:', fields_of_interest)
eprint('code:', code)
eprint('ukb_pheno_file:', ukb_pheno_file)
eprint('print_to_stdout:', print_to_stdout)

#need to identify what columns to use by index
with open(ukb_pheno_file, 'r') as ukbb_pheno:
    #read in header
    head_string = ukbb_pheno.readline()
    try:
        header = pd.Series(
        dict(zip([x+1 for x in range(len(head_string.split("\t")))],
            [any([y in x for y in fields_of_interest]) for x in head_string.split("\t")]))
        )
    except:
        eprint("your fields are not present in the header of the ukb phenotype file you provided, have you made sure you are using the right file?")
        sys.exit()

#this is the index of the columns that hold information we care about, want as a space seperate string to pass it into a bash
header_index_of_interest = list(header[header == True].index)

#all the reading steps happen inside this with clause
with open(ukb_pheno_file, 'r') as ukbb_pheno:
    #header line as list of header names, presumed to always be first line and will break if this is not the case
    header = ukbb_pheno.readline().split("\t")
    #keep only the rows we want for the header
    header = [header[x-1] for x in header_index_of_interest]
    results_list = []
    counter = 0
    eprint("processing rows:")
    for row in ukbb_pheno:
        row = row.split("\t")
        #we only want columns that are the fields we are interested in
        #minus 1 the index to get the python count from zero
        row_subset = [row[x-1] for x in header_index_of_interest]
        #this checks if the code of interest is present in the fields of interest columns
        if any([code in x for x in row_subset]) == True:
            results_list.append(row_subset)
        counter += 1
        if counter % 50000 == 0:
            eprint(counter)

#make a dict
results_dict = dict(zip(header, [[x] for x in results_list[0]]))

#this cycles through each row in results_list, coverts to dict, and then appends it to results_dict
for row in results_list[1:]:
   temp_row_dict = dict(zip(header,row))
   for key in results_dict:
       results_dict[key].append(temp_row_dict[key])

#covert results_dict to dataframe and export to tsv
filtered_table = pd.DataFrame(results_dict)
if print_to_stdout == False:
    filtered_table.to_csv(output, index=False, sep="\t")

eprint('Done, exiting')
sys.exit()
