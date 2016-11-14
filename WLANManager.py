"""
Author:			Manas Oswal @manas99 (github)
License:		MIT License
File name:		WLANManager.py
Description:	Scripts for getting  WLAN information on windows
Language:		Python
"""
import subprocess
import math

"""
type:		 function
name:		 percentTodBm
params:		 1 (int)
description: Converts the the signal strength from percent to dBm.
return-type: int
"""
def percentTodBm(pc):
	dBm = (pc/2) -100
	return dBm


"""
type:		 function
name:		 dBmToPercent
params:		 1 (int)
description: Converts the the signal strength from dBm to percent.
return-type: int
"""
def dBmToPercent(dBm):
	pc = 2*(dBm + 100)
	return pc


"""
type:		 class
name:	 	 WLANManager
description: WLAN Manager; To get all SSIDs, etc. using windows cmd commands.
"""
class WLANManager:
	'Wireless LAN Manager.'

"""
type:		 function
name:		 getWLANList
params:		 null
description: Gets all details abour all the available WLANs
return-type: array of objects
"""
	def getWLANList(self):
		if self.checkWLANState() == 1:
			results = self.getResponseStr()
			wifi_list = []
			for ssid in results:
				fin_ssid = {}
				ssid = ssid.split("\n")
				fin_ssid["ssid"] = ssid[0].replace(" ", "").split(":")[1]
				fin_ssid["signal_percent"] = float(ssid[5].replace(" ", "").split(":")[1].replace("%", ""))
				fin_ssid["signal_dBm"] = percentTodBm(fin_ssid["signal_percent"])
				fin_ssid["bssid"] = ssid[4].replace(" ", "").split("BSSID1:")[1]
				fin_ssid["network_type"] = ssid[1].replace(" ", "").split(":")[1]
				fin_ssid["authentication"] = ssid[2].replace(" ", "").split(":")[1]
				fin_ssid["encryption"] = ssid[3].replace(" ", "").split(":")[1]
				fin_ssid["radio_type"] = ssid[6].replace(" ", "").split(":")[1]
				fin_ssid["channel"] = ssid[7].replace(" ", "").split(":")[1]
	
				if fin_ssid["radio_type"] == "802.11a" :
					fin_ssid["frequency_GHz"] = 5
		
				if fin_ssid["radio_type"] == "802.11b" or fin_ssid["radio_type"] == "802.11g" :
					fin_ssid["frequency_GHz"] = 2.4
		
				if fin_ssid["radio_type"] == "802.11n":
					channel_list_5GHz = ["36", "38", "40", "42", "44", "46", "48", "52", "56", "60", "64", "100", "104", "108", "112", "116", "120", "124", "128", "132", "136", "140", "149", "153", "157", "161", "165"]
					if fin_ssid["channel"] in channel_list_5GHz:
						fin_ssid["frequency_GHz"] = 5
					else:
						fin_ssid["frequency_GHz"] = 2.4
	
				wifi_list.append(fin_ssid)
			
			return wifi_list
		else:
			return self.checkWLANState()

			
"""
type:		 function
name:		 getWLANBySSID
params:		 ssid (str)
description: Gets all details abour a specific WLAN network specified by ssid
return-type: none if not found else object
"""
	def getWLANBySSID(self, ssid):
		if self.checkWLANState() == 1:
			list = self.getWLANList()
			for x in list:
				if x["ssid"] == ssid:
					return x
		else:
			return self.checkWLANState()

"""
type:		 function
name:		 getSSIDList
params:		 null
description: Gets a list of all the available SSIDs
return-type: array
"""
	def getSSIDList(self):
		if self.checkWLANState() == 1:
			list = self.getWLANList()
			ret_list = []
			for x in list:
				ret_list.append(x["ssid"])
			return ret_list
		else:
			return self.checkWLANState()

"""
type:		 function
name:		 checkWLANState
params:		 null
description: checks the state of the WLAN adapter
return-type: 1 if adapter working else str which describes the error
"""
	def checkWLANState(self):
		try:
			ret = subprocess.check_output(["netsh", "wlan", "show", "network", "mode=Bssid"])
			return 1
		except subprocess.CalledProcessError as e:
			return e.output.decode("ascii").replace("\r\n\r\n\r\n","")

"""
type:		 function
name:		 getResponseStr
params:		 null
description: executes the cmd command and returns the output in a formatted array
return-type: array
"""			
	def getResponseStr(self):
		if self.checkWLANState() == 1:
			ret = subprocess.check_output(["netsh", "wlan", "show", "network", "mode=Bssid"])
			ret = ret.decode("ascii") # needed in python 3

			ret = ret.replace("\r","")
			ret = ret.replace("\t","")
			ret = ret.split("\nSSID")
			del ret[0]
			return ret
		else:
			return self.checkWLANState()
	