"""
CSS-Styles for MainWindow called by PyQT
Feel free to edit (Basic CSS)
"""


def window():
    """CSS style of main window properties"""
    style = """
        QMainWindow {
            background-color: rgb(25, 25, 26);
        }

        QToolTip {
            background-color: rgb(46, 46, 46);
            color: white;
            font-weight: bold;
            border: 0px;
        }
        """
    return style


def icon(icon_path):
    """CSS style of window icon"""
    style = f"""
        QListView {{
            background-color: rgb(25, 25, 26);
            border: 0px;
            background-image: url("{icon_path}");
            background-size: auto;
        }}
        """
    return style


def background():
    """CSS style of main window background"""
    style = """
        QListView {
            background-color: rgb(40, 40, 42);
            border: 0px
        }

        QToolTip {
            background-color: rgb(46, 46, 46);
            color: white;
            border: 0px;
        }
        """
    return style


def closeBtn():
    """CSS style of window close button"""
    style = """
        QPushButton {
            border: 0px; 
            border-radius: 10px; 
            background-color: rgb(176, 46, 63);
        } 
    
        QPushButton:hover:!pressed {
            background-color: rgb(143, 41, 55);
        }
        """
    return style


def minimizeBtn():
    """CSS style of window minimize button"""
    style = """
    QPushButton {
        border: 0px; 
        border-radius: 10px; 
        background-color: rgb(207, 156, 45)
    } 

    QPushButton:hover:!pressed {
        background-color: rgb(166, 121, 25)
    }
    """
    return style


def infoBtn():
    style = """
    QPushButton {
        border: 0px; 
        border-radius: 10px; 
        background-color: rgb(93, 184, 75)
    } 

    QPushButton:hover:!pressed {
        background-color: rgb(60, 138, 44)
    }
    """
    return style


def logTable():
    style = """
    QListWidget {
        background-color: rgb(70, 70, 70); 
        border: 0px black;
        border-style: solid;
        border-top-left-radius: 0px;
        border-top-right-radius: 0px;
        border-bottom-left-radius: 5px;
        border-bottom-right-radius: 0px;
        font-size: 13px;
    }
    
    QListWidget::item {
        color: white;
        font-weight: bold;
    }
    
    QListWidget::item:selected {
        background: rgb(40, 40, 40); 
        color: white;
        border: 0px black;
    }
    
    QListWidget::item:hover {
        background: rgb(55, 55, 55); 
        color: white;
        border: 0px black;
    }
    """
    return style


def logTableTitle():
    style = """
    QLabel {
        color: white;
        font-weight: bold;
        background-color: rgb(70, 70, 70);
        border-top-left-radius: 5px;
        border-top-right-radius: 0px;
        border-bottom-left-radius: 0px;
        border-bottom-right-radius: 0px;
    }
    """
    return style


def timeTable():
    style = """
    QListWidget {
        background-color: rgb(70, 70, 70); 
        border: 0px black;
        border-style: solid;
        border-top-left-radius: 0px;
        border-top-right-radius: 0px;
        border-bottom-left-radius: 0px;
        border-bottom-right-radius: 5px;
        font-size: 13px;
    }
    
    QListWidget::item {
        color: white;
        font-weight: bold;
    }
    
    QListWidget::item:selected {
        background: rgb(70, 70, 70); 
        color: white;
        border: 0px black;
    }
    
    QListWidget::item:hover {
        background: rgb(70, 70, 70); 
        color: white;
        border: 0px black;
    }
    
    QListWidget::hover {
        background: rgb(70, 70, 70); 
        border: 0px black;
    }

    """
    return style


def timeTableTitle():
    style = """
    QLabel {
        color: white;
        font-weight: bold;
        background-color: rgb(70, 70, 70);
        border-top-left-radius: 0px;
        border-top-right-radius: 5px;
        border-bottom-left-radius: 0px;
        border-bottom-right-radius: 0px;
    }
    """
    return style


def discordStartBtn():
    style = """
            QPushButton {
                border: 0px; 
                border-top-left-radius: 10px;
                border-top-right-radius: 0px;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 0px;
                background-color: rgb(207, 156, 45);
                font-weight: bold;
            } 

            QPushButton:hover:!pressed {
                background-color: rgb(166, 121, 25);
            }
            """
    return style


def discordSelectBtn():
    style = """
            QPushButton {
                border: 0px; 
                border-top-left-radius: 0px;
                border-top-right-radius: 10px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 10px;
                background-color: rgb(207, 156, 45);
                font-weight: bold;
            } 

            QPushButton:hover:!pressed {
                background-color: rgb(166, 121, 25);
            }
            """
    return style


def settingsBtn(icon_path):
    style = f"""
    QPushButton {{
        border: 0px; border-radius: 10px; 
        background-color: rgb(100, 100, 100);
        background-image: url("{icon_path}");
        background-position: center;
        background-size: 50%;
    }}
    
    QPushButton:hover:!pressed {{
        background-color: rgb(70, 70, 70)
    }}
    """
    return style


def discordBtn():
    style = """
    QPushButton {
        border: 0px; border-radius: 10px; 
        background-color: rgb(100, 100, 100);
    } 

    QPushButton:hover:!pressed {
        background-color: rgb(70, 70, 70)
    }
    """
    return style


def openBtn():
    style = """
    QPushButton {
        border: 0px; border-radius: 10px; 
        background-color: rgb(100, 100, 100);
    } 

    QPushButton:hover:!pressed {
        background-color: rgb(70, 70, 70)
    }
    """
    return style


def copyBtn():
    style = """
    QPushButton {
        border: 0px; border-radius: 10px; 
        background-color: rgb(100, 100, 100);
    } 

    QPushButton:hover:!pressed {
        background-color: rgb(70, 70, 70)
    }
    """
    return style


def discordPostTb():
    style = """
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
    QLineEdit {
        border-top-left-radius: 0px;
        border-top-right-radius: 10px;
        border-bottom-left-radius: 0px;
        border-bottom-right-radius: 10px;
        padding-left: 12px
    }
    """
    return style


def discordDeleteBtn():
    style = """
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
    QPushButton {
        border: 0px; border-radius: 6px; 
        background-color: white;
        font-family: 'Bebas Neue', cursive;
        font-weight: bold;
    }
    QPushButton:hover:!pressed {
        background-color: rgb(224, 224, 224);
    }
    """
    return style


def serverTw():
    style = """
    QTableWidget{
        background: rgb(70, 70, 70);
        color: white;
    }
    
    QTableWidget::item:selected{
        background: rgb(40, 40, 40);
        color: white;
    }
    
    QHeaderView::section {
        background: rgb(70, 70, 70);
        color: white;
        border: 0px;
        font-weight: bold;
    }
    
    """
    return style


def addBtn():
    style = """
    QPushButton {
        border: 0px; border-radius: 10px; 
        background-color: rgb(100, 100, 100);
    } 

    QPushButton:hover:!pressed {
        background-color: rgb(70, 70, 70)
    }
    """
    return style


def removeBtn():
    style = """
    QPushButton {
        border: 0px; border-radius: 10px; 
        background-color: rgb(100, 100, 100);
    } 

    QPushButton:hover:!pressed {
        background-color: rgb(70, 70, 70)
    }
    """
    return style


def selectBtn():
    style = """
    QPushButton {
        border: 0px; border-radius: 10px; 
        background-color: rgb(93, 184, 75);
    } 

    QPushButton:hover:!pressed {
        background-color: rgb(60, 138, 44)
    }
    """
    return style


def serverNameTb():
    style = """
    QLineEdit {
        border-top-left-radius: 10px;
        border-top-right-radius: 0px;
        border-bottom-left-radius: 10px;
        border-bottom-right-radius: 0px;
        padding-left: 4px
    }
    """
    return style


def serverUrlTb():
    style = """
    QLineEdit {
        border-top-left-radius: 0px;
        border-top-right-radius: 10px;
        border-bottom-left-radius: 0px;
        border-bottom-right-radius: 10px;
        padding-left: 4px
    }
    """
    return style

