from logging import debug, warning
from os import listdir, path
import os
import re


def still_renamer(still_file_path: str):
    remove_count = 0
    for f in listdir(still_file_path):
        if f == ".DS_Store":
            continue
        file_name = path.splitext(f)[0]
        file_extention = path.splitext(f)[1]

        # remove drx file
        if file_extention == ".drx":
            os.remove(path.join(still_file_path, f))
            remove_count += 1
            continue

        _f = re.findall(r"(.*)__[0-9]{1,}\.[0-9]{1,}\.[0-9]{1,}", file_name)

        if bool(_f):
            _file_name = _f[0]
            os.rename(
                path.join(still_file_path, f),
                path.join(still_file_path, _file_name) + file_extention,
            )
        else:
            warning(f"{file_name}.tiff exist!")
            continue

    print(f"delete {remove_count} drx files")
