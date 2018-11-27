### Script by Tudor Ciolac ###
### Written October 2018 ###

#!/usr/bin/env python3
import math
import time
import requests
import os.path
import re
import getpass

##### Declarations #####

epochtime = str(int(math.floor(time.time())))

class credCollect:
	def __init__(self,sourceFile, cust, aUsername, aPassword, option, aDuration, aBackup, lineCount):
		self.sourceFile = sourceFile
		self.destFile = destFile
		self.cust = cust
		self.aUsername = aUsername
		self.aPassword = aPassword
		self.option = option
		self.aDuration = aDuration
		self.aBackup = aBackup
		self.lineCount = lineCount

def grabCredentials():
	eventCounter = 0
	while eventCounter == 0:
		credCollect.sourceFile = input("Source File Path: ")
		if os.path.isfile(credCollect.sourceFile):
			getLineCount()
			eventCounter = 1
		else:
			print ("No such file exists, please enter a valid file:")
			eventCounter = 0;

	while eventCounter == 1:
		credCollect.cust = input("Cluster (a/b): ")
		if credCollect.cust.lower() != 'a' and credCollect.cust.lower() != 'b':
			print("Invalid Input")
			eventCounter = 1
		else:
			eventCounter = 2
	while eventCounter == 2:
		credCollect.aUsername = input("Your admin username: ")
		if '@' not in credCollect.aUsername and '.' not in credCollect.aUsername:
			print ("Invalid Input, proper format is admin@domain.tld")
			eventCounter = 2
		else:
			eventCounter = 3
	while eventCounter == 3:	
		credCollect.aPassword = getpass.getpass("Your admin password: ")
		loginBool = checkLogin()
		if loginBool == True:
			eventCounter = 4
		else:
			print ("Invalid Username/Password. Please try again.")
			return
	while eventCounter == 4:
		credCollect.option = input("Single Sign On (24 hours) or Long Term Token? Desired Input: SSO/Token: ")
		if credCollect.option.lower() != 'sso' and credCollect.option.lower() != 'token':
			print ("Invalid Input, Desired Input: SSO/Token")
		else:
			if credCollect.option.lower() == 'sso':
				credCollect.option = True
				credCollect.aDuration = '24'
				eventCounter = 6
			else:
				credCollect.option = False
				credCollect.aBackup = False
				eventCounter = 5
	while eventCounter == 5:
		credCollect.aDuration = input("Token Duration in hours: ")
		try:
			int(credCollect.aDuration) + 1
		except ValueError:
			print ("Invalid Input, must enter a numerical value between 1-744")
		else:
			if int(credCollect.aDuration) <= 0 or int(credCollect.aDuration) >= 755:
				print ("Invalid Input, must enter a numerical value between 1-744")
				eventCounter = 5
			else:
				credCollect.aDuration = str(credCollect.aDuration)
				storeValues()
				return
	while eventCounter == 6:
		if credCollect.option != False:
			credCollect.aBackup = input("Secondary SSOs?: ").lower()[0]
			if credCollect.aBackup != 'y' and credCollect.aBackup != 'n':
				print("Invalid Input, acceptable input is y or n")
				eventCounter = 6
			else:
				if credCollect.aBackup == 'y':
					credCollect.aBackup = True
					storeValues()
					return
				else:
					credCollect.aBackup = False
					storeValues()
					return
def checkLogin():
	data ='{"credentials": {"user":"' + credCollect.aUsername + '","password":"' + credCollect.aPassword + '"},"generate_session_token":true}'
	response = requests.post('https://admin.' + credCollect.cust + '.hostedemail.com/api/authenticate', data=data)
	if '"success":true,' in str(response.text):
		return True
	elif '"success":true,' not in str(response.text):
		return False

def sendRequest(lineItem):
	if credCollect.option == True:
		#sso
		data ='{"credentials": {"user":"' + credCollect.aUsername + '","password":"' + credCollect.aPassword + '"},"user":"' + lineItem + '","type":"sso","reason":"Migration"}'
	else: 
		#token
		data ='{"credentials": {"user":"' + credCollect.aUsername + '","password":"' + credCollect.aPassword + '"},"user":"' + lineItem + '","type":"session","duration":"' + credCollect.aDuration + '","reason":"Migration"}'
	response = requests.post('https://admin.' + credCollect.cust + '.hostedemail.com/api/generate_token', data=data)
	return (str(response.text))

def getLineCount():
	with open(credCollect.sourceFile) as f:
		credCollect.lineCount = (len(f.readlines()))
	return

def storeValues():
	createFile()
	firstLine()
	lineCount = 0
	requestResult = ""
	requestResult2 = ""
	value = ""
	value2 = ""
	credCollect.currLine = ""
	with open(credCollect.sourceFile) as f:
		for line in f:
			if lineCount <= credCollect.lineCount:
				lineCount = lineCount + 1
				requestResult = str(sendRequest((line).replace("\n","")))
				if '"success":true' in requestResult:
					value = re.search('"token":"(.*?)", "audit"', requestResult)
					if credCollect.aBackup == True:
						requestResult2 = str(sendRequest((line).replace("\n","")))
						value2 = re.search('"token":"(.*?)", "audit"', requestResult2)
				else:
					value = re.search('"error":"(.*?)", "audit"', requestResult)
					if credCollect.aBackup == True:
						requestResult2 = str(sendRequest((line).replace("\n","")))
						value2 = re.search('"error":"(.*?)", "audit"', requestResult2)					
				if credCollect.aBackup == True:
					writeLine("\n" + ((line).replace("\n","") + "," + value.group(1) + "," + value2.group(1)).replace("\n",""))
					print (("Generating for: " + str(line)).replace("\n","") + "... " + str(math.floor((lineCount/credCollect.lineCount)*100)) + "% Completed\n", end="", flush=True)
				else:
					writeLine("\n" + ((line).replace("\n","") + "," + value.group(1)).replace("\n",""))
					print (("Generating for: " + str(line)).replace("\n","") + "... " + str(math.floor((lineCount/credCollect.lineCount)*100)) + "% Completed\n", end="", flush=True)

def firstLine():
	#Select Data
	if credCollect.aBackup == True:
		credCollect.destFile.write ("Domain,Token/SSO #1,Token/SSO #2")
		counter = 1;
	else:
		credCollect.destFile.write ("Domain,Token/SSO")
		counter = 0;

def createFile():
	credCollect.destFile = open(epochtime + ".results.csv" , "x")

def writeLine(contents):
	credCollect.destFile.write (contents)

##### Script Begins #####

grabCredentials()
