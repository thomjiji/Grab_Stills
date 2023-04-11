from os import path
import os


class DTG_Path(object):
    """DTG_Path."""

    def __init__(self, DID_8: str, volume_name: str, volume_type: str):
        super(DTG_Path, self).__init__()
        self.DID_8 = DID_8
        self.volume_name = volume_name
        self.volume_type = volume_type

        # volume_path for macos
        if volume_name is "/":
            self.volume_path = "/Volumes/Macintosh HD"
        else:
            self.volume_path = path.join("/Volumes", volume_name)

    def get_date_id(self):
        return self.DID_8

    def get_source_path(self):
        if self.volume_type is "RAID":
            _source_path = path.join(
                self.volume_path, f"Source_Media/{self.DID_8}/Source"
            )
            if path.exists(_source_path):
                return _source_path
            else:
                print("No source found for DID")
                return None
        else:
            return None

    def get_still_temp_path(self):
        if self.volume_type is "RAID":
            return path.join(self.volume_path, f"Still/{self.DID_8}/temp")
        if self.volume_type is "Desktop":
            return path.join(
                path.expanduser("~"), f"Desktop/Still/{self.DID_8}/temp"
            )

    def get_still_path(self):
        if self.volume_type is "RAID":
            return path.join(self.volume_path, f"Still/{self.DID_8}/")
        if self.volume_type is "Desktop":
            return path.join(
                path.expanduser("~"), f"Desktop/Still/{self.DID_8}/"
            )
