import requests
import PyQt5.QtCore as QtCore


class UploadLogs(QtCore.QThread):
    """Define Signal for main window"""
    newUpload = QtCore.pyqtSignal(dict)

    def __init__(self, path, row, config, parent=None):
        """Init Thread"""
        QtCore.QThread.__init__(self, parent)
        self.log_path = path
        self.row = row
        self.userToken = config['webhook']['user_token']
        self.url = f'https://dps.report/uploadContent?json=1&generator=ei&userToken={self.userToken}'

    def run(self):
        """Upload file to dps.report for permalink and basic information"""
        returnDict = {}
        file = {'file': ('dps_log.zevtc', open(self.log_path, 'rb'), 'text/zevtc')}
        r = requests.post(self.url, files=file)
        if r.status_code == 200:
            info = r.json()
            returnDict['success'] = str(info['encounter']['success'])
            returnDict['url'] = str(info['permalink'])
            returnDict['code'] = str(r.status_code)
            returnDict['row'] = self.row
        else:
            returnDict['success'] = 'Error'
            returnDict['url'] = ''
            returnDict['code'] = str(r.status_code)
            returnDict['row'] = self.row
        self.newUpload.emit(returnDict)
