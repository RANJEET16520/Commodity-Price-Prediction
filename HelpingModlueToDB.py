import os
import sys
import pandas as pd 

def Directory(path):
	direcs = []
	for dirs in os.listdir(path):
		# print(dirs)
		direcs.append(dirs)
	return (direcs)

def FilterStateName(state):
	filterstate = ""
	for ch in state:
		if ch is " ":
			continue
		elif ch is'(':
			filterstate+='_'
		elif ch is ')':
			continue
		else:
			filterstate+=ch
	return filterstate

def FileFinder(path):
	for root, dirs, files in os.walk(path):
		# print(path)
		back = []
		for file in files:
			if file.endswith('.csv'):
				# print(path)
				file, _ = file.split('.')
				# print (file)
				back.append(file)
		return back
	