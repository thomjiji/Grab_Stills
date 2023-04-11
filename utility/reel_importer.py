from os import DirEntry, path
import re

from utility.pattern import *


class Reel_Importer(object):
    """Reel_Importer"""

    def __init__(self, reel_path: DirEntry):
        super(Reel_Importer, self).__init__()
        self.reel_path = reel_path

    def get_reel_name(self):
        return self.reel_path.name

    def get_reel_path(self):
        return self.reel_path.path

    def get_source_clip_path(self) -> str:
        if CANON_C_REEL_REGEX.match(self.get_reel_name()) != None:
            reel_number = re.findall(
                r"Canon[A-Z]([0-9]{3})", self.get_reel_name()
            )[0]
            return path.join(self.get_reel_path(), f"CRM/REEL_{reel_number}")
        if ARRI_ALEXA_REEL_REGEX.match(self.get_reel_name()) != None:
            return self.get_reel_path()
        if ARRI_ALEXA_35_REEL_REGEX.match(self.get_reel_name()) != None:
            return self.get_reel_path()

        return "No match source!"
