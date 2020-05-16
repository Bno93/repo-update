""" Handle the settings file  """
import os
import json
import logging

from pathlib import Path

class Settings():
    """ Settings class which provides read and save functions for the settings file """
    def __init__(self):
        self.settings_file = 'settings.json'
        self.settings_dir = os.path.join(str(Path.home()), '.vcs-lite')
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
        with open(self.get_sttings_path(), "w") as write_settings:
            json.dump(settings, write_settings, indent=4)
        # end
    # end

    def get_sttings_path(self):
        return os.path.join(self.settings_dir, self.settings_file)
    # end

    def load_settings(self):
        """ loads the settings file and create an empty one if file dosen't exists """
        loaded_settings = {}
        try:
            logging.info('open %s', self.get_sttings_path())
            with open(self.get_sttings_path(), 'r') as settings_file:

                loaded_settings = json.load(settings_file)
            # end

        except IOError:
            self.make_default_settings()
            return self.load_settings()
        except json.JSONDecodeError as decode_error:
            logging.error('couldn\'t parse settings %s(%s:%s)',
                          self.get_sttings_path,
                          decode_error.lineno,
                          decode_error.colno)
            return None
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
