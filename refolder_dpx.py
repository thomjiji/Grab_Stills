import os
from utility.pattern import *

DPX_PATH="/Volumes/DTG_SSD_8TR0/802302_Still_Project/DAY_004_20230317/DPX"
ALEXA_35_CLIP_REGEX=re.compile(r'[A-Z][A-Z_][0-9]{4}C[0-9]{3}_[0-9]{6}_[0-9]{6}_(?:a|p)[A-Z0-9]{4}')

def refolder_dpx(dpx_path):
    for f in os.scandir(dpx_path):
        if f.name == '.DS_Store':
            continue
        file_name,file_ext=os.path.splitext(f.name)

        try:
            dpx_file_folder=os.path.join(dpx_path,file_name)
            os.mkdir(dpx_file_folder)
        except Exception as e:
            raise e

        new_file_name=ALEXA_35_CLIP_REGEX.match(file_name)[0]
        new_file_full_name=new_file_name+file_ext
        os.rename(f.path,os.path.join(dpx_file_folder,new_file_full_name))

for dpx_scene_dir_path in os.scandir(DPX_PATH):
    if dpx_scene_dir_path.is_dir():
        refolder_dpx(dpx_scene_dir_path.path)


