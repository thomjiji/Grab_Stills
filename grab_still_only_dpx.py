import os
import re
import time
from os import listdir, path
import os
import re
from pybmd import Bmd
from pybmd.gallery_still_album import StillFormats
from pybmd.toolkits import *
from dftt_timecode import DfttTimecode
from utility.dtg_path_generator import DTG_Path

from utility.still_renamer import still_renamer
from utility.timeline_render import timeline_render
from utility.pattern import *

LOCAL_RESOLVE=Bmd()
LOCAL_FUSION=LOCAL_RESOLVE.fusion()

project_manager=LOCAL_RESOLVE.get_project_manager()
current_project=project_manager.get_current_project()
current_timeline=current_project.get_current_timeline()



if DID_REGEX_L.match(current_timeline.get_name()) is None:
    
    print('timeline name is not a valid DID!')
    exit()
else:
    DID=DID_REGEX_L.findall(current_timeline.get_name())[0][0]

path_generator=DTG_Path(DID,'/','Desktop')

TEMP_PATH=path_generator.get_still_temp_path()
RENDER_PATH=path_generator.get_still_path()

DPX_PATH=path.join(RENDER_PATH,"DPX")

##TEST PATH
# TEMP_PATH='/Volumes/SSD_Transfer_4T/802302_Still_Project/dpx_3_2'
# RENDER_PATH='/Volumes/SSD_Transfer_4T/802302_Still_Project/dpx_3_2'

try:
    os.makedirs(DPX_PATH)
except Exception as e:
    print(f'{DPX_PATH} exists!')

try:
    os.makedirs(RENDER_PATH)
except Exception as e:
    print(f'{RENDER_PATH} exists!')

timeline_framerate=24
resolve_version=LOCAL_RESOLVE.get_version()

#get timeline start timecode
if resolve_version[0] is 18:
    timeline_start_timecode=DfttTimecode(current_timeline.get_start_timecode(),'auto',timeline_framerate)
else:
    timeline_start_timecode=DfttTimecode('01:00:00:00','auto',timeline_framerate)


marker_list=current_timeline.get_markers()
still_list=[]

#grab stills for every marker
for marker_frameid in marker_list:
    marker_timecode:DfttTimecode=timeline_start_timecode+marker_frameid
    current_timeline.set_current_timecode(marker_timecode.timecode_output())
    # timeline_item=current_timeline.get_current_video_item()
    # pro=timeline_item.get_media_pool_item().get_clip_property()
    
    # #get frame count for the marker
    # clip_start_timecode=DfttTimecode(timeline_item.get_media_pool_item().get_clip_property('Start TC'),'auto',timeline_framerate)
    # clip_frame_count=marker_frameid-(timeline_item.get_start()-int(timeline_start_timecode.timecode_output('frame')))+int(clip_start_timecode.timecode_output('frame'))
    
    # reel_name=timeline_item.get_media_pool_item().get_clip_property('Reel Name')
    
    # reel_number=re.findall(r'(^[a-z0-9A-Z_]{6})',reel_name)[0]
    # file_name=timeline_item.get_media_pool_item().get_clip_property('File Name')
    # frames=timeline_item.get_media_pool_item().get_clip_property('Frames')
    
    
    still=current_timeline.grab_still()
    still_list.append(still)
    time.sleep(0.1)
    

current_gallery=current_project.get_gallery()
current_album=current_gallery.get_current_still_album()


#export TIFF stills

##scan tiff file path skip export if tiff file already exist
file_name_list = [os.path.splitext(f.name)[0] for f in os.scandir(
    TEMP_PATH) if f.is_file()]

for still in still_list:
    current_album.export_stills(gallery_stills= [still],folder_path= DPX_PATH,file_prefix=current_album.get_label(still),format=StillFormats.DPX)
    
        
    
#clear album
stills=current_album.get_stills()
current_album.delete_stills(stills)

#remove DRX files
remove_count=0
for f in listdir(DPX_PATH):
    if f == '.DS_Store':
        continue
    file_name=path.splitext(f)[0]
    file_extention=path.splitext(f)[1]
    #remove drx file
    if file_extention == '.drx':
        os.remove(path.join(DPX_PATH,f))
        remove_count+=1
        continue

print(f'delete {remove_count} drx files')

#import TIFF to resolve and transcode to Prores4444 single frame 

# ##TODO clean RENDER_PATH
# exist_mov_list = [f.path for f in os.scandir(
#     RENDER_PATH) if f.is_file()]
# for f in exist_mov_list:
#     os.remove(f)
    

# current_media_pool=current_project.get_media_pool()
# current_media_pool.set_current_folder(current_media_pool.add_sub_folder(current_media_pool.get_current_folder(),'TIFF'))
# ##delete temp timeline if exist
# _timeline=get_timeline(current_project,f'TEMP_{DID}')
# if bool(_timeline):
#     current_media_pool.delete_timelines([_timeline])
# render_timeline=current_media_pool.create_timeline_from_clips(f'TEMP_{DID}',current_media_pool.import_media(TEMP_PATH))
# timeline_render(project=current_project,timeline=render_timeline,render_destination=RENDER_PATH)
