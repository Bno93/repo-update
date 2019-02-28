import sys
import os
import subprocess
import logging
# import tempfile
# sys.stdout = tempfile.TemporaryFile()
# sys.stderr = tempfile.TemporaryFile()

class Updater(object):
    """ class which handles the execution of the update command """
    def __init__(self):
        logging.basicConfig(filename="vcs-lite.log",
                            level=logging.INFO,
                            format='[%(asctime)s] %(levelname)s - %(message)s',
                            datefmt='%d-%m-%Y %H:%M:%S')
    # end

    def update(self, label, path, vcs):
        """ execute the vcs update command """

        repo = {
            'label': label,
            'path': path,
            'status': '',
            'message': []
        }

        logging.info('updating {} [{}]'.format(path, vcs['program']))

        try:
            os.chdir(path)
        except Exception:
            logging.error("could not find path to repository")
            repo['status'] = "warning"
            repo['message'].append(['folder not found'])
            return repo
        # end

        cmd = ""
        if vcs['program'] == 'git':
            cmd = vcs['program'] + " " + vcs['command']
        elif vcs['program'] == 'svn':
            cmd = vcs['program'] + " " + vcs['command']
        # end

        # message = []
        try:
            logging.info("init subprocess")
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            proc = subprocess.Popen(cmd, universal_newlines=True,
                                    stdout=subprocess.PIPE,
                                    stdin=subprocess.PIPE,
                                    stderr=subprocess.STDOUT,
                                    startupinfo=startupinfo)
            for line in proc.stdout:
                logging.info("exec update: {}".format(line))
                if 'up to date' in line or 'At revision' in line:
                    repo['status'] = "upToDate"
                elif 'conflict' in line:
                    repo['status'] = 'conflict'
                elif 'error' in line:
                    repo['status'] = 'conflict'
                elif 'Updating' in line or 'Updated to revision':
                    repo['status'] = "updating"
                # end

                line.replace('\n', '')
                line.replace('\t', '')
                logging.info(line)

                repo['message'].append(str(line))
            # end
        except subprocess.CalledProcessError as err:
            # print("ERROR: " + err)
            logging.error("error: " + err)
            sys.exit(-1)
        except KeyboardInterrupt:
            # print("stop updating")
            logging.warning("updating was cancled by CTR+C")
            sys.exit(-2)
        except Exception as e:
            logging.error("something went wrong: {}".format(e))
        finally:

            logging.info("exit updater")
        # end
        return repo

    # end
