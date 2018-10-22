import os
import json

from pathlib import Path

class Settings(object):
  def __init__(self):
    self.settings_file = 'settings.json'
    self.settings_dir = str(Path.home()) + '\\.repo-updater'
    self.settings_default = {
        "execpath": ".",
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
      write_settings.closed
  # end

  # TODO use path join 
  def _get_sttings_path(self):
    return "{}\\{}".format(self.settings_dir, self.settings_file)
  # end

  def load_settings(self):
      loaded_settings = {}
      try:
          with open(self._get_sttings_path(), 'r') as settings_file:
              loaded_settings = json.load(settings_file)
          # end

          settings_file.closed
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
    self._set_settings(self.settings_default)
# end

# end