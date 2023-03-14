import os
from os import path

from pybmd import Bmd
from pybmd.gallery_still_album import StillFormats

STILL_PROJECT_PATH = "/Users/wheheohu/Desktop/80220401"
#STILL_PROJECT_PATH = "/Users/wheheohu/Desktop/Still_Export_Test"

LOCAL_RESOLVE = Bmd()
project_manager = LOCAL_RESOLVE.get_project_manager()
current_project = project_manager.get_current_project()
current_timeline = current_project.get_current_timeline()
timeline_name = current_timeline.get_name()
export_path = os.path.join(STILL_PROJECT_PATH, timeline_name)
if not os.path.exists(export_path):
    os.makedirs(export_path)
stills = current_timeline.grab_all_stills(1)
current_gallery = current_project.get_gallery()
current_album = current_gallery.get_current_still_album()
for still in stills:
    still_label = current_album.get_label(still)
    current_album.export_stills(
        [still], folder_path=export_path, file_prefix=still_label, format=StillFormats.PNG)


# for DEBUG
#current_album.delete_stills(stills)

# remove drx
for f in os.listdir(export_path):
    file_name, file_extention = path.splitext(f)
    if file_extention == '.drx':
        os.remove(path.join(export_path, f))


def main():
    print(export_path)


if __name__ == "__main__":
    main()
