import os
import re
import time
import argparse
from pybmd import Bmd
from pybmd.gallery_still_album import StillFormats
from pybmd.toolkits import get_timeline
from dftt_timecode import DfttTimecode

from utility.still_renamer import still_renamer
from utility.timeline_render import timeline_render


def grab_still(render_path: str, temp_path: str):
    LOCAL_RESOLVE = Bmd()
    LOCAL_FUSION = LOCAL_RESOLVE.fusion()

    project_manager = LOCAL_RESOLVE.get_project_manager()
    current_project = project_manager.get_current_project()
    current_timeline = current_project.get_current_timeline()

    RENDER_PATH = render_path
    if temp_path is None:
        TEMP_PATH = os.path.join(RENDER_PATH, "TEMP")
    else:
        TEMP_PATH = temp_path

    DID = current_timeline.get_name()

    try:
        os.makedirs(TEMP_PATH)
    except Exception as e:
        print(f"{TEMP_PATH} exists!")

    try:
        os.makedirs(RENDER_PATH)
    except Exception as e:
        print(f"{RENDER_PATH} exists!")

    timeline_framerate = int(current_timeline.get_setting("timelineFrameRate"))
    resolve_version = LOCAL_RESOLVE.get_version()

    # get timeline start timecode
    if resolve_version[0] == 18:
        timeline_start_timecode = DfttTimecode(
            current_timeline.get_start_timecode(),
            "auto",
            timeline_framerate,
            False,
            True,
        )
    else:
        timeline_start_timecode = DfttTimecode(
            "01:00:00:00", "auto", timeline_framerate, False, True
        )

    marker_list = current_timeline.get_markers()
    still_dict = {}

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
            False,
            True,
        )
        clip_frame_count = (
            marker_frameid
            - (
                timeline_item.get_start()  # Get clip start frame position on the timeline.
                - int(timeline_start_timecode.timecode_output("frame"))
            )
            + int(clip_start_timecode.timecode_output("frame"))
        )

        reel_name = timeline_item.get_media_pool_item().get_clip_property(
            "Reel Name"
        )
        reel_number = reel_name
        file_name = timeline_item.get_media_pool_item().get_clip_property(
            "File Name"
        )
        frames = timeline_item.get_media_pool_item().get_clip_property("Frames")

        still = current_timeline.grab_still()
        still_dict.update(
            {still: [reel_number, file_name, frames, f"{clip_frame_count:08d}"]}
        )
        time.sleep(0.5)

    current_gallery = current_project.get_gallery()
    current_album = current_gallery.get_current_still_album()

    # export TIFF stills

    ## scan tiff file path skip export if tiff file already exist
    file_name_list = [
        os.path.splitext(f.name)[0]
        for f in os.scandir(TEMP_PATH)
        if f.is_file()
    ]

    for still in still_dict:
        still_property = still_dict[still]
        _file_prefix = "".join([str(data) + "_" for data in still_property])
        if _file_prefix in file_name_list:
            continue
        else:
            current_album.export_stills(
                gallery_stills=[still],
                folder_path=TEMP_PATH,
                file_prefix=_file_prefix,
                format=StillFormats.TIF,
            )

    # clear album
    stills = current_album.get_stills()
    current_album.delete_stills(stills)

    # rename TIFF still files
    still_renamer(TEMP_PATH)

    # import TIFF to resolve and transcode to ProRes4444 single frame

    ## Clean RENDER_PATH
    exist_mov_list = [f.path for f in os.scandir(RENDER_PATH) if f.is_file()]
    for f in exist_mov_list:
        os.remove(f)

    current_media_pool = current_project.get_media_pool()
    current_media_pool.set_current_folder(
        current_media_pool.add_sub_folder(
            current_media_pool.get_current_folder(), "TIFF"
        )
    )

    ## delete temp timeline if exist
    _timeline = get_timeline(current_project, f"TEMP_{DID}")
    if bool(_timeline):
        current_media_pool.delete_timelines([_timeline])
    render_timeline = current_media_pool.create_timeline_from_clips(
        f"TEMP_{DID}", current_media_pool.import_media(TEMP_PATH)
    )
    timeline_render(
        project=current_project,
        timeline=render_timeline,
        render_destination=RENDER_PATH,
    )


if __name__ == "__main__":
    paser = argparse.ArgumentParser(
        "grab still from davinci resolve timeline marker"
    )
    paser.add_argument(
        "-renderPath",
        "-rP",
        required=True,
        help="prores 4444 mov still render path",
    )
    paser.add_argument("-tempPath", "-tP", help="temp still file path ")

    args = paser.parse_args()
    render_path = args.renderPath
    temp_path = args.tempPath
    grab_still(render_path=render_path, temp_path=temp_path)