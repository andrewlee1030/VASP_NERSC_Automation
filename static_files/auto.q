#! /bin/bash
#SBATCH -N {nodes}
#SBATCH -p {queuetype}
#SBATCH -J {name}
#SBATCH -t {walltime}
#SBATCH -C knl
#SBATCH -A {key}
#SBATCH --mail-type=ALL
#SBATCH --mail-user=andrewlee1030quest@gmail.com


cd $SLURM_SUBMIT_DIR
module load vasp/20181030-knl
export OMP_NUM_THREADS=1
mpitasks=`echo $SLURM_JOB_NUM_NODES*64|bc`
srun -n $mpitasks -c4 --cpu_bind=cores vasp_std > log 2> err

