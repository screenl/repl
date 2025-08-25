#!/bin/bash
#SBATCH --job-name=prover
#SBATCH --output=/scratch/yj2638/repl/batch_logs/eval_%j.out
#SBATCH --error=/scratch/yj2638/repl/batch_logs/eval_%j.err
#SBATCH --gres=gpu
#SBATCH --cpus-per-task=8
# account=pr_117_tandon_advanced
#SBATCH --nodes=1
#SBATCH --time=08:00:00
#SBATCH --mail-user=yj2638@nyu.edu

cd /scratch/yj2638/repl

source .venv/bin/activate

python3 main_minif2f_prove.py

