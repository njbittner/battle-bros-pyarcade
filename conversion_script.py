import sys
import glob
import os

def run(cmd):
    print(cmd)
    os.system(cmd)

def make_backup(root_folder):
    run(f"cp -R {root_folder} {root_folder}_bakup")


if __name__ == "__main__":
    root = sys.argv[1]
    make_backup(root)
    print(root)
    files = sorted(glob.glob(root + '/*.png'))
    print(len(files))
    bite = 6
    n_folders = len(files)//bite
    cur_idx = 0
    for folder_idx in range(n_folders):
        folder_name = root + f"/{folder_idx:03}"
        run("mkdir " + folder_name)
        for file in files[cur_idx: cur_idx+bite]:
            run(f"mv {file} {folder_name}")
        cur_idx = cur_idx+bite

