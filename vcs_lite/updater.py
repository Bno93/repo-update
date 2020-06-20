import sys
import os
import subprocess
import logging
from settings import Settings

class Updater(object):
    """ class which handles the execution of the update command """
    def __init__(self):
        self.settings = Settings()
    # end

    def update_all(self):
        # check if settings could be laoded
        loaded_settings = self.settings.load_settings()

        if(not loaded_settings):
            logging.error("couldn't load settings")
            raise IOError('not settings file')
        # end

        update_list = loaded_settings['toUpdate']
        report = { 'repos': [] }
        try:
            for repo in update_list:
                if repo['enabled']:
                    vcs = repo['vcs']
                    result = self.update(repo['label'],
                                            repo['folder'], vcs)
                    report['repos'].append(result)
                else:
                    repo = {
                        'label': repo['label'],
                        'path': repo['folder'],
                        'status': 'disabled',
                        'message': ["repo not enabled to update"]
                    }
                    report['repos'].append(repo)
                # end
            # end
        except KeyboardInterrupt:
            pass

        # end

    def update(self, label, path, vcs):
        """ execute the vcs update command """
        logging.info("{} with {program} {command}".format(label, **vcs))
        repo = {
            'label': label,
            'path': path,
            'status': '',
            'message': []
        }

        logging.info('updating %s [%s]', path, vcs['program'])

        try:
            logging.info("change dir to %s", path)
            os.chdir(path)
        except FileNotFoundError as fnf:
            logging.error("could not find path to repository %s", fnf)
            repo['status'] = "warning"
            repo['message'].append(['folder not found'])
            return repo
        except PermissionError as perm:
            logging.error("could not find path to repository %s", perm)
            repo['status'] = "warning"
            repo['message'].append(['folder not found'])
            return repo
        # end

        cmd = [vcs['program'], vcs['command']]

        try:
            logging.info("init subprocess")
            startupinfo = None

            if sys.platform == "win32":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            proc = subprocess.Popen(cmd, universal_newlines=True,
                                    stdout=subprocess.PIPE,
                                    stdin=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    startupinfo=startupinfo)
            for line in proc.stdout:
                # print(line)
                line.replace("\n", "")
                logging.info("exec update: %s", line)
                if 'up to date' in line:
                    repo['status'] = "upToDate"
                elif 'At revision' in line:
                    repo['status'] = "upToDate"
                elif 'Bereits aktuell' in line:
                    repo['status'] = "upToDate"
                elif 'Already up to date.' in line:
                    repo['status'] = "upToDate"
                elif 'conflict' in line:
                    repo['status'] = 'conflict'
                elif 'error' in line:
                    repo['status'] = 'conflict'
                elif 'Updating' in line or 'Updated to revision' in line:
                    repo['status'] = "updating"
                else:
                    repo['status'] = 'unknown'
                # end

                line.replace('\n', '')
                line.replace('\t', '')
                logging.info(line)

                repo['message'].append(str(line))
            # end
        except subprocess.CalledProcessError as err:
            # print("ERROR: " + err)
            logging.error("error: %s", err)
            sys.exit(-1)
        except KeyboardInterrupt:
            # print("stop updating")
            logging.warning("updating was cancled by CTR+C")
            sys.exit(-2)
        except FileNotFoundError as fnf:
            print(fnf)
            logging.error("error: %s", fnf)
        finally:

            logging.info("exit updater")
        # end
        return repo

    # end
