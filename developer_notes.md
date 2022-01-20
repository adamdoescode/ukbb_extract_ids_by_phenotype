
# 19.jan.2022 things todo

After presenting this repo/script to the lab I have been given a few suggestions and possible edge cases I should consider.

- [x] Error when no rows return a result - add try/except clause
- [x] DEBUG try except clause for field names/codes
- [x] timecourse fields; should be as simple as specifying specific column eg 40002.1
  - [ ] debug of issue with column selection
- [ ] make sure doesn't get wrong phenotype code e.g F20 is for other things than SCZ
- [ ] more difficult to avoid is cases where there is something like F200* for a different field. Oh no! Should be mostly okay, but worth checking...
- [ ] continous traits? Probably doesn't work, could set up a flag and an if statement to process these differently which should be pretty feasible but maybe not needed?
- [x] only print columns user selects in field flag cmd input - already does this, no need to edit
- [ ] maybe todo: pull row descriptions from ukb47659.html which tags with field number code thingy anyway


#  ~~debug try except clause for field names/codes~~ Error when no rows return a result - add try/except clause

Make a truncated file for quick debugging:
```
cd /home/control/data/UKBB_July_2021_version/Subsetted_phenotype_fields
head -100000 Mental_health_UKBB_July_2021_Freeze.txt > /home/control/data/users/adam/ukbb_extract_ids_by_phenotype/sensitive_data/mental.health.first.100k.rows.txt
```
Update: This file turns out to be useless
Instead, lets try one that explicitly extracts rows with alphabetic chars in them:
`rg -N -e "[A-z]" /home/control/data/UKBB_July_2021_version/Subsetted_phenotype_fields/Longitudinal_medical_history_UKBB_July_2021_Freeze.txt | head -10000 > /home/control/data/users/adam/ukbb_extract_ids_by_phenotype/sensitive_data/10k.with.char.mental.health.txt`

Added this whole folder to `.gitignore` because it is important that I don't leak this to github by accident.

Test script basics:
```
python -u get.phenotype.from.ukbb.tables.py \
    -F '40002' \
    -uc F2 \
    -uf sensitive_data/10k.with.char.mental.health.txt \
    -o output/quick.test.tsv
```
This throws an index error:
Traceback (most recent call last):
  File "get.phenotype.from.ukbb.tables.py", line 119, in <module>
    results_dict = dict(zip(header, [[x] for x in results_list[0]]))
IndexError: list index out of range

Okay fixed with a try except clause

# DEBUG try except clause for field names/codes

## find a code that works for my debug set

Turns out the issue was that there were no codes in the first 100k rows (really?). Fixed by using ripgrep to pull rows with [A-z] instead for the phenotype file.

## DEBUG try/except

Script that triggers the try except:
```
python -u get.phenotype.from.ukbb.tables.py \
    -F 'cake' \
    -uc F2 \
    -uf sensitive_data/10k.with.char.mental.health.txt \
    -o output/quick.test.tsv
```
It did not trigger the try except clause... because 'eid' always appears! So the exception will never occur anyway.

After removing the try and except it now errors and exits with correct behaviour.

# timecourse fields

40002-0.1 is a valid column with a single F20 present
40002-1.1 is a valid column but without any F20 values
400021.1 is not a valid column.

```
python -u get.phenotype.from.ukbb.tables.py \
    -F '40002-0.1' \
    -uc F20 \
    -uf sensitive_data/10k.with.char.mental.health.txt \
    -o output/quick.test.tsv
python -u get.phenotype.from.ukbb.tables.py \
    -F '40002-1.1' \
    -uc F20 \
    -uf sensitive_data/10k.with.char.mental.health.txt \
    -o output/quick.test.tsv
python -u get.phenotype.from.ukbb.tables.py \
    -F '400021.1' \
    -uc F20 \
    -uf sensitive_data/10k.with.char.mental.health.txt \
    -o output/quick.test.tsv
```
So the first two work, with 40002-0.1 returning a file with one entry as expected. 40002-1.1 works but exits when it does not find any F20 which is as expected. 400021.1 fails when the field does not match.

This means a user could input specific colnames and they will work.

## debug of issue with column selection

However there is a problem because I am using `in` it will include longer strings where the substring is valid.
e.g for 40002-0.1 I get: `40002-0.1,40002-0.10,40002-0.11,40002-0.12,40002-0.13,40002-0.14`

So I need to not use `in` statements here...

Lets do an if statement so that we have:
```
flag_for_all_columns_of_field = BOOL
if flag == True:
    field_from_userinput.str.find(field_from_pheno)
else if flag == False:
    field_from_userinput in field_from_pheno
```

```
python -u get.phenotype.from.ukbb.tables.py \
    -F '40002' \
    -uc F20 \
    -uf sensitive_data/10k.with.char.mental.health.txt \
    -o output/quick.test.all.tsv \
    -all
```
Output has all field 40002 cols and one row corresponding to one hit.
```
python -u get.phenotype.from.ukbb.tables.py \
    -F '40002-0.1' \
    -uc F20 \
    -uf sensitive_data/10k.with.char.mental.health.txt \
    -o output/quick.test.specific.col.tsv
```
Output has only 40002-0.1 and not 40002-0.10 etc.

This now works!


