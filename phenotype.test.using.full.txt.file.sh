#!/bin/bash
#SBATCH --cpus-per-task=1
#SBATCH --time=72:00:00
#SBATCH --output=logs/phenotype.test.stdout.txt
#SBATCH --error=logs/phenotype.test.stderr.txt

echo 'START'
#make sure we are in the right folder
cd /home/control/data/users/adam/ukbb_extract_ids_by_phenotype

source ~/apps/pkg/anaconda3/etc/profile.d/conda.sh
conda activate adams

#we make sure to send the output - which is sensitive data! - to a directory not inside the git commit
python -u get.phenotype.from.ukbb.tables.py \
    -F '40002' \
    -uc F20 \
    -uf /home/control/data/UKBB_July_2021_version/ukb47659.txt \
    -o output/F20.40002.subset.tsv

echo 'DONE'
