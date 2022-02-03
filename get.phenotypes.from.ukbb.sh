#!/bin/bash
#SBATCH --cpus-per-task=1
#SBATCH --time=72:00:00
#SBATCH --output=logs/get.phenotypes.from.ukbb.stdout.txt
#SBATCH --error=logs/get.phenotypes.from.ukbb.stderr.txt

echo 'START'
#make sure we are in the right folder
#cd /home/control/data/users/adam/ukbb_extract_ids_by_phenotype
#
#source ~/apps/pkg/anaconda3/etc/profile.d/conda.sh
#conda activate adams

#we make sure to send the output - which is sensitive data! - to a directory not inside the git commit
python3 -u get.phenotype.from.ukbb.tables.py \
    -F '40002 41270 41202 41204 41201 40006 40001' \
    -uc F20 \
    -uf /home/control/data/UKBB_July_2021_version/Subsetted_phenotype_fields/Longitudinal_medical_history_UKBB_July_2021_Freeze.txt \
    -o output/scz.pheno.subset.tsv \
    --all

python3 -u get.phenotype.from.ukbb.tables.py \
    -F '40002 41270 41202 41204 41201 40006 40001' \
    -uc F25 \
    -uf /home/control/data/UKBB_July_2021_version/Subsetted_phenotype_fields/Longitudinal_medical_history_UKBB_July_2021_Freeze.txt \
    -o output/affective.pheno.subset.tsv

python3 -u get.phenotype.from.ukbb.tables.py \
    -F '40002 41270 41202 41204 41201 40006 40001' \
    -uc F31 \
    -uf /home/control/data/UKBB_July_2021_version/Subsetted_phenotype_fields/Longitudinal_medical_history_UKBB_July_2021_Freeze.txt \
    -o output/bip.pheno.subset.tsv

echo 'DONE'
