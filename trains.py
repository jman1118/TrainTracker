#Python WAMTA tracker
""" A very basic python app using a gui to track trains on the Washington Metro """

# -*- coding: utf-8 -*-
# -- Train Tracker for Washington Metro --
#Note: code pulled from https://github.com/lygras/WMATA and modified

import json #Deals with json data format
import re # import regional expression (might use later, idk)
from tkinter import * #import tkinter
try:
    from urllib.request import urlopen, Request # Works in Python 3
except ImportError:
    from urllib2 import urlopen, Request #Works in Python 2
    
demo_key = "" #WMATA API key
train_url = "https://api.wmata.com/StationPrediction.svc/json/GetPrediction/All"
hdrs = {'api_key': demo_key}
req = Request(train_url, headers=hdrs) #Provides API key
result = urlopen(req)
raw_data = result.read().decode('utf8')#decodes data using utf 8
data = json.loads(raw_data) #interprets raw data using json
line = ""
#change abbreviations to full station name 
MetroLines = {
	"BL" : "Blue Line",
	"GR" : "Green Line",
	"OR" : "Orange Line",
	"RD" : "Red Line",
	"SV" : "Silver Line",
	"YL" : "Yellow Line"
	}

	

def get_info(line):
	traindata = data["Trains"] #traindata is a list containing dictionaries
	str = ""
#current line being tracked
	time = 5 # time is an integer value for the number of minutes before a train arrives at a station
	for i in traindata:
		for a,b in MetroLines.items():
			i["Line"] = i["Line"].replace(a,b)
		if(i["Line"] in line and i["Min"].isnumeric()):
			str += "The {} train bound for {} will be arriving at {} Station in {} minute(s)\n".format(i["Line"],i["DestinationName"],i['LocationName'],i['Min'])
			print("The {} train bound for {} will be arriving at {} Station in {} minute(s)".format(i["Line"],i["DestinationName"],i['LocationName'],i['Min']))
		elif(i["Line"] == line and i["Min"] == "ARR"):
			str += "The {} train towards {} is now arriving at {} Station\n".format(i["Line"],i["DestinationName"],i["LocationName"])
			print("The {} train towards {} is now arriving at {} Station".format(i["Line"],i["DestinationName"],i["LocationName"]))
		elif(i["Line"] == line and i["Min"] == "BRD"):
			str+="The {} train towards {} is now boarding at {} Station\n".format(i["Line"],i["DestinationName"],i["LocationName"])
			print("The {} train towards {} is now boarding at {} Station".format(i["Line"],i["DestinationName"],i["LocationName"]))
		elif(i["Line"] == line and i["Min"] == "DLY"):
			str+="The {} train bound for {} is delayed\n".format(i["Line"], i["DestinationName"])
			print("The {} train bound for {} is delayed".format(i["Line"], i["DestinationName"]))

	return str

		
	
choices = [ 'Red Line','Green Line','Blue Line','Yellow Line','Orange Line', 'Silver Line']

def gui(choices,line, display_text="Choose a train line from list"):
	
	root = Tk()
	
	canceled = BooleanVar()
	selectedLine = StringVar()
	selectedLine.set(choices[0])
	Label(root, text=display_text).pack()
	OptionMenu(root, selectedLine, *choices).pack()
	txt=Text(root, width=80, height =15)
	s = Scrollbar(root)
	s.pack(side=RIGHT, fill=Y)
	s.config(command=txt.yview)
	s.config(command=txt.yview)
	txt.config(yscrollcommand=s.set)
	txt.pack(expand=True)
	
	def action():
		
		print (selectedLine.get())
		line = selectedLine.get()
		output = get_info(line)
		txt.insert(END,output)
		return line
		
	def clear():		
		txt.delete('1.0',END)
		
	def cancel_action(): canceled.set(True); root.quit()
	Button(root, text="OK", command=action).pack(side=LEFT, ipadx=10)
	Button(root, text="Cancel", command=cancel_action).pack(side=RIGHT, ipadx=10)
	Button(root, text="Clear", command=clear).pack(side=RIGHT)
	
	root.mainloop()
	

gui(choices,line)


