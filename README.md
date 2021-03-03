# GW2 Upload Tool for ArcDPS

## Overview
**-> WARNING: This is a pre-release! Errors can occure! Please report crashes and bugs via GitHub, thank you!<-**

**-> Tool may be shown as untrusted File by AntiVirus <-**

![Overview](/images/overview.png)

1. Boss name and status
2. Log time
3. Enable/Disable automatic posting (only works when a webhook is set up! See below)
4. Open Webhook Menu
5. Post selected log if 6. is empty, else post log entered in 6.
6. Enter manual dps.report url to post on discord
7. Open selected log in your browser (via dps.report)
8. Copy log url to Windows clipboard
9. Open Settings folder

## Example
![Discord Example](/images/discord.png)

## Requirements
* Windows 10
* Latest ArcDPS build from here: [Deltaconnected](https://www.deltaconnected.com/arcdps/x64/)
* Latest Guild Wars 2 build
## How to install
1. Download .zip folder from here: [Download](https://github.com/Jatzelberger/gw2-upload-tool/releases)
2. Extract **ALL** files to a folder you wish (eg. .../desktop/uploadtool/)
3. Open _UploadTool.exe_
4. Read [How to set up](https://github.com/Jatzelberger/gw2-upload-tool#how-to-set-up)
5. You can create a shortcut to your desktop by rightclicking on _UploadTool.exe_ -> _Send to_ -> _Desktop_
## How to set up
**ArcDPS Setup:**
1. Within GW2, open your ArcDPS config via ALT+SHIFT+T
2. Navigate to _LOGGING_ and enable as shown below:

![LOGGING Settings](/images/logging_settings.png)

**Important:** _compress logs with PowerShell (Win10)_ has to be enabled!

**Webhook Setup:**
1. Open the server you want to post your logs onto
2. Open _Server Settings_ and go to _Integration_
3. Now you click on _WebHooks_ and _Create new WebHook_
4. (Name doesnt matter since it will be overwritten anyways. Just for server-audit identification)
5. Select a channel you want to post your logs to
6. Now click on _copy WebHook URL_
7. Open Upload Tool with double-click on _UploadTool.exe_
8. Click on the small arrow next to _START_. It should open a small menu
9. Now enter a webhook name to identify your server and copy your webhook url inside the corresponding text field
10. Click **+** button to add this server to the server list
11. (Repeat as many servers as you want)
12. To select a server just click on its name and press the green arrow button to select it for posting

**Boss Whitelist Setup:**
1. Within Upload Tool, click on the small gear in the bottom right corner (explorer window should be open)
2. Double click on _settings.ini_
3. under _[whitelist]_ you can disable automatic posting by settings value from _True_ to _False_
4. changes need a restart of Upload Tool!
5. Currently, only Raids are supported by automatic posting. Link generation works with every boss! Formatting of Discord message could look weird with everything else

## TODO
- [ ] Redo BossView from two lists to one table (bugs occure when to many logs are listed)
- [ ] Fix: _statue of Fate_ is shown as _Dhuum_
- [ ] Add support for uncompressed .evtc files
- [ ] Add support for fractals and strike missions
- [ ] Fix icon bugs when Windows Scale is above 100%

## FAQ
**Is it safe to use?**

There should be no problem using Upload Tool, but I can not guarantee for anything!


**Why is it 90MB?**

Since its written in Python is has to be shipped with a compiler to work on any pc


**Any questions, bugs or requests?**

Ask me on GitHub or ingame via _NightElf.8624_
