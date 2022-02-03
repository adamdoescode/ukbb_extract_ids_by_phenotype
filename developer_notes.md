
# 19.jan.2022 things todo

After presenting this repo/script to the lab I have been given a few suggestions and possible edge cases I should consider.

- [x] Error when no rows return a result - add try/except clause
- [x] DEBUG try except clause for field names/codes
- [x] timecourse fields; should be as simple as specifying specific column eg 40002.1
  - [x] debug of issue with column selection
- [x] make sure doesn't get wrong phenotype code e.g F20 is for other things than SCZ - no way to avoid. But maybe this doesn't actually occur in the UKBB?
- [x] more difficult to avoid is cases where there is something like F200* for a different field. Oh no! Should be mostly okay, but worth checking.
- [ ] continous traits? Probably doesn't work, could set up a flag and an if statement to process these differently which should be pretty feasible but maybe not needed?
- [x] only print columns user selects in field flag cmd input - already does this, no need to edit
- [ ] refactor code into functions
- [ ] remove endline '\n' from rows, eg: '41283-0.15\n'
- [ ] maybe todo: pull row descriptions from ukb47659.html which tags with field number code thingy anyway
- [ ] FIX: wrong column headers for select.whole.columns.py script
- [ ] FIX: fields less than 6 digits pull those with 6 or more digits because I am using a simple "in" statement to test. Need to test for field followed by "-".

Quick test for `get.phenotype.from.ukbb.tables.py`:
```
python3 -u get.phenotype.from.ukbb.tables.py \
    -F '40002' \
    -uc F20 \
    -uf sensitive_data/10k.with.char.mental.health.txt \
    -o output/quick.test.all.tsv \
    -all
```

Quick test for `select.specific.columns.from.ukbb.tables.py`:
```
python3 -u select.specific.columns.from.ukbb.tables.py \
    -F '21001' \
    -uf sensitive_data/ukb47.head.txt \
    -o output/bugs.21001.ukb47head.tsv \
    --all
```

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
    -o output/quick.test.specific.col.tsv \
    -all
```
Output has only 40002-0.1 and not 40002-0.10 etc.

This now works!

# adding functions

Was a bad idea and now loads of things have broken.

Current problem:
```
python -u get.phenotype.from.ukbb.tables.py \
    -F '40002-0.1' \
    -uc F20 \
    -uf sensitive_data/10k.with.char.mental.health.txt \
    -o output/quick.test.specific.col.tsv
```
Traceback (most recent call last):
  File "get.phenotype.from.ukbb.tables.py", line 176, in <module>
    main()
  File "get.phenotype.from.ukbb.tables.py", line 173, in main
    format_and_save_output(results_list, head_string)
  File "get.phenotype.from.ukbb.tables.py", line 160, in format_and_save_output
    results_dict[key].append(temp_row_dict[key])
UnboundLocalError: local variable 'temp_row_dict' referenced before assignment
(adams) 

This turned out to be an indentation error but also an indexing error. Both now fixed.

Test for a few different fields and codes, see 

# companion script for pulling whole columns

Sometimes you just want all of a specifc column. This sounds easy, but it is a bit of a pain to find which column index matches your column(s). You also need to deal with not knowing how many columns match your field code. These are easily solved with a simple python script.

```
python3 -u select.specific.columns.from.ukbb.tables.py \
    -F '40002 40001' \
    -uf sensitive_data/10k.with.char.mental.health.txt \
    -o output/test.pull.whole.columns.tsv \
    --all
```

# FIX: wrong column headers for select.whole.columns.py script

This command pulls the wrong columns (or headers?):
```
python3 -u select.specific.columns.from.ukbb.tables.py \
    -F '40002 40001' \
    -uf /home/control/data/UKBB_July_2021_version/Subsetted_phenotype_fields/Longitudinal_medical_history_UKBB_July_2021_Freeze.txt \
    -o output/test.pull.whole.columns.tsv \
    --all
```

These column fields are present in the header. So it's not finding things that are not there.

It correctly pulls the eid column which is good.

But it then just pulls the next columns until it has enough to match with the number that match with the number of fields in `-F '40002 40001'`.

Does it do the same with the sample data?

```
python3 -u select.specific.columns.from.ukbb.tables.py \
    -F '40002 40001' \
    -uf sensitive_data/10k.with.char.mental.health.txt \
    -o output/select.wrong.output.debug.sampledata.tsv \
    --all
```

Yes. So I can safely use the sample data to troubleshoot.

I think the important variable is `header_index_of_interest`.

So printing that column returns the right indicies for the columns we want:

[1, 1453, 1454, 1455, 1456, 1457, 1458, 1459, 1460, 1461, 1462, 1463, 1464, 1465, 1466, 1467, 1468, 1469, 1470, 1471, 1472, 1473, 1474, 1475, 1476, 1477, 1478, 1479, 1480, 1481, 1482]
% head -1 sensitive_data/10k.with.char.mental.health.txt | awk '{print $1453}'
40001-0.0

I have modified a few lines in the `print_columns()` algorithm so that it outputs correctly now.

`rg 1000067 sensitive_data/10k.with.char.mental.health.txt | rg G122`

I should double check that the same is not happening in the `get.phenotype.from.ukbb.tables.py` script:

```
python3 -u get.phenotype.from.ukbb.tables.py \
    -F '40002' \
    -uc F20 \
    --all \
    -uf sensitive_data/10k.with.char.mental.health.txt \
    -o output/quick.test.specific.col.tsv
```

It seems to be working fine.

# more bugs in select.specific.columns.from.ukbb.tables.py identified by danielle

- [ ] header prints twice
- [ ] eid row does not print
- [ ] all other rows incorrect

First I should see if I can replicate these bugs:

```
python3 -u select.specific.columns.from.ukbb.tables.py \
    -F '40002 40001' \
    -uf sensitive_data/10k.with.char.mental.health.txt \
    -o output/more.bugs.debug.sampledata.tsv \
    --all
```
This produces the duplicate header column but the eid row is correct.

Try using the full phenotype file instead:
```
python3 -u select.specific.columns.from.ukbb.tables.py \
    -F '40002 40001' \
    -uf /home/control/data/UKBB_July_2021_version/ukb47659.txt \
    -o output/more.bugs.debug.sampledata.full.pheno.tsv \
    --all
```

Okay so this has all danielle's described problems.

I should make a file that contains the first 10 rows and 10 cols of ukb47659 and test that:
```
head /home/control/data/UKBB_July_2021_version/ukb47659.txt > sensitive_data/ukb47.head.txt
head /home/control/data/UKBB_July_2021_version/ukb47659.txt | awk '{print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $5 "\t" $6 "\t" $7 "\t" $8 "\t" $9 "\t" $10}' > sensitive_data/ukb47.head.first10cols.txt
python3 -u select.specific.columns.from.ukbb.tables.py \
    -F '21001' \
    -uf sensitive_data/ukb47.head.txt \
    -o output/more.bugs.debug.ukb47head.tsv \
    --all
python3 select.specific.columns.from.ukbb.tables.py \
    -F '5' \
    -uf sensitive_data/ukb47.head.first10cols.txt \
    -o output/more.bugs.debug.ukb47head.10cols.tsv \
    --all
```

For some reason the awk command is introducing new issues. Nope looks like it is an issue with the column with "5-0.0" in the header? But it looks fine...

```
head /home/control/data/UKBB_July_2021_version/ukb47659.txt | awk '{print $1 "\t" $2 "\t" $3 "\t" $4 "\t" $5 "\t" $6 "\t" $7 "\t" $8 "\t" $9 "\t" $10 "\t" $11}' > sensitive_data/ukb47.head.first11cols.txt
python3 select.specific.columns.from.ukbb.tables.py \
    -F '5' \
    -uf sensitive_data/ukb47.head.first11cols.txt \
    -o output/more.bugs.debug.ukb47head.11cols.tsv \
    --all
```

The commas are from end of line characters. We can delete them like so:
for the head string which becomes the header:
head_string = ukbb_pheno.readline().replace("\n","").split("\t")

And similarly when we open the file again for the rest of the rows.

## double header

For the double header the lines of interest are:
```
        with open(ukb_pheno_file, 'r') as ukbb_pheno:
            #skip header row by iterating once
            ukbb_pheno.readline()
```

So uncommenting `ukbb_pheno.readline()` works for the full phenotype file. But I think it will now skip a line for the longitudinal results?

Let's check:
```
python3 -u select.specific.columns.from.ukbb.tables.py \
    -F '40002' \
    -uf sensitive_data/10k.with.char.mental.health.txt \
    -o output/more.bugs.debug.sampledata.tsv \
    --all
```
And then inspect headers for same eid in first row:
```
head -2 sensitive_data/10k.with.char.mental.health.txt | awk '{print $1}'
head -2 output/more.bugs.debug.sampledata.tsv | awk '{print $1}'
head -2 sensitive_data/ukb47.head.first11cols.txt | awk '{print $1}'
head -2 output/more.bugs.debug.ukb47head.11cols.tsv | awk '{print $1}'
```
eid
1000013
eid
1000013
eid
1000013
eid
1000013

Nope, it's fine!

## short fields picking up all longer fields where it is contained as a sub-field

This is problematic for picking these shorter field names. Should be able to regex a solution.

This repos the problem without making a huge file:
```
python3 -u select.specific.columns.from.ukbb.tables.py \
    -F '2' \
    -uf sensitive_data/ukb47.head.txt \
    -o output/bugs.2.ukb47head.tsv \
    --all
```

Fixed by changing `field_from_userinput in field_from_pheno.split` to `field_from_userinput == field_from_pheno.split("-")[0]` here:
```
        if flag_for_all_columns_of_field == True:
            eprint("testing all columns of field")
            #get general matches
            header = pd.Series(dict(zip([x+1 for x in range(len(head_string))],
                [any([field_from_userinput == field_from_pheno.split("-")[0] for field_from_userinput in fields_of_interest]) for field_from_pheno in head_string])))
```

Fixed!

## eid missing issue


```
python3 -u select.specific.columns.from.ukbb.tables.py \
    -F '21001' \
    -uf sensitive_data/ukb47.head.txt \
    -o output/bugs.21001.ukb47head.tsv \
    --all
python3 -u select.specific.columns.from.ukbb.tables.py \
    -F '3' \
    -uf sensitive_data/ukb47.head.txt \
    -o output/bugs.2.ukb47head.tsv \
    --all
```

eid missing from `output/bugs.21001.ukb47head.tsv`
eid present in `output/bugs.2.ukb47head.tsv` but is in column 2?

Suggests an off-by-1 error somewhere.

Yes, it is in these lines in `print_columns()`:
```
                row_subset = [row[column_index-1].replace("\n","") for column_index in header_index_of_interest]
                results_list.append(row_subset)
            subsetted_head_string = [head_string[column_index-1] for column_index in header_index_of_interest]
```

I have removed the -1 from column index here.
