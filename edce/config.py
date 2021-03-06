import sys
if sys.version_info.major < 3:
	print("You need to use Python 3.x, e.g. python3 <filename>")
	exit()

import configparser
import getpass
import edce.error
import os

ConfigFilename = 'edce.ini'
Config = configparser.RawConfigParser()
Config.read(ConfigFilename)

def checkMissingPaths(config):
	if not config.has_section('paths'):
		config.add_section('paths')

	if not config.has_section('paths') or not config.has_option('paths','cookie_file'):
		config.set('paths','cookie_file', os.path.join(".", "cookies.txt"))

	if not config.has_option('paths','time_file'):
		config.set('paths','time_file', os.path.join(".", "last.time"))

	if not config.has_option('paths','last_file'):
		config.set('paths','last_file', os.path.join(".", "last.json"))

def setConfigFile(configFilename):
	global Config
	global ConfigFilename

	ConfigFilename = configFilename
	Config = configparser.RawConfigParser()
	Config.read(configFilename)

def ConfigSectionMap(section):
	dict1 = {}
	try:
		options = Config.options(section)
		for option in options:
			try:
				dict1[option] = Config.get(section, option)
				if dict1[option] == -1:
					DebugPrint("skip: %s" % option)
			except:
				print("exception on %s!" % option)
				dict1[option] = None
				raise edce.error.ErrorConfig('Please run client-setup.py to generate the configuration file.')
	except:
		raise edce.error.ErrorConfig('Please run client-setup.py to generate the configuration file.')
	return dict1

def getString(section, key):
	res = ''
	try:
		res = edce.config.ConfigSectionMap(section)[key]
	except:
		raise edce.error.ErrorConfig('Please run client-setup.py to generate the configuration file.')	
	return res
	
def performSetup():

	print("Enter your Frontier Store credentials here. You can leave your username or password empty, however you will be prompted every time you run the edce_client.py script.")
	username = input("Frontier Store Username: ").strip()
	password = getpass.getpass('Frontier Store Password: ').strip()
	enableEDDNInput = input("Send market data to EDDN. No private information is sent. [Y/n]: ").strip().lower()
		
	enableEDDN = enableEDDNInput == '' or enableEDDNInput == 'y'

	writeConfig(username, password, enableEDDN)

	print("Setup complete. {0} written.".format(ConfigFilename))
	print("**NOTE: Your username and password are not stored encrypted. Make sure this file is protected.")

def writeConfig(username, password, enableEDDN, cookieFilePath = ".", timeFilePath = ".", lastJSONPath = "."):
	global ConfigFilename

	Config = configparser.RawConfigParser()

	Config.add_section('login')
	Config.set('login','username',username)
	Config.set('login','password',password)

	Config.add_section('urls')
	Config.set('urls','url_login','https://companion.orerve.net/user/login')
	Config.set('urls','url_verification','https://companion.orerve.net/user/confirm')
	Config.set('urls','url_profile','https://companion.orerve.net/profile')
	Config.set('urls','url_eddn','http://eddn-gateway.elite-markets.net:8080/upload/')

	Config.add_section('preferences')
	Config.set('preferences','enable_eddn','Yes' if enableEDDN else 'No')

	Config.add_section('paths')
	Config.set('paths','cookie_file', os.path.join(cookieFilePath, "cookies.txt"))
	Config.set('paths','time_file', os.path.join(timeFilePath, "last.time"))
	Config.set('paths','last_file', os.path.join(lastJSONPath, "last.json"))

	with open(ConfigFilename,'w') as cfgfile:
		Config.write(cfgfile)

	setConfigFile(ConfigFilename)

checkMissingPaths(Config)
