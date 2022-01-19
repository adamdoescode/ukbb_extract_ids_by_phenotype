#!/bin/bash
#SBATCH --cpus-per-task=1
#SBATCH --time=72:00:00
#SBATCH --output=logs/get.phenotypes.from.ukbb.stdout.txt
#SBATCH --error=logs/get.phenotypes.from.ukbb.stderr.txt

echo 'START'

cd /home/control/data/users/adam/prs.scz.bip2

source ~/apps/pkg/anaconda3/etc/profile.d/conda.sh
conda activate adams

python -u scripts/get.phenotype.from.ukbb.tables.py \
    -F '40002 41270 41202 41204 41201 40006 40001' \
    -uc F20 \
    -uf /home/control/data/UKBB_July_2021_version/Subsetted_phenotype_fields/Longitudinal_medical_history_UKBB_July_2021_Freeze.txt \
    -o phenotypes/scz.pheno.subset.tsv

python -u scripts/get.phenotype.from.ukbb.tables.py \
    -F '40002 41270 41202 41204 41201 40006 40001' \
    -uc F25 \
    -uf /home/control/data/UKBB_July_2021_version/Subsetted_phenotype_fields/Longitudinal_medical_history_UKBB_July_2021_Freeze.txt \
    -o phenotypes/affective.pheno.subset.tsv

python -u scripts/get.phenotype.from.ukbb.tables.py \
    -F '40002 41270 41202 41204 41201 40006 40001' \
    -uc F31 \
    -uf /home/control/data/UKBB_July_2021_version/Subsetted_phenotype_fields/Longitudinal_medical_history_UKBB_July_2021_Freeze.txt \
    -o phenotypes/bip.pheno.subset.tsv

echo 'DONE'
