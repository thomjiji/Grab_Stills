import argparse
import os

from pybmd import Bmd
from pybmd.toolkits import add_subfolders

from utility.pattern import *
from utility.dtg_path_generator import DTG_Path
from utility.reel_importer import Reel_Importer

def source_import(DID:str):
    if DID_REGEX.match(DID) is None:
        print(f'Not a Valid DID: {DID}')
        exit()
    dtg_path=DTG_Path(DID_8=DID,volume_name='RAID6_070201',volume_type='RAID')

    
    reel_list=[f for f in os.scandir(dtg_path.get_source_path()) if f.is_dir()]
    reel_clip_path_list=[Reel_Importer(f).get_source_clip_path() for f in reel_list]
    LOCAL_RESOLVE=Bmd()
    LOCAL_FUSION=LOCAL_RESOLVE.fusion()
    
    project_manager=LOCAL_RESOLVE.get_project_manager()
    current_project=project_manager.get_current_project()
    current_media_pool=current_project.get_media_pool()
    
    current_media_pool.set_current_folder(current_media_pool.get_root_folder())
    add_subfolders(current_media_pool,current_media_pool.get_root_folder(),f'{DID}/Source/')
    
    current_media_pool.import_media(reel_clip_path_list)
    
    
    
    

if __name__ == "__main__":
    paser=argparse.ArgumentParser("import source to davinci resolve for 80220702")
    paser.add_argument('-d',required=True,help='DID for import')
    args=paser.parse_args()
    
    DID=args.d
    source_import(DID)