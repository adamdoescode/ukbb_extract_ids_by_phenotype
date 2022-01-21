# ukbb_extract_ids_by_phenotype

Internally used script for efficiently extracting ukbb iids by phenotypes from UKBB phenotype files.

Should work fine with subsetted files and the full file since it is processor intensive and not memory intensive.

## Examples:

On neuromol, you can try the following example:
```
python3 -u get.phenotype.from.ukbb.tables.py \
    -F '40002 41270 41202 41204 41201 40006 40001' \
    -uc F20 \
    -uf /home/control/data/UKBB_July_2021_version/Subsetted_phenotype_fields/Longitudinal_medical_history_UKBB_July_2021_Freeze.txt \
    -o output/scz.pheno.subset.tsv \
    --all
```

You may find the script runs marginally faster if you activate a conda environment first. `conda activate adams` will activate a conda environment where this script will robustly work.

You can take a look at the test `phenotype.test.using.full.txt.file.sh` script to get an idea for several ways to run the script. **These won't work if you cloned this repository from github as the sensitive files are deliberately excluded.**


## commentary

The reason I wrote the script this way is because I can't keep the whole table in memory. Easier to iterate through in a processor intensive manner:

1. read in file as iterator
2. read in a single line
   1. format as a `dict` with column headers from line1 as keys
3. filter line for just the columns I want (need to keep eid so I know which individual I am looking at)
4. look at each column for what I want
5. if positive, extract the eid plus the columns of interest into a dict
6. when done perform QC:
   1. Check all rows have at least one positive hit for the code you want
7. convert results dict to dataframe and export to tsv

You can use the tsv for downstream applications such as filtering UKBB bgen files or performing PRS scoring etc.

Example of how to use this script to extract ICD10 code for schizophrenia (F20) from the ICD10 fields (40002 41270 41202 41204 41201 40006 40001) **on neuromol**:
```
conda activate adams

python -u scripts/get.phenotype.from.ukbb.tables.py \
    -F '40002 41270 41202 41204 41201 40006 40001' \
    -uc F20 \
    -uf /home/control/data/UKBB_July_2021_version/Subsetted_phenotype_fields/Longitudinal_medical_history_UKBB_July_2021_Freeze.txt \
    -o scz.pheno.subset.tsv
```

Output tsv will be: `scz.pheno.subset.tsv` and it will currently contain every column from the input table but with only the rows containing the right phenotype code in the right column(s)/field(s).

# companion script for pulling whole columns

Sometimes you just want all of a specifc column. This sounds easy, but it is a bit of a pain to find which column index matches your column(s). You also need to deal with not knowing how many columns match your field code. These are easily solved with a simple python script.

```
python3 -u select.specific.columns.from.ukbb.tables.py \
    -F '40002 41270 41202 41204 41201 40006 40001' \
    -uf /home/control/data/UKBB_July_2021_version/Subsetted_phenotype_fields/Longitudinal_medical_history_UKBB_July_2021_Freeze.txt \
    -o output/scz.pheno.subset.tsv \
    --all
```

