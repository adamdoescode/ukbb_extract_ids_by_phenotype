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

def select_columns():
    '''
    based on input, selects columns and pulls them, row by row, into a pandas dataframe
    '''
    pass

def print_columns():
    '''
    print results to tsv (or stdout?)
    '''
    pass

def main():
    input_parsing()
    select_columns()
    print_columns()

if __name__ == "__main__":
    main()
    sys.exit()
