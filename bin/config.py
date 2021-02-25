import configparser
import requests
import os


def checkSettings():
    """Checks if settings file already exist. Else creates new settings file with default values"""
    if os.path.exists('config/settings.ini'):
        pass
    else:
        createSettingsFile()


def createSettingsFile():
    """Creates new settings file in /config/settings.ini with default values"""
    refresh_rate = 3  # default refresh rate for log lookup in seconds

    try:
        r = requests.get('https://dps.report/getUserToken', timeout=3)  # requests user token from dps.report
        if r.status_code == 200:
            user_token = r.json()['userToken']
        else:
            user_token = 'None'
    except:
        user_token = ''

    with open('config/settings.ini', 'w') as cfg_file:
        cfg = configparser.ConfigParser()

        """Explorer settings"""
        cfg.add_section('explorer')
        default_path = f'C:\\Users\\{os.getlogin()}\\Documents\\Guild Wars 2\\addons\\arcdps\\arcdps.cbtlogs'
        cfg.set('explorer', 'path', default_path)
        cfg.set('explorer', 'refresh_rate', str(refresh_rate))

        """Discord Webhook settings"""
        cfg.add_section('webhook')
        cfg.set('webhook', 'server', '-1')
        cfg.set('webhook', 'url', '')
        cfg.set('webhook', 'user_token', user_token)
        cfg.add_section('servers')

        """Bosses for posting settings"""
        cfg.add_section('whitelist')

        cfg.set('whitelist', 'Vale Guardian', 'True')
        cfg.set('whitelist', 'Gorseval the Multifarious', 'True')
        cfg.set('whitelist', 'Sabetha the Saboteur', 'True')

        cfg.set('whitelist', 'Slothasor', 'True')
        cfg.set('whitelist', 'Bandit Trio', 'True')
        cfg.set('whitelist', 'Matthias Gabrel', 'True')

        cfg.set('whitelist', 'Keep Construct', 'True')
        cfg.set('whitelist', 'Twisted Castle', 'True')
        cfg.set('whitelist', 'Xera', 'True')

        cfg.set('whitelist', 'Cairn the Indomitable', 'True')
        cfg.set('whitelist', 'Mursaat Overseer', 'True')
        cfg.set('whitelist', 'Samarog', 'True')
        cfg.set('whitelist', 'Deimos', 'True')

        cfg.set('whitelist', 'Soulless Horror', 'True')
        cfg.set('whitelist', 'River of Souls', 'True')
        cfg.set('whitelist', 'Statues of Grenth', 'True')
        cfg.set('whitelist', 'Dhuum', 'True')

        cfg.set('whitelist', 'Conjured Amalgamate', 'True')
        cfg.set('whitelist', 'Twin Largos', 'True')
        cfg.set('whitelist', 'Qadim', 'True')

        cfg.set('whitelist', 'Cardinal Sabir', 'True')
        cfg.set('whitelist', 'Cardinal Adina', 'True')
        cfg.set('whitelist', 'Qadim the Peerless', 'True')

        """Flush settings to file"""
        cfg.write(cfg_file)


def read_settings():
    """Reading config file and reformatting from configparser-object to dic"""
    config = configparser.ConfigParser()
    config.read('config/settings.ini')
    config_dict = {}
    for section in config.sections():  # convert configparser-object to dictionary
        config_dict[section] = dict(config[section])
    return config_dict


def remove_servers(name):
    """Remove deleted webhooks"""
    cfg = configparser.ConfigParser()
    cfg.read('config/settings.ini')
    cfg.remove_option('servers', name)
    with open('config/settings.ini', 'w') as cfg_file:
        cfg.write(cfg_file)


def add_server(name, url):
    """Add new webhooks"""
    cfg = configparser.ConfigParser()
    cfg.read('config/settings.ini')
    cfg.set('servers', name, url)
    with open('config/settings.ini', 'w') as cfg_file:
        cfg.write(cfg_file)


def change_webhook(row, url):
    """Change existing webhook"""
    cfg = configparser.ConfigParser()
    cfg.read('config/settings.ini')
    cfg.set('webhook', 'server', str(row))
    if url != 'False':
        cfg.set('webhook', 'url', url)
    with open('config/settings.ini', 'w') as cfg_file:
        cfg.write(cfg_file)
