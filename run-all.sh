#!/bin/bash

for script in $(ls scripts/eyesstream_20210526T05/*.slurm)
do
   sbatch $script
done
