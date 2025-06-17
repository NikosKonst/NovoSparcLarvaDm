#!/bin/bash

### SBATCH OPTIONS ###
#SBATCH --partition=ipop-up
#SBATCH --job-name=Novosparc
#SBATCH --output=Novosparc-%j.out
#SBATCH --error=Novosparc-%j.err
#SBATCH --mem=200G
#SBATCH --cpus-per-task=8

### MODULES ###
module purge
source /shared/home/${USER}/.bashrc
conda activate novosparc

start0=`date +%s`
echo '########################################'
echo 'Date:' $(date --iso-8601=seconds)
echo 'User:' $USER
echo 'Host:' $HOSTNAME
echo 'Job Name:' $SLURM_JOB_NAME
echo 'Job Id:' $SLURM_JOB_ID
echo 'Directory:' $(pwd)
echo '########################################'

### check python ###
which python
python --version

### variables
INPUTFILE="Last_ATLAS"
ALPHAPARAMETER=0.3

echo "Novosparc run on $INPUTFILE.csv with alpha $ALPHAPARAMETER" 

### COMMANDS ###
python Last_Novosparc.py $INPUTFILE $ALPHAPARAMETER

echo '########################################'
echo 'Job finished' $(date --iso-8601=seconds)
end=`date +%s`
runtime=$((end-start0))
minute=60
echo "---- Total runtime $runtime s ; $((runtime/minute)) min ----"