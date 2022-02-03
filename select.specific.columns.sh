#!/bin/bash
#SBATCH --cpus-per-task=1
#SBATCH --time=72:00:00
#SBATCH --output=logs/get.phenotypes.from.ukbb.stdout.txt
#SBATCH --error=logs/get.phenotypes.from.ukbb.stderr.txt

echo 'START'
#make sure we are in the right folder
cd /home/control/data/users/adam/ukbb_extract_ids_by_phenotype

source ~/apps/pkg/anaconda3/etc/profile.d/conda.sh
conda activate adams

#we make sure to send the output - which is sensitive data! - to a directory not inside the git commit
python3 -u select.specific.columns.from.ukbb.tables.py \
    -F '40002 40001' \
    -uf sensitive_data/10k.with.char.mental.health.txt \
    -o output/select.wrong.output.debug.sampledata.tsv \
    --all

echo 'DONE'
