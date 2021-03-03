import os
import glob
import time
from datetime import datetime
import PyQt5.QtCore as QtCore


class getLogs(QtCore.QThread):
    """Define Signal for main window"""
    newLog = QtCore.pyqtSignal(dict)  # Signal emits new log to main Thread

    def __init__(self, config, parent=None):
        """Init Thread"""
        QtCore.QThread.__init__(self, parent)
        self.config = config
        """Add bosses for changing display name in following pattern: '<folder name>': '<custom name>'"""
        self.bossList = {'Vale Guardian': 'Vale Guardian',
                         'Gorseval the Multifarious': 'Gorseval the Multifarious',
                         'Sabetha the Saboteur': 'Sabetha the Saboteur',
                         'Slothasor': 'Slothasor',
                         'Berg': 'Bandit Trio',
                         'Matthias Gabrel': 'Matthias Gabrel',
                         'Keep Construct': 'Keep Construct',
                         'Haunting Statue': 'Twisted Castle',
                         'Xera': 'Xera',
                         'Cairn the Indomitable': 'Cairn the Indomitable',
                         'Mursaat Overseer': 'Mursaat Overseer',
                         'Samarog': 'Samarog',
                         'Deimos': 'Deimos',
                         'Soulless Horror': 'Soulless Horror',
                         'Desmina': 'River of Souls',
                         'Broken King': 'Broken King',
                         'Eater of Souls': 'Eater of Souls',
                         'Eye of Fate': 'Eyes of Judgment and Fate',
                         'Eye of Judgment': 'Eyes of Judgment and Fate',
                         'Dhuum': 'Dhuum',
                         'Conjured Amalgamate': 'Conjured Amalgamate',
                         'Nikare': 'Twin Largos',
                         'Qadim': 'Qadim',
                         'Cardinal Sabir': 'Cardinal Sabir',
                         'Cardinal Adina': 'Cardinal Adina',
                         'Qadim the Peerless': 'Qadim the Peerless'}

    def run(self):
        """script to get new generated log files"""
        path = self.config["explorer"]["path"]
        if not path:
            path = f'C:\\Users\\{os.getlogin()}\\Documents\\Guild Wars 2\\addons\\arcdps\\arcdps.cbtlogs'

        while True:
            list_of_files = glob.glob(f'{path}/**/*.zevtc', recursive=True)
            if len(list_of_files) > 0:
                old_latest_file = max(list_of_files, key=os.path.getctime)

                while True:
                    returnDict = {}
                    list_of_files = glob.glob(f'{path}/**/*.zevtc', recursive=True)
                    new_latest_file = max(list_of_files, key=os.path.getctime)
                    if new_latest_file != old_latest_file:
                        returnDict['path'] = new_latest_file
                        returnDict['time'] = datetime.now().strftime('%H:%M:%S')
                        returnDict['url'] = ''
                        log_name = new_latest_file.split('\\')[-2]
                        returnDict['name'] = self.bossList[log_name] if log_name in self.bossList else log_name
                        self.newLog.emit(returnDict)
                        old_latest_file = new_latest_file
                    time.sleep(float(self.config['explorer']['refresh_rate']))

            else:
                time.sleep(float(self.config['explorer']['refresh_rate']))
