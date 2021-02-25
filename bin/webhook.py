from discord_webhook import DiscordWebhook, DiscordEmbed
import math
import datetime
import PyQt5.QtCore as QtCore
import requests


def emojis():
    """define id's for custom discord emojis"""
    return {'player': ':bust_in_silhouette:',
                      'damage': ':crossed_swords:',
                      'quickness': '<:quickness:776075657519693825>',
                      'alacrity': '<:alacrity:776075657159376956>',
                      'might': '<:might:776075657402646568>',
                      'fury': '<:fury:776075657343402024>',
                      'Spellbreaker': '<:warrior_spellbreaker:776075661537574913>',
                      'Berserker': '<:warrior_berserker:776075661785694238>',
                      'Warrior': '<:warrior:776075661559201802>',
                      'Deadeye': '<:thief_deadeye:776075661710065664>',
                      'Daredevil': '<:thief_daredevil:776075661685030923>',
                      'Thief': '<:thief:776075661407158314>',
                      'Renegade': '<:revenant_renegade:776075661516996629>',
                      'Herald': '<:revenant_herald:776075661755547678>',
                      'Revenant': '<:revenant:776075659519983688>',
                      'Soulbeast': '<:ranger_soulbeast:776075661932101632>',
                      'Druid': '<:ranger_druid:776075661575585842>',
                      'Ranger': '<:ranger:776075661331922945>',
                      'Scourge': '<:necro_scourge:776075661722517534>',
                      'Reaper': '<:necro_reaper:776075661516472371>',
                      'Necromancer': '<:necro:776075659864571955>',
                      'Mirage': '<:mirage:776075660111118376>',
                      'Chronomancer': '<:mesmer_chronomancer:776075661751484496>',
                      'Mesmer': '<:mesmer:776075659646205964>',
                      'Firebrand': '<:guardian_firebrand:776075660132352040>',
                      'Dragonhunter': '<:guardian_dragonhunter:776075659574640680>',
                      'Guardian': '<:guardian:776075659763122206>',
                      'Scrapper': '<:engineer_scrapper:776075660010455050>',
                      'Holosmith': '<:engineer_holosmith:776075661512540180>',
                      'Engineer': '<:engineer:776075659000414229>',
                      'Weaver': '<:ele_weaver:776075656986492959>',
                      'Tempest': '<:ele_tempest:776075656928296971>',
                      'Elementalist': '<:ele:776075657095413771>'}


def characters():
    """define unicode characters"""
    return {
        'success': u'\u2714',
        'fail': u'\u2716',
        'healthbar_full': u'\u25B0',
        'healthbar_empty': u'\u25B1',
        'space': u'\u2800'
    }


class Webhook(QtCore.QThread):

    def __init__(self, log_url, config, auto_enabled, parent=None):
        """Thread for discord webhook"""
        QtCore.QThread.__init__(self, parent)
        self.log_url = log_url
        self.wh_url = config['webhook']['url']
        self.boss_list = config['whitelist']
        self.log = {}
        self.emoji = emojis()
        self.chars = characters()
        self.auto_enabled = auto_enabled
        self.name = self.log_url.split('_')[-1]
        self.enabled_bosses = self.get_bosses()

    def run(self):
        """init Thread"""
        self.log = self.get_logDict()
        if (self.auto_enabled and self.name in self.enabled_bosses) or (not self.auto_enabled):
            if 'error' not in self.log:
                self.webhook()

    def get_logDict(self):
        """Fetch further log information"""
        r = requests.post(f'https://dps.report/getJson?permalink={self.log_url}', timeout=10)
        if str(r.status_code) == '200':
            log = r.json()
            return log
        else:
            return {'error': True}

    def get_bosses(self):
        """Get list of enabled bosses"""
        liste = []
        bosses = {'vale guardian': 'vg',
                  'gorseval the multifarious': 'gors',
                  'sabetha the saboteur': 'sab',
                  'slothasor': 'sloth',
                  'bandit trio': 'trio',
                  'matthias gabrel': 'matt',
                  'keep construct': 'kc',
                  'twisted castle': 'tc',
                  'xera': 'xera',
                  'cairn the indomitable': 'cairn',
                  'mursaat overseer': 'mo',
                  'samarog': 'sam',
                  'deimos': 'dei',
                  'soulless horror': 'sh',
                  'river of souls': 'rr',
                  'statues of grenth': 'eyes',
                  'dhuum': 'dhuum',
                  'conjured amalgamate': 'ca',
                  'twin largos': 'twins',
                  'qadim': 'qadim',
                  'cardinal sabir': 'sabir',
                  'cardinal adina': 'adina',
                  'qadim the peerless': 'qpeer'
                  }
        for boss in self.boss_list:
            if self.boss_list[boss].lower() == 'true':
                if boss in bosses:
                    liste.append(bosses[boss])
        return liste

    def webhook(self):
        """configure webhook"""
        webhook = DiscordWebhook(url=self.wh_url, username='DPS Logs')

        """configure webhook header and author"""
        if self.log['success']:
            embed = DiscordEmbed(color=0x00FF00)
            success_author_string = f'{self.log["fightName"]}    ' + self.chars['success']
            embed.set_author(name=success_author_string, url=self.log_url, icon_url=self.log['fightIcon'])
        else:
            embed = DiscordEmbed(color=0xB40404)
            fail_author_string = f'{self.log["fightName"]}    ' + self.chars['fail']
            embed.set_author(name=fail_author_string, url=self.log_url, icon_url=self.log['fightIcon'])

        """configure webhook footer"""
        embed.set_footer(text=f'Recorded by {self.log["recordedBy"]}')
        embed.set_timestamp(timestamp=self.get_time())

        """configure boss info field"""
        embed.add_embed_field(name='> **BOSS INFO**', value=self.get_bossInfo(), inline=False)

        """configure player info field"""
        embed.add_embed_field(name=f'> **PLAYER INFO**\n{self.get_playerInfoHeader()}',
                              value=self.get_playerInfo(), inline=False)

        """configure link info field"""
        embed.add_embed_field(name='> **LINK**', value=self.log_url, inline=False)

        """pack embeds to webhook and send"""
        webhook.add_embed(embed)
        response = webhook.execute()

    def get_time(self):
        """get current time in special format"""
        kill_time = datetime.datetime.strptime(self.log["timeEnd"][0:19], "%Y-%m-%d %H:%M:%S") + \
                    datetime.timedelta(hours=5)
        return int((kill_time - datetime.datetime.utcfromtimestamp(0)).total_seconds())

    def get_bossInfo(self):
        """Create boss info string"""
        log_duration = f'Duration: {self.log["duration"][0:7]}\n'

        if self.log['triggerID'] == 21105:  # Largos
            nikare_perc = round(100 - float(self.log['targets'][0]['healthPercentBurned']), 2)
            nikare = f'**Nikare:**\nHealth: {nikare_perc}%\n'
            nikare_bar = self.get_healthBar(nikare_perc)

            kenut_perc = round(100 - float(self.log['targets'][1]['healthPercentBurned']), 2)
            kenut = f'\n**Kenut:**\nHealth: {kenut_perc}%\n'
            kenut_bar = self.get_healthBar(kenut_perc)

            return log_duration + nikare + nikare_bar + kenut + kenut_bar

        elif self.name == 'eyes':
            fate_perc = round(100 - float(self.log['targets'][0]['healthPercentBurned']), 2)
            fate = f'**Eye of Fate:**\nHealth: {fate_perc}%\n'
            fate_bar = self.get_healthBar(fate_perc)

            judge_perc = round(100 - float(self.log['targets'][1]['healthPercentBurned']), 2)
            judge = f'\n**Eye of Judgement:**\nHealth: {judge_perc}%\n'
            judge_bar = self.get_healthBar(judge_perc)

            return log_duration + fate + fate_bar + judge + judge_bar

        elif self.name == 'trio':
            berg_perc = round(100 - float(self.log['targets'][0]['healthPercentBurned']), 2)
            berg = f'**Berg:**\nHealth: {berg_perc}%\n'
            berg_bar = self.get_healthBar(berg_perc)

            zane_perc = round(100 - float(self.log['targets'][1]['healthPercentBurned']), 2)
            zane = f'\n**Zane:**\nHealth: {zane_perc}%\n'
            zane_bar = self.get_healthBar(zane_perc)

            narella_perc = round(100 - float(self.log['targets'][2]['healthPercentBurned']), 2)
            narella = f'\n**Narella:**\nHealth: {narella_perc}%\n'
            narella_bar = self.get_healthBar(narella_perc)

            return log_duration + berg + berg_bar + zane + zane_bar + narella + narella_bar

        else:
            boss_perc = round(100 - float(self.log['targets'][0]['healthPercentBurned']), 2)
            boss_health = f'Health: {boss_perc}%\n'
            boss_bar = self.get_healthBar(boss_perc)

            return log_duration + boss_health + boss_bar

    def get_healthBar(self, percentage):
        """Create healthbar"""
        length = 25
        number = length * percentage / 100
        full_brackets = math.ceil(number)
        empty_brackets = length - full_brackets

        return self.chars['healthbar_full'] * full_brackets + self.chars['healthbar_empty'] * empty_brackets

    def get_playerInfoHeader(self):  # else to many characters in player string
        """Create 'PLAYER INFO' Header"""
        s = self.chars['space']
        header = f'{s * 2}{self.emoji["player"]}{s * 14}{self.emoji["damage"]}{s * 3} {self.emoji["quickness"]}' \
                 f'{s * 3} {self.emoji["alacrity"]}{s * 4}{self.emoji["fury"]} {s * 3} {self.emoji["might"]}\n'

        return header

    def get_playerInfo(self):
        """Fetch all infos from json (boons, dps, profession, etc.)"""
        info = {}
        quickness, alacrity, might, fury = 0.0, 0.0, 0.0, 0.0
        for i in range(len(self.log['players'])):  # fetching info of all players
            if self.log["players"][i]["name"] != 'Conjured Sword':  # filter ca-swords from players
                name = self.log["players"][i]["name"]  # get name of character
                profession = self.log["players"][i]["profession"]  # get profession of character

                if self.name in ("twins", "eyes"):  # get dps if more than one boss
                    dps = self.log["players"][i]["dpsTargets"][0][0]['dps'] + \
                          self.log["players"][i]["dpsTargets"][1][0]['dps']

                elif self.name == 'trio':
                    dps = self.log["players"][i]["dpsTargets"][0][0]['dps'] + \
                          self.log["players"][i]["dpsTargets"][1][0]['dps'] + \
                          self.log["players"][i]["dpsTargets"][2][0]['dps']

                else:
                    dps = self.log["players"][i]["dpsTargets"][0][0]['dps']  # get dps on single boss encounters

                for j in range(len(self.log["players"][i]['buffUptimes'])):  # fetch quickness data
                    if self.log["players"][i]['buffUptimes'][j]['id'] == 1187:
                        quickness = self.log["players"][i]['buffUptimes'][j]['buffData'][0]['uptime']
                        break
                for j in range(len(self.log["players"][i]['buffUptimes'])):  # fetch alacrity data
                    if self.log["players"][i]['buffUptimes'][j]['id'] == 30328:
                        alacrity = self.log["players"][i]['buffUptimes'][j]['buffData'][0]['uptime']
                        break
                for j in range(len(self.log["players"][i]['buffUptimes'])):  # fetch might data
                    if self.log["players"][i]['buffUptimes'][j]['id'] == 740:
                        might = self.log["players"][i]['buffUptimes'][j]['buffData'][0]['uptime']
                        break
                for j in range(len(self.log["players"][i]['buffUptimes'])):
                    if self.log["players"][i]['buffUptimes'][j]['id'] == 725:  # fetch fury data
                        fury = self.log["players"][i]['buffUptimes'][j]['buffData'][0]['uptime']
                        break

                info[name] = {'dps': dps, 'profession': profession, 'quickness': quickness, 'alacrity': alacrity,
                              'fury': fury, 'might': might}  # store player data in dictionary

        player_list = sorted(info, key=lambda x: info[x]['dps'], reverse=True)

        player_string = ''
        for name in player_list:  # circle through sorted players
            profession = info[name]['profession']
            dps = str(info[name]['dps'])
            quickness = '{0:.2f}%'.format(round(info[name]['quickness'], 2)) \
                if info[name]['quickness'] >= 10 else '{0:.2f}%'.format(round(info[name]['quickness'], 2))
            alacrity = '{0:.2f}%'.format(round(info[name]['alacrity'], 2)) \
                if info[name]['quickness'] >= 10 else '{0:.2f}%'.format(round(info[name]['alacrity'], 2))
            might = '{0:.2f}'.format(round(info[name]['might'], 2)) \
                if info[name]['quickness'] >= 10 else '{0:.2f}'.format(round(info[name]['might'], 2))
            fury = '{0:.2f}%'.format(round(info[name]['fury'], 2)) \
                if info[name]['quickness'] >= 10 else '{0:.2f}%'.format(round(info[name]['fury'], 2))

            player_string += self.emoji[profession] + '`' \
                             + name + (' ' * (21 - len(name) + 5 - len(dps))) \
                             + dps + (' ' * (8 - len(quickness))) \
                             + quickness + (' ' * (8 - len(alacrity))) \
                             + alacrity + (' ' * (8 - len(fury))) \
                             + fury + (' ' * (7 - len(might))) \
                             + might + ' ' + '`\n'  # format info string
        return player_string
