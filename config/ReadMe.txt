Thank you for using GW2 Upload Tool!

Within this folder you will find another file called settings.ini (generated after first start of this program).
On Windows you should be able to open this file with Windows Editor by simply double clicking it.
Now you can see all settings you can change.

The file is ordered by some headers, such as [explorer]. To edit this file just change the value of a setting after the "=".

Explaination:

[explorer]
path = root folder where logs are saved. Default should work if you havent changed anything within the game
refresh_rate = how often will the program look for new files, number in seconds. if you want to choose decimal use . not ,!
	       3 seconds are default and should be fine. Change to a higher number if the Tool causes lags

[webhook]
server = leave unchanged. For internal use
url = is the current webhook url, should not be changed within this config file (see github documentary)
user_token = is your personal userToken from dps.report. Can be changed but never share!

[servers]
just leave it as it is. For internal url storage of different webhooks

[whitelist]
here you can change which bosses will be posted on discord.
Removing or value change to False will cause no further posting on discord!
Everything else can still be posted manualy by clicking the discord button