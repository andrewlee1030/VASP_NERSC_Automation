import glob
import shutil
import os

poscars = glob.glob('poscars/*')
for p in poscars:
    name = '_'.join(p.split('/')[1].split('_')[1:])
    #if len(name) != 10: continue
    sub_dirs = glob.glob(f'{name}/*')
    for dirs in  sub_dirs: 
        print(dirs)
        sub_files = glob.glob(f'{dirs}/*')
        for files in sub_files:
            if 'core' in files: os.remove(files)
