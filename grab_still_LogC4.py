import os, shutil
import re
import time
from pybmd import Bmd
from pybmd.gallery_still_album import StillFormats
from pybmd.toolkits import *
from dftt_timecode import DfttTimecode
from utility.dtg_path_generator import DTG_Path

from utility.still_renamer import still_renamer
from utility.timeline_render import timeline_render
from utility.pattern import *

LOCAL_RESOLVE = Bmd()
LOCAL_FUSION = LOCAL_RESOLVE.fusion()

project_manager = LOCAL_RESOLVE.get_project_manager()
current_project = project_manager.get_current_project()
current_timeline = current_project.get_current_timeline()

DID = current_timeline.get_name()
# DID = timeline_name[:timeline_name.rfind("_")]

BASE_FOLDER = "/Users/kelvin/Desktop/Still/JPG_OUT/LogC4_2048_858_239/" + DID

try:
    os.makedirs(BASE_FOLDER)
except Exception as e:
    print(e)

timeline_framerate = int(
    current_timeline.get_setting("timelinePlaybackFrameRate")
)
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
stills = []

# grab stills for every marker
for marker_frameid in marker_list:
    marker_timecode: DfttTimecode = timeline_start_timecode + marker_frameid
    current_timeline.set_current_timecode(marker_timecode.timecode_output())
    timeline_item = current_timeline.get_current_video_item()
    pro = timeline_item.get_media_pool_item().get_clip_property()

    # get frame count for the marker
    clip_start_timecode = DfttTimecode(
        timeline_item.get_media_pool_item().get_clip_property("Start TC"),
        "auto",
        timeline_framerate,
    )
    clip_frame_count = (
        marker_frameid
        - (
            timeline_item.get_start()
            - int(timeline_start_timecode.timecode_output("frame"))
        )
        + int(clip_start_timecode.timecode_output("frame"))
    )

    reel_name = timeline_item.get_media_pool_item().get_clip_property(
        "Reel Name"
    )
    # reel_number=re.findall(r'(^[a-z0-9A-Z_]{6})',reel_name)[0]
    clip_name = timeline_item.get_media_pool_item().get_clip_property(
        "Clip Name"
    )
    name, ext = os.path.splitext(clip_name)
    frames = timeline_item.get_media_pool_item().get_clip_property("Frames")

    still = current_timeline.grab_still()
    stills.append({"name": name, "frame": clip_frame_count, "obj": still})
    time.sleep(0.5)

current_gallery = current_project.get_gallery()
current_album = current_gallery.get_current_still_album()

for still in stills:
    file = "%s.mxf_%s" % (still["name"], still["frame"])
    path = BASE_FOLDER + "/" + file + ".jpg"
    print(still)
    if os.path.exists(path):
        os.remove(path)
    current_album.export_stills(
        gallery_stills=[still["obj"]],
        folder_path=BASE_FOLDER,
        file_prefix=file,
        format=StillFormats.JPG,
    )


stills = current_album.get_stills()
current_album.delete_stills(stills)

files = list(os.walk(BASE_FOLDER))[0][2]
for file in files:
    if ".drx" in file:
        os.remove(BASE_FOLDER + "/" + file)
