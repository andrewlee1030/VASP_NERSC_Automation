#! /usr/bin/env python

import sys
import os
import shutil
import subprocess
import glob
import json
import job_control as jc
import re
import numpy as np

with open('user_info.json', 'r') as f:
    info = json.load(f)

USER_name = info['user_name']

class Result(jc.DFTjob):
    def __init__(self, poscar):
        jc.DFTjob.__init__(self, poscar)
        self.result = {}
        self.check_result()
        self.completed = 0
    def check_result(self):
        print(self.path)
        print(self.conf_lst)
        for c in self.conf_lst:
            cp = os.path.join(self.path, c)
            if not os.path.exists(cp):
                return
            else:
                os.chdir(cp)
                out = subprocess.check_output(['../../check_converge.sh','../../current_running']).decode("utf-8") 
                if "True" in out:
                    os.chdir(self.global_path)
                    print("    ", c, " is converged")
                    self.result[ c ] = self.read_oszicar(cp)
                    if c == 'rlx2':
                        self.result[ 'A' ] = self.read_surf_area(cp)
                    continue
            os.chdir(self.global_path)
        return

    def read_oszicar(self, conf_path):
        """
        Read converged energy from OSZICAR
        """
        oz = os.path.join(conf_path, 'OSZICAR')
        
        with open(oz, 'r') as f:
            for line in f:
                if re.search(' F= ', line):
                    final_line = line.strip()

        v = final_line.split()[2]
        return float(v)

    def read_surf_area(self, conf_path):
        """
        Read surface area from CONTCAR
        """
        ct = os.path.join(conf_path, 'CONTCAR')
        
        with open(ct, 'r') as f:
            dat = f.readlines()[2:5]
            a1 = list(map(float, dat[0].strip().split()))
            a2 = list(map(float, dat[1].strip().split()))
            return np.linalg.norm(np.cross(a1, a2))

if __name__ == "__main__":
    poscars = glob.glob('poscars/*')
    os.system('squeue -u '+USER_name+' > current_running')
    completed = 0
    output = {}
    
    for p in poscars:
        name = '_'.join(p.split('/')[1].split('_')[1:])
        try:
            d = Result(p)
            output[ name ] = d.result
            if len(output[ name ]) == 4: 
                completed += 1
                sub_dirs = glob.glob(f'{name}/*')
                for sub_dir in sub_dirs:
                    if sub_dir not in [f'{name}/rlx',f'{name}/rlx2',f'{name}/stc',f'{name}/POSCAR']: 
                        shutil.rmtree(sub_dir)
                        print(f'    Removed {sub_dir}')
        except: print(f'    *** Error with {name} ***   ')
    with open(os.path.basename(os.getcwd())+'_result.json', 'w') as f:
        json.dump(output, f, indent=4, ensure_ascii = False)

    print('\n'+str(completed)+' finished.')

