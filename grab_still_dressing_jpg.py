import os
import time
from os import listdir, path

from dftt_timecode import DfttTimecode
from fpdf import FPDF
from pybmd import Bmd
from pybmd.gallery_still_album import StillFormats

from utility.pattern import *
from utility.watermark import watermark_to_jpg

LOCAL_RESOLVE = Bmd()
LOCAL_FUSION = LOCAL_RESOLVE.fusion()
project_manager = LOCAL_RESOLVE.get_project_manager()
current_project = project_manager.get_current_project()
current_timeline = current_project.get_current_timeline()

if DID_REGEX_L.match(current_timeline.get_name()) is None:
    print("timeline name is not a valid DID!")
    exit()
else:
    DID = DID_REGEX_L.findall(current_timeline.get_name())[0][0]

DRESSING_STILL_PATH = "/Volumes/RAID6_230201/Output/toDressing"

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
still_dcit = {}
scene_set = set()

for marker_frameid in marker_list:
    marker_timecode: DfttTimecode = timeline_start_timecode + marker_frameid
    current_timeline.set_current_timecode(marker_timecode.timecode_output())
    timeline_item = current_timeline.get_current_video_item()
    scene = timeline_item.get_media_pool_item().get_metadata("Scene")
    if scene not in scene_set:
        scene_set.add(scene)
    still = current_timeline.grab_still()
    still_dcit.update({still: scene})

    time.sleep(0.15)

current_gallery = current_project.get_gallery()
current_album = current_gallery.get_current_still_album()

# export JPG stills
JPG_PATH = path.join(DRESSING_STILL_PATH, DID)
try:
    os.makedirs(JPG_PATH)
except Exception as e:
    print(f"{JPG_PATH} exists!")
for still in still_dcit:
    still_label = current_album.get_label(still)
    still_label += f"_SC{still_dcit[still]}"
    current_album.export_stills(
        gallery_stills=[still],
        folder_path=JPG_PATH,
        file_prefix=still_label,
        format=StillFormats.JPG,
    )

# clear album
stills = current_album.get_stills()
current_album.delete_stills(stills)


# remove DRX files
def remove_drx(STILL_PATH):
    remove_count = 0
    for f in listdir(STILL_PATH):
        if f == ".DS_Store":
            continue
        file_name = path.splitext(f)[0]
        file_extention = path.splitext(f)[1]
        # remove drx file
        if file_extention == ".drx":
            os.remove(path.join(STILL_PATH, f))
            remove_count += 1
            continue
    print(f"delete {remove_count} drx files at {STILL_PATH}")


remove_drx(JPG_PATH)

# add watermark to jpg and create pdf
SCENE_FIND_REG = re.compile(r"(?:.*)_(SC.*)_[0-9]{1,}\.[0-9]{1,}\.[0-9]{1,}.*")

pdf = FPDF("P", "pt", (2048, 858))

for f in os.scandir(JPG_PATH):
    if f.name == ".DS_Store":
        continue
    scene_name = SCENE_FIND_REG.findall(f.name)[0]
    watermark_to_jpg(f.path, f.path, scene_name)
    pdf.add_page()
    pdf.image(f.path, 0, 0)

pdf_output_path = JPG_PATH + f"/{DID}_服装组专阅.pdf"
pdf.output(pdf_output_path)