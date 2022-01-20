#!/bin/bash
#SBATCH --cpus-per-task=1
#SBATCH --time=72:00:00
#SBATCH --output=logs/test.different.inputs.stdout.txt
#SBATCH --error=logs/test.different.inputs.stderr.txt

echo 'START'
#make sure we are in the right folder
cd /home/control/data/users/adam/ukbb_extract_ids_by_phenotype

source ~/apps/pkg/anaconda3/etc/profile.d/conda.sh
conda activate adams

python -u get.phenotype.from.ukbb.tables.py \
    -F '40002 41270 41202 41204 41201 40006 40001' \
    -uc F20 \
    -uf sensitive_data/10k.with.char.mental.health.txt \
    -o output/scz.test.subset.tsv \
    -all

python -u get.phenotype.from.ukbb.tables.py \
    -F '40002 41270 41202 41204 41201 40006 40001' \
    -uc F25 \
    -uf sensitive_data/10k.with.char.mental.health.txt \
    -o output/affective.test.subset.tsv \
    -all

python -u get.phenotype.from.ukbb.tables.py \
    -F '40002 41270 41202 41204 41201 40006 40001' \
    -uc F31 \
    -uf sensitive_data/10k.with.char.mental.health.txt \
    -o output/bip.test.subset.tsv \
    -all

python -u get.phenotype.from.ukbb.tables.py \
    -F '40002-0.1' \
    -uc F20 \
    -uf sensitive_data/10k.with.char.mental.health.txt \
    -o output/quick.test.specific.col.tsv

python -u get.phenotype.from.ukbb.tables.py \
    -F '40002' \
    -uc F20 \
    -uf sensitive_data/10k.with.char.mental.health.txt \
    -o output/quick.test.all.tsv \
    -all

python -u get.phenotype.from.ukbb.tables.py \
    -F '40002-0.1' \
    -uc F20 \
    -uf sensitive_data/10k.with.char.mental.health.txt \
    -o output/quick.test.tsv
