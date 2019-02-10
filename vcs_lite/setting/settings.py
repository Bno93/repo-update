""" Handle the settings file  """
import os
import json

from pathlib import Path

class Settings(object):
    """ Settings class which provides read and save functions for the settings file """
    def __init__(self):
        self.settings_file = 'settings.json'
        self.settings_dir = str(Path.home()) + '\\.vcs-lite'
        self.settings_default = {
            "toUpdate": [
                {
                    "label": "Git Repo",
                    "folder": "",
                    "vcs": {
                        "program": "git",
                        "command": "pull"
                    },
                    "enabled": True
                },
                {
                    "label": "Svn Repo",
                    "folder": "",
                    "vcs": {
                        "program": "svn",
                        "command": "update"
                    },
                    "enabled": True
                },
            ]
        }
    # end

    def _set_settings(self, settings):
        with open(self._get_sttings_path(), "w") as write_settings:
            json.dump(settings, write_settings, indent=4)
        # end
    # end

    # TODO use path join
    def _get_sttings_path(self):
        return "{}\\{}".format(self.settings_dir, self.settings_file)
    # end

    def load_settings(self):
        """ loads the settings file and create an empty one if file dosen't exists """
        loaded_settings = {}
        try:
            with open(self._get_sttings_path(), 'r') as settings_file:
                loaded_settings = json.load(settings_file)
            # end

        except IOError:
            self.make_default_settings()
            return self.load_settings()
        # end
        return loaded_settings
    # end

    def make_default_settings(self):
        """ create default settings file """
        if not os.path.exists(self.settings_dir):
            os.makedirs(self.settings_dir)
        # end
        self._set_settings(self.settings_default)
    # end

# end