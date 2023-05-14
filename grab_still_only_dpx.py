import os
import time
from os import listdir, path

from pybmd import Bmd
from pybmd.gallery_still_album import StillFormats
from dftt_timecode import DfttTimecode

from utility.dtg_path_generator import DTG_Path
from utility.pattern import *

LOCAL_RESOLVE = Bmd()
LOCAL_FUSION = LOCAL_RESOLVE.fusion()

project_manager = LOCAL_RESOLVE.get_project_manager()
current_project = project_manager.get_current_project()
current_timeline = current_project.get_current_timeline()

if DID_REGEX_L.match(current_timeline.get_name()) is None:
    print("Timeline name is not a valid DID!")
    exit()
else:
    DID = DID_REGEX_L.findall(current_timeline.get_name())[0][0]

path_generator = DTG_Path(DID, "/", "Desktop")

TEMP_PATH = path_generator.get_still_temp_path()
RENDER_PATH = path_generator.get_still_path()
DPX_PATH = path.join(RENDER_PATH, "DPX")

try:
    os.makedirs(DPX_PATH)
except FileExistsError as e:
    print(f"{DPX_PATH} exists!")

try:
    os.makedirs(RENDER_PATH)
except FileExistsError as e:
    print(f"{RENDER_PATH} exists!")

timeline_framerate = 24
resolve_version = LOCAL_RESOLVE.get_version()

# get timeline start timecode
if resolve_version[0] == 18:
    timeline_start_timecode = DfttTimecode(
        current_timeline.get_start_timecode(), "auto", timeline_framerate
    )
else:
    timeline_start_timecode = DfttTimecode(
        "01:00:00:00", "auto", timeline_framerate
    )

marker_list = current_timeline.get_markers()
still_dict = {}
scene_set = set()

# grab stills for every marker
for marker_frameId in marker_list:
    marker_timecode: DfttTimecode = timeline_start_timecode + marker_frameId
    current_timeline.set_current_timecode(marker_timecode.timecode_output())
    timeline_item = current_timeline.get_current_video_item()
    scene = timeline_item.get_media_pool_item().get_metadata("Scene")
    if scene not in scene_set:
        scene_set.add(scene)
    still = current_timeline.grab_still()
    still_dict.update({still: scene})
    time.sleep(0.3)

current_gallery = current_project.get_gallery()
current_album = current_gallery.get_current_still_album()

# create Scene folder
for scene in scene_set:
    dpx_scene_path = path.join(DPX_PATH, "SC" + scene)
    try:
        os.makedirs(dpx_scene_path)
    except FileExistsError as e:
        print(f"{dpx_scene_path} exists!")

# export DPX stills
for still in still_dict:
    dpx_scene_path = path.join(DPX_PATH, "SC" + still_dict[still])
    current_album.export_stills(
        gallery_stills=[still],
        folder_path=dpx_scene_path,
        file_prefix=current_album.get_label(still),
        format=StillFormats.DPX,
    )

# clear album
stills = current_album.get_stills()
current_album.delete_stills(stills)


# remove DRX files
def remove_drx(dpx_path):
    remove_count = 0
    for f in listdir(dpx_path):
        if f == ".DS_Store":
            continue
        file_extension = path.splitext(f)[1]
        # remove drx file
        if file_extension == ".drx":
            os.remove(path.join(dpx_path, f))
            remove_count += 1
            continue
    print(f"delete {remove_count} drx files at {dpx_path}")


dpx_scene_list = [f.name for f in os.scandir(DPX_PATH) if f.is_dir()]

for scene_folder in dpx_scene_list:
    remove_drx(path.join(DPX_PATH, scene_folder))