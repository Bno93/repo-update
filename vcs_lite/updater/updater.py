import sys
import os
import subprocess
import logging


class Updater(object):
    """ class which handles the execution of the update command """
    def __init__(self):
        self.updtodate = ['up to date', 'At revision', 'Bereits aktuell']
    # end

    def update(self, label, path, vcs):
        """ execute the vcs update command """
        print("{} with {program} {command}".format(label, **vcs))
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
            output = str(proc.communicate())
            print("output: {}".format(output))
            for line in output[0]:
                # print(line)
                logging.info("exec update: %s", line)
                if line in self.updtodate:
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
