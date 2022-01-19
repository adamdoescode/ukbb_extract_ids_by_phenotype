
# 19.jan.2022 things todo

After presenting this repo/script to the lab I have been given a few suggestions and possible edge cases I should consider.

- [x] Error when no rows return a result - add try/except clause
- [ ] DEBUG try except clause for field names/codes
- [ ] timecourse fields; should be as simple as specifying specific column eg 40002.1
- [ ] make sure doesn't get wrong phenotype code e.g F20 is for other things than SCZ
- [ ] more difficult to avoid is cases where there is something like F200* for a different field. Oh no! Should be mostly okay, but worth checking...
- [ ] continous traits? Probably doesn't work, could set up a flag and an if statement to process these differently which should be pretty feasible but maybe not needed?
- [ ] only print columns user selects in field flag cmd input
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






