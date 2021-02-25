import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
import bin.MainWindowStyle as MwStyle
import bin.config as config
import bin.explorer as explorer
import bin.webhook as webhook
import bin.network as network
import sys
import os


class App(QtWidgets.QMainWindow):
    def __init__(self, mw_name, mw_x, mw_y, version):
        super().__init__()
        self.mw_name = mw_name
        self.mw_x = mw_x
        self.mw_y = mw_y
        self.version = version

        """define global varibales"""
        self.log_dict = {}
        self.config_dict = config.read_settings()
        self.autoUploadEnabled = False

        """define icons and graphics"""
        self.close_icon = 'graphics/close.png'
        self.minimize_icon = 'graphics/minimize.png'
        self.info_icon = 'graphics/info.png'
        self.success_icon = 'graphics/success_mono.png'
        self.fail_icon = 'graphics/fail_mono.png'
        self.upload_icon = 'graphics/upload.png'
        self.error_icon = 'graphics/error_mono.png'
        self.copy_icon = 'graphics/copy.png'
        self.open_icon = 'graphics/open.png'
        self.pause_icon = 'graphics/pause.png'
        self.start_icon = 'graphics/start.png'
        self.discord_icon = 'graphics/discord.png'
        self.settings_icon = 'graphics/settings_mini.png'
        self.clock_icon = 'graphics/clock.png'
        self.app_icon = 'graphics/logo.png'  # Windows Icon
        self.app_icons = 'graphics/logos.png'  # Header Icon
        self.add_icon = 'graphics/add.png'
        self.remove_icon = 'graphics/remove.png'
        self.select_icon = 'graphics/select.png'

        """init UI"""
        self.initUI()
        self.show()

    def initUI(self):
        """MainWindow Attributes"""
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # remove window frame
        self.setStyleSheet(MwStyle.window())
        self.setFixedSize(self.mw_x, self.mw_y)
        self.setWindowIcon(QtGui.QIcon(self.app_icon))
        self.setWindowTitle(self.mw_name)
        self.mw_center()

        """init ui elements"""
        self.windowIcon()
        self.windowBackground()
        self.windowCloseBtn()
        self.windowMinimizeBtn()
        self.windowInfoBtn()

        """init widgets"""
        self.logTableWidget()
        self.timeTableWidget()
        self.discordStartBtn()
        self.webhookSelectMenu()
        self.discordPostTB()
        self.discordPostBtn()
        self.openLinkBtn()
        self.copyLinkBtn()

        """init settings"""
        self.openSettingsBtn()

        """start looking for new logs: new thread"""
        self.explorerThread = explorer.getLogs(self.config_dict)
        self.explorerThread.newLog.connect(self.updateLists)
        self.explorerThread.start()

    def mw_center(self):
        """Open MW centered on current screen"""
        monitor_res = QtWidgets.QDesktopWidget().screenGeometry()
        x = (monitor_res.width() / 2) - (self.frameSize().width() / 2)
        y = (monitor_res.height() / 2) - (self.frameSize().height() / 2)
        self.move(x, y)

    def mousePressEvent(self, event):
        """Window Drag actions since window frame is removed (pressing)"""
        if event.button() == QtCore.Qt.LeftButton and event.pos().y() <= 28:  # draggable only on top bar and with L-Btn
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Window Drag actions since window frame is removed (moving)"""
        if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Window Drag actions since window frame is removed (releasing)"""
        self.offset = None
        super().mouseReleaseEvent(event)

    def windowIcon(self):
        """Set Icon in top left corner"""
        self.ui_windowIcon = QtWidgets.QListWidget(self)
        self.ui_windowIcon.setGeometry(4, 4, 20, 20)
        self.ui_windowIcon.setStyleSheet(MwStyle.icon(self.app_icons))

    def windowBackground(self):
        """Top window bar for buttons"""
        self.ui_titleBar = QtWidgets.QListWidget(self)
        self.ui_titleBar.setGeometry(0, 28, 400, 572)
        self.ui_titleBar.setStyleSheet(MwStyle.background())

    def windowCloseBtn(self):
        """Creates close button for Main Window"""
        self.btn_WindowClose = QtWidgets.QPushButton('', self)
        self.btn_WindowClose.setGeometry(376, 4, 20, 20)
        self.btn_WindowClose.setIcon(QtGui.QIcon(self.close_icon))
        self.btn_WindowClose.setIconSize(QtCore.QSize(10, 10))
        self.btn_WindowClose.setStyleSheet(MwStyle.closeBtn())
        self.btn_WindowClose.setToolTip('Close')
        self.btn_WindowClose.clicked.connect(self.windowCloseBtnAction)

    def windowCloseBtnAction(self):
        """Called when close button pressed: stop program"""
        sys.exit()

    def windowMinimizeBtn(self):
        """Creates minimize button for Main Window"""
        self.btn_WindowMinimize = QtWidgets.QPushButton('', self)
        self.btn_WindowMinimize.setGeometry(352, 4, 20, 20)
        self.btn_WindowMinimize.setIcon(QtGui.QIcon(self.minimize_icon))
        self.btn_WindowMinimize.setIconSize(QtCore.QSize(10, 10))
        self.btn_WindowMinimize.setStyleSheet(MwStyle.minimizeBtn())
        self.btn_WindowMinimize.setToolTip('Minimize')
        self.btn_WindowMinimize.clicked.connect(self.windowMinimizeBtnAction)

    def windowMinimizeBtnAction(self):
        """Called when minimize button is pressed: minimizes program"""
        self.showMinimized()

    def windowInfoBtn(self):
        """Creates info button"""
        self.btn_WindowInfo = QtWidgets.QPushButton('', self)
        self.btn_WindowInfo.setGeometry(328, 4, 20, 20)
        self.btn_WindowInfo.setIcon(QtGui.QIcon(self.info_icon))
        self.btn_WindowInfo.setIconSize(QtCore.QSize(12, 12))
        self.btn_WindowInfo.setStyleSheet(MwStyle.infoBtn())
        self.btn_WindowInfo.setToolTip('Info')
        self.btn_WindowInfo.clicked.connect(self.windowInfoBtnAction)

    def windowInfoBtnAction(self):
        """Open/Close info window with author and version"""
        pass

    def logTableWidget(self):
        """Creates list widget for log name and status"""
        self.lw_logTable = QtWidgets.QListWidget(self)
        self.lw_logTable.setGeometry(4, 52, 301, 520)
        self.lw_logTable.setStyleSheet(MwStyle.logTable())
        self.lw_logTable.setFocusPolicy(QtCore.Qt.NoFocus)

        self.ui_logTableTitle = QtWidgets.QLabel('NAME', self)
        self.ui_logTableTitle.setGeometry(4, 32, 301, 20)
        self.ui_logTableTitle.setStyleSheet(MwStyle.logTableTitle())
        self.ui_logTableTitle.setAlignment(QtCore.Qt.AlignCenter)

    def timeTableWidget(self):
        """Creates list widget for log time"""
        self.lw_timeTable = QtWidgets.QListWidget(self)
        self.lw_timeTable.setGeometry(307, 52, 88, 520)
        self.lw_timeTable.setStyleSheet(MwStyle.timeTable())
        self.lw_timeTable.setFocusPolicy(QtCore.Qt.NoFocus)

        self.ui_timeTableTitle = QtWidgets.QLabel('TIME', self)
        self.ui_timeTableTitle.setGeometry(307, 32, 88, 20)
        self.ui_timeTableTitle.setStyleSheet(MwStyle.timeTableTitle())
        self.ui_timeTableTitle.setAlignment(QtCore.Qt.AlignCenter)

    def updateLists(self, logDict):
        """Update lists when new logs are generated"""
        self.lw_logTable.addItem(logDict['name'])
        log_item = self.lw_logTable.item(self.lw_logTable.count() - 1)
        log_item.setIcon(QtGui.QIcon(self.upload_icon))
        log_item.setToolTip('Uploading...')

        self.lw_timeTable.addItem(logDict['time'])
        time_item = self.lw_timeTable.item(self.lw_timeTable.count() - 1)
        time_item.setIcon(QtGui.QIcon(self.clock_icon))

        self.log_dict[self.lw_logTable.count() - 1] = logDict
        row = self.lw_logTable.count() - 1
        path = logDict['path']
        self.initUpload(path, row)

    def initUpload(self, path, row):
        """Upload file to dps.report for further information  -> New Thread"""
        self.uploadThread = network.UploadLogs(path, row, self.config_dict)
        self.uploadThread.newUpload.connect(self.updateIcon)
        self.uploadThread.start()

    def updateIcon(self, updateDict):
        """Handle Icon updates and error handles"""
        row = updateDict['row']
        url = updateDict['url']
        scode = updateDict['code']
        success = updateDict['success']
        if success == 'Error':  # TODO: Implement retry button in case of error (height: 52px + (row * 21px)) when button is 21px x 21px
            self.lw_logTable.item(row).setIcon(QtGui.QIcon(self.error_icon))
            self.lw_logTable.item(row).setToolTip('ERROR Code: ' + scode)
        elif success == 'False':
            self.lw_logTable.item(row).setIcon(QtGui.QIcon(self.fail_icon))
            self.lw_logTable.item(row).setToolTip('Fail')
            self.log_dict[row]['url'] = url

        elif success == 'True':
            self.lw_logTable.item(row).setIcon(QtGui.QIcon(self.success_icon))
            self.lw_logTable.item(row).setToolTip('Success')
            self.log_dict[row]['url'] = url
            if self.autoUploadEnabled:
                self.initPost(url)
        else:
            pass

    def initPost(self, log_url):
        """Post Log on discord  -> New Thread"""
        if self.config_dict['webhook']['url'] != '':
            self.webhookThread = webhook.Webhook(log_url, self.config_dict, self.autoUploadEnabled)
            self.webhookThread.start()

    def discordStartBtn(self):
        """Creates button to start discord posting"""
        self.btn_startDiscord = QtWidgets.QPushButton('START', self)
        self.btn_startDiscord.setGeometry(4, 576, 65, 20)
        self.btn_startDiscord.setStyleSheet(MwStyle.discordStartBtn())
        self.btn_startDiscord.setIcon(QtGui.QIcon(self.start_icon))
        self.btn_startDiscord.clicked.connect(self.discordStartBtnAction)

        """Creates button to select and change discord server"""
        self.btn_openServerMenu = QtWidgets.QPushButton('^', self)
        self.btn_openServerMenu.setGeometry(70, 576, 10, 20)
        self.btn_openServerMenu.setStyleSheet(MwStyle.discordSelectBtn())
        self.btn_openServerMenu.setToolTip('Select Discord Server')
        self.btn_openServerMenu.clicked.connect(self.openWebhookSelectMenu)

    def webhookSelectMenu(self):
        """Creates Menu for Discord Server selection"""
        self.ui_weebhookBackground = QtWidgets.QListWidget(self)
        self.ui_weebhookBackground.setGeometry(8, 418, 383, 150)
        self.ui_weebhookBackground.setStyleSheet(MwStyle.background())
        self.ui_weebhookBackground.hide()

        """Creates server Table"""
        self.tw_servers = QtWidgets.QTableWidget(self)
        self.tw_servers.setGeometry(12, 422, 375, 118)
        self.tw_servers.setStyleSheet(MwStyle.serverTw())
        self.tw_servers.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)  # disable scroll bars
        self.tw_servers.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tw_servers.verticalHeader().hide()  # disable side headers
        self.tw_servers.setShowGrid(False)  # disable table grid
        self.tw_servers.setSortingEnabled(False)  # disable sorting ability
        self.tw_servers.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)  # select whole row instead of item
        self.tw_servers.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)  # disable multiline selection
        self.tw_servers.setFocusPolicy(QtCore.Qt.NoFocus)  # disable focus border
        self.tw_servers.horizontalHeader().setDisabled(True)  # make top headers unclickable
        self.tw_servers.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # make item uneditable
        self.tw_servers.setAutoScroll(False)  # disable item scrolling
        self.tw_servers.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)  # disable column resize

        """Init basic items such as header"""
        self.tw_servers.setColumnCount(2)
        self.tw_servers.setColumnWidth(0, 100)
        self.tw_servers.setColumnWidth(1, 273)
        self.tw_servers.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('NAME'))
        self.tw_servers.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('URL'))

        """Creates Table spacer"""
        self.tw_servers_spacer = QtWidgets.QListWidget(self)
        self.tw_servers_spacer.setGeometry(112, 423, 1, 116)
        # TODO: Find out how to disable resize function of columns

        """Fills list with items"""
        entries = len(self.config_dict['servers'])
        self.tw_servers.setRowCount(entries)
        if entries > 0:
            i = 0
            for key in self.config_dict['servers']:
                self.tw_servers.setItem(i, 0, QtWidgets.QTableWidgetItem(key))
                self.tw_servers.setItem(i, 1, QtWidgets.QTableWidgetItem(self.config_dict['servers'][key]))
                self.tw_servers.setRowHeight(i, 20)
                i += 1
            if self.config_dict['webhook']['server'] != '-1':
                self.tw_servers.setCurrentCell(int(self.config_dict['webhook']['server']), 0)

        """Creates Add button"""
        self.btn_addServer = QtWidgets.QPushButton('', self)
        self.btn_addServer.setGeometry(321, 544, 20, 20)
        self.btn_addServer.setIcon(QtGui.QIcon(self.add_icon))
        self.btn_addServer.setStyleSheet(MwStyle.addBtn())
        self.btn_addServer.setToolTip('Add server')
        self.btn_addServer.clicked.connect(self.serverMenuAddAction)

        """Creates remove button"""
        self.btn_removeServer = QtWidgets.QPushButton('', self)
        self.btn_removeServer.setGeometry(345, 544, 20, 20)
        self.btn_removeServer.setIcon(QtGui.QIcon(self.remove_icon))
        self.btn_removeServer.setStyleSheet(MwStyle.removeBtn())
        self.btn_removeServer.setToolTip('Remove selected server')
        self.btn_removeServer.clicked.connect(self.serverMenuRemoveAction)

        """Creates select button"""
        self.btn_selectServer = QtWidgets.QPushButton('', self)
        self.btn_selectServer.setGeometry(368, 544, 20, 20)
        self.btn_selectServer.setIcon(QtGui.QIcon(self.select_icon))
        self.btn_selectServer.setStyleSheet(MwStyle.selectBtn())
        self.btn_selectServer.setToolTip('Select selected server')
        self.btn_selectServer.clicked.connect(self.serverMenuSelectAction)

        """Creates name TextBox"""
        self.tb_serverName = QtWidgets.QLineEdit('', self)
        self.tb_serverName.setGeometry(12, 544, 100, 20)
        self.tb_serverName.setPlaceholderText('webhook name')
        self.tb_serverName.setStyleSheet(MwStyle.serverNameTb())

        """Creates url TextBox"""
        self.tb_serverUrl = QtWidgets.QLineEdit('', self)
        self.tb_serverUrl.setGeometry(113, 544, 204, 20)
        self.tb_serverUrl.setPlaceholderText('webhook url')
        self.tb_serverUrl.setStyleSheet(MwStyle.serverUrlTb())

        """Creates clear button"""
        self.delete_url_btn = QtWidgets.QPushButton('X', self)
        self.delete_url_btn.setGeometry(303, 547, 12, 12)
        self.delete_url_btn.setStyleSheet(MwStyle.discordDeleteBtn())
        self.delete_url_btn.clicked.connect(self.serverMenuUrlClearAction)

        """Hide everything on startup"""
        self.tw_servers_spacer.hide()
        self.tw_servers.hide()
        self.btn_addServer.hide()
        self.btn_removeServer.hide()
        self.btn_selectServer.hide()
        self.tb_serverName.hide()
        self.tb_serverUrl.hide()
        self.delete_url_btn.hide()

    def openWebhookSelectMenu(self):
        """Shows/Hides server menu when little arrow button was clicked"""
        if self.ui_weebhookBackground.isVisible():
            self.ui_weebhookBackground.hide()
            self.tw_servers.hide()
            self.tw_servers_spacer.hide()
            self.btn_addServer.hide()
            self.btn_removeServer.hide()
            self.btn_selectServer.hide()
            self.tb_serverName.hide()
            self.tb_serverUrl.hide()
            self.delete_url_btn.hide()
        else:
            self.ui_weebhookBackground.show()
            self.tw_servers.show()
            self.tw_servers_spacer.show()
            self.btn_addServer.show()
            self.btn_removeServer.show()
            self.btn_selectServer.show()
            self.tb_serverName.show()
            self.tb_serverUrl.show()
            self.delete_url_btn.show()
            self.tw_servers.setCurrentCell(int(self.config_dict['webhook']['server']), 0)

    def serverMenuUrlClearAction(self):
        """Handle clear of url textbox in server menu on button click"""
        if self.tb_serverUrl.text() != '':
            self.tb_serverUrl.setText('')

    def serverMenuAddAction(self):
        """Handle add entry in server list"""
        names = []
        for i in range(0, self.tw_servers.rowCount()):
            names.append(self.tw_servers.item(i, 0).text())

        if self.tb_serverName.text() != '' and self.tb_serverUrl.text() != '' and \
                self.tb_serverName.text() not in names:
            row = self.tw_servers.rowCount()
            name = self.tb_serverName.text()
            url = self.tb_serverUrl.text()
            self.tw_servers.setRowCount(row + 1)
            self.tw_servers.setItem(row, 0, QtWidgets.QTableWidgetItem(name))
            self.tw_servers.setItem(row, 1, QtWidgets.QTableWidgetItem(url))
            self.tw_servers.setRowHeight(row, 20)
            self.tb_serverName.setText('')
            self.tb_serverUrl.setText('')

            config.add_server(name, url)
            self.config_dict['servers'][name] = url

    def serverMenuRemoveAction(self):
        """Handle remove entry in server list"""
        if self.tw_servers.currentRow() != -1:
            row = self.tw_servers.currentRow()
            name = self.tw_servers.selectedItems()[0].text()
            url = self.tw_servers.selectedItems()[1].text()
            self.tw_servers.removeRow(self.tw_servers.currentRow())
            config.remove_servers(name)
            del self.config_dict['servers'][name]
            if url == self.config_dict['webhook']['url']:
                config.change_webhook(-1, '')
                self.config_dict['webhook']['server'] = '-1'
                self.config_dict['webhook']['url'] = ''
            if row < int(self.config_dict['webhook']['server']):
                config.change_webhook(int(self.config_dict['webhook']['server']) - 1, 'False')
                self.config_dict['webhook']['server'] = str(int(self.config_dict['webhook']['server']) - 1)

    def serverMenuSelectAction(self):
        """Handle server selection"""
        if self.tw_servers.currentRow() != -1:
            row = self.tw_servers.currentRow()
            url = self.tw_servers.selectedItems()[1].text()
            config.change_webhook(row, url)
            self.config_dict['webhook']['server'] = str(row)
            self.config_dict['webhook']['url'] = url
            self.openWebhookSelectMenu()

    def discordStartBtnAction(self):
        """Handle START-Button action (starting thread and changing button icon/text"""
        if self.btn_startDiscord.text() == 'START':
            self.btn_startDiscord.setText('PAUSE')
            self.btn_startDiscord.setIcon(QtGui.QIcon(self.pause_icon))
            self.autoUploadEnabled = True
        else:
            self.btn_startDiscord.setText('START')
            self.btn_startDiscord.setIcon(QtGui.QIcon(self.start_icon))
            self.autoUploadEnabled = False

    def discordPostBtn(self):
        """Creates manual post button to post selected log or in TextBox (tb_customLink) entered link"""
        self.btn_postSelectedLog = QtWidgets.QPushButton('', self)
        self.btn_postSelectedLog.setGeometry(84, 576, 20, 20)
        self.btn_postSelectedLog.setIcon(QtGui.QIcon(self.discord_icon))
        self.btn_postSelectedLog.setStyleSheet(MwStyle.discordBtn())
        self.btn_postSelectedLog.setToolTip('Post selected log')
        self.btn_postSelectedLog.clicked.connect(self.discordPostBtnAction)

    def discordPostBtnAction(self):
        """Check if TextBox is full, else post selected log from list. Clears TextBox if full"""
        if self.tb_customLink.text() == '' and self.lw_logTable.count() >= 1 and self.lw_logTable.currentRow() >= 0:
            url = self.log_dict[self.lw_logTable.currentRow()]['url']
            self.initPost(url)
        else:
            url = self.tb_customLink.text()
            self.initPost(url)
            self.tb_customLink.setText('')

    def discordPostTB(self):
        """Creates TextBox to enter custom link for discord posting and clear button"""
        self.tb_customLink = QtWidgets.QLineEdit('', self)
        self.tb_customLink.setPlaceholderText('dps.report url')
        self.tb_customLink.setGeometry(94, 576, 230, 20)
        self.tb_customLink.setStyleSheet(MwStyle.discordPostTb())

        self.delete_text_btn = QtWidgets.QPushButton('X', self)
        self.delete_text_btn.setGeometry(310, 579, 12, 12)
        self.delete_text_btn.setStyleSheet(MwStyle.discordDeleteBtn())
        self.delete_text_btn.clicked.connect(self.discordPostDeleteBtnAction)

    def discordPostDeleteBtnAction(self):
        """Called when clear button is pressed. Set TextBox text empty"""
        self.tb_customLink.setText('')

    def openLinkBtn(self):
        """Creates open link in Browser button"""
        self.btn_openSelectedLink = QtWidgets.QPushButton('', self)
        self.btn_openSelectedLink.setGeometry(328, 576, 20, 20)
        self.btn_openSelectedLink.setIcon(QtGui.QIcon(self.open_icon))
        self.btn_openSelectedLink.setStyleSheet(MwStyle.openBtn())
        self.btn_openSelectedLink.setToolTip('Open selected log in browser')
        self.btn_openSelectedLink.clicked.connect(self.openLinkBtnAction)

    def openLinkBtnAction(self):
        """Opens selected log in standard browser"""
        if self.lw_logTable.count() >= 1 and self.lw_logTable.currentRow() >= 0:
            url = self.log_dict[self.lw_logTable.currentRow()]['url']
            if url:
                os.startfile(url)

    def copyLinkBtn(self):
        """Creates copy link from selected log to clipboard button"""
        self.btn_copySelectedLink = QtWidgets.QPushButton('', self)
        self.btn_copySelectedLink.setGeometry(352, 576, 20, 20)
        self.btn_copySelectedLink.setIcon(QtGui.QIcon(self.copy_icon))
        self.btn_copySelectedLink.setStyleSheet(MwStyle.copyBtn())
        self.btn_copySelectedLink.setToolTip('Copy selected log to clipboard')
        self.btn_copySelectedLink.clicked.connect(self.copyLinkBtnAction)

    def copyLinkBtnAction(self):
        """Copies url from selected log to clipboard via command line"""
        if self.lw_logTable.count() >= 1 and self.lw_logTable.currentRow() >= 0:
            url = self.log_dict[self.lw_logTable.currentRow()]['url']
            if url:  # could through exception from line above
                command = 'echo | set /p nul=' + url.strip() + '| clip'
                os.system(command)

    def openSettingsBtn(self):
        """Creates button to open settings"""
        self.btn_openSettings = QtWidgets.QPushButton('', self)
        self.btn_openSettings.setGeometry(376, 576, 20, 20)
        self.btn_openSettings.setStyleSheet(MwStyle.settingsBtn(self.settings_icon))
        self.btn_openSettings.setToolTip('Settings')
        self.btn_openSettings.clicked.connect(self.openSettingsBtnAction)

    def openSettingsBtnAction(self):
        """Opens config folder"""
        path = os.path.realpath('config/')
        os.startfile(path)
        # TODO: Figure out how to implement a settings window (in main window or external) or simple config file
