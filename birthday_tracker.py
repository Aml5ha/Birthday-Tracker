import re
import csv
from datetime import date
from bs4 import BeautifulSoup

#global vars
monthToDigit = { 'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06', 'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12' }
namesOfPeople = {}
todaysDate = date.today().strftime("%m/%d/%y")

def getNames(fileName):
	try:
		namesFile = open(fileName, 'r')
		for name in namesFile:
			name = name.strip()
			if(name != ''):
				namesOfPeople[name] = ""
		namesFile.close()
	except FileNotFoundError:
		print("File '" + fileName + "' not found")



def populateBirthdayDict(fileName, getAll):
	url = fileName
	page = open(url)
	soup = BeautifulSoup(page.read(), "html.parser")
	friendsList = soup.find_all('p', class_='_52jh _5at0 _592p')
	for friend in friendsList:
		currName = friend.getText()
		if(getAll and currName not in namesOfPeople):
			namesOfPeople[currName] = "" 
		if(currName in namesOfPeople):
			birthday = friend.find_next_sibling('p').getText()
			if(birthday == ""): #gets overwritten if your html page goes 12+ months
				birthday = todaysDate # means birthday is today
			namesOfPeople[currName] = birthday


def getFormattedDate(birthdayString):
	if(birthdayString == "" or birthdayString == todaysDate):
		return birthdayString
	birthdayArr = birthdayString.split(",")
	monthAndDayArr = birthdayArr[1].strip().split(" ")
	month = monthToDigit[monthAndDayArr[0]]
	day = monthAndDayArr[1].strip()
	year = birthdayArr[2].strip()
	return (month + "/" + day + "/" + year)


def getInputsAndSetUp():

	friendsFileName = input("Enter filename that contains friends' names or press enter for default (default is names.txt). Or type 'All' to get everyone's birthdays!: ")
	birthdayFileName = input("Enter filename that has Facebook Mobile Birthday html displaying 12+ months or press enter for default (default is birthday.html): ")

	yearsToKeepEvent = input("Enter years to keep event reminders or press enter for default (default is 3 years): ")

	if(yearsToKeepEvent == ""):
		yearsToKeepEvent = 3
	else:
		try:
			yearsToKeepEvent = int(yearsToKeepEvent)
		except:
			print("Please enter integer value above 0")
			quit()
	if(yearsToKeepEvent < 1):
		print("Please enter integer value above 0")

	if(friendsFileName.strip() == ""):
		friendsFileName = "names.txt"
	if(birthdayFileName.strip() == ""):
		birthdayFileName = "birthday.html"

	getAll = True
	if(friendsFileName != "All"):
		getAll = False
		getNames(friendsFileName) # populates namesOfPeople dictionary with names of friends mapped to their birthday, initialized to empty string
	populateBirthdayDict(birthdayFileName, getAll)
	return yearsToKeepEvent


def main():
	print('''
--------------------------------------------------------------------------------------------------------------------------------
Welcome to Arman's Birthday Extractor script. This program requires two files: names.txt and birthday.html.
param: names.txt should be a newline separated list of Facebook Friends whose birthdays you want to export to your calendar.
param: birthday.html should be the downloaded html page from 'https://m.facebook.com/events/calendar/birthdays'. Be sure to scroll down 12+ months so all birthdays are displayed.
The program takes these two files, scrapes the birthdays, and writes them to a csv file, which can then be imported to Google Calendar.
Since Google Calendar doesn't support recurring events, the program asks for a third parameter for how many years to keep the birthday on your calendar.
The default value for this optional parameter is 5 years.
Any birthdays not found will not be added to the csv file.
Be sure to keep this file in the same directory as the other two files.
--------------------------------------------------------------------------------------------------------------------------------
		''')
	print()
	yearsToKeepEvent = getInputsAndSetUp()
	with open("calendar.csv", "w") as calendar:
		writer = csv.writer(calendar)
		writer.writerow(['Subject', 'Start Date', 'All Day Event']) #write a row a headers, needed for Google Calendar.csv file
		for name in namesOfPeople:
			eventName = name + "'s Birthday"
			birthDate = getFormattedDate(namesOfPeople[name])
			if(birthDate == ""):
				print("Could not find birthday for: " + name)
				continue

			for i in range(yearsToKeepEvent):
				tempRowToWrite = [eventName, birthDate, True]
				writer.writerow(tempRowToWrite)

				yearToAdd = int(birthDate[-2:])
				yearToAdd += 1
				birthDate = birthDate[:-2] + str(yearToAdd)
				
main()	
				