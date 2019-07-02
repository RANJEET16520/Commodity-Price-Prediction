import os
import sys

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkinter import messagebox

import pandas as pd
import DbValues as DV
import WorkingModel as WM

os.system('python3 WorkingModel.py')

class GUI:
	def ExitPriceGraph(self):
		for i in range(0,len(self.year)):
			try:
				self.YearButton[i].destroy()
			except Exception as e:
				pass
			
		for i in range(0,len(self.mon)):
			try:
				self.MonthButton[i].destroy()
			except Exception as e:
				pass			
		
		try:
			self.ShowPG.destroy()
			self.ExitPG.destroy()
			self.ResetPG.destroy()
		except Exception as e:
			pass

		self.Label2 = Label(self.Canvas1)
		self.Label2.place(relx = 0.54, rely = 0.25, height = 20, width = 50)
		self.Label3 = Label(self.Canvas1)
		self.Label3.place(relx = 0.62, rely = 0.25, height = 20, width = 50)
		return

	def ResetPriceGraph(self):
		self.yearselected = 0
		self.monselected = 0
		for i in range(len(self.mon)):
			try:
				if self.MonthButton[i]['bg'] == 'blue':
					self.MonthButton[i]['bg'] = "#d9d9d9"
			except Exception as e:
				pass				
		for i in range(len(self.year)):
			try:
				if self.YearButton[i]['bg'] == 'blue':
					self.YearButton[i]['bg'] = "#d9d9d9"
			except Exception as e:
				pass
			
		return
		
	def DayData(self,monselected):
		print(monselected)
		self.monselected = 0
		self.monselected = monselected

		def checking8(x):
			if monselected == 0:
				return
			WM.ShowPrice(x,self.yearselected,self.monselected,self.mandi_name)
			return

		da = self.yr_df.groupby(['month']).get_group(self.monselected)
		dd = da[['MODALPRICE','day']]

		self.MonthButton[self.indexmonth[self.monselected]].configure(bg = 'blue')
	
		self.ShowPG = Button(self.Canvas1, text = 'Show Price Graph', command = lambda x = dd: checking8(x)) # Mandi Reset Button
		self.ShowPG.place(relx = 0.555, rely = 0.42, height = 30, width = 120)

		self.ResetPG = Button(self.Canvas1, text = 'Reset Values', command = lambda x = self.monselected: self.ResetPriceGraph()) # Mandi Reset Button
		self.ResetPG.place(relx = 0.555, rely = 0.47, height = 30, width = 120)

		self.ExitPG = Button(self.Canvas1, text = 'Exit Price Graph', command = lambda x = self.monselected: self.ExitPriceGraph()) # Mandi Reset Button
		self.ExitPG.place(relx = 0.555, rely = 0.52, height = 30, width = 120)
		return
		# print(dd)
		
	def MonthsDisp(self, yearselected):

		def checking7(x):
			for j in range(0, len(self.mon)):
				if self.yearselected == 0:
					messagebox.showerror("Error","Wrong Option!!!")
					return
				if self.MonthButton[j]['bg'] == 'blue':
					messagebox.showerror("Error","Wrong Option!!!")
					return
			self.DayData(x)

		self.yearselected = 0
		self.yearselected = yearselected
		print(self.yearselected)
		
		self.YearButton[self.indexyear[self.yearselected]].configure(bg = 'blue')

		self.yr_df = 0
		self.yr_df = self.df.groupby(['year']).get_group(self.yearselected)
		self.mon = self.yr_df['month'].unique().tolist()

		y = self.y
		inc1, inc2 = 0, 0
		i = 0
		self.indexmonth = {}

		for mun in self.mon:
			self.indexmonth.update({mun:i})
			self.MonthButton[i] = Button(self.Canvas1, text = mun, command = lambda x = mun: checking7(x)) # Mandi Selection
			if i%2 is 0:
				self.MonthButton[i].place(relx = 0.605, rely = 0.28 + inc1, height = self.ButHeight, width = 40)
				inc1 += y
			else:
				self.MonthButton[i].place(relx = 0.635, rely = 0.28 + inc2, height = self.ButHeight, width = 40)
				inc2 += y
			i+=1
		return

	# To create price graph monthly
	def Price_Graph(self, data):
		# messagebox.showerror("Error","Under-Construction!!!")
		Db_Data = WM.DBData(data)
		def checking6(x):
			for j in range(0, len(self.year)):
				if self.YearButton[j]['bg'] == 'blue':
					pass
					show = False
					messagebox.showerror("Error","Wrong Option!!!")
					return
			self.MonthsDisp(x)

		if len(Db_Data) == 0:
			messagebox.showerror("Error","No Data!!!")
			return
		
		self.Label2 = Label(self.Canvas1)
		self.Label2.place(relx = 0.54, rely = 0.25, height = 20, width = 50)
		self.Label2.configure(anchor = W)
		self.Label2.configure(background = self._bgcolor)
		self.Label2.configure(disabledforeground = "#a3a3a3")
		self.Label2.configure(foreground = "#5e5e5e")
		self.Label2.configure(text = '''Year''')
		
		self.Label3 = Label(self.Canvas1)
		self.Label3.place(relx = 0.62, rely = 0.25, height = 20, width = 50)
		self.Label3.configure(anchor = W)
		self.Label3.configure(background = self._bgcolor)
		self.Label3.configure(disabledforeground = "#a3a3a3")
		self.Label3.configure(foreground = "#5e5e5e")
		self.Label3.configure(text = '''Month''')
		# self.Label3.pack()
	
		self.df = WM.Data_Builder(Db_Data)
		self.year = 0
		self.year = self.df['year'].unique().tolist()
		self.indexyear = {}
		y = self.y
		inc = 0
		i = 0
		for ys in self.year:
			self.indexyear.update({ys:i})
			self.YearButton[i] = Button(self.Canvas1, text = ys, command = lambda x = ys: checking6(x)) # Mandi Selection
			self.YearButton[i].place(relx = 0.53, rely = 0.28 + inc, height = self.ButHeight, width = 60)
			inc += y
			i+=1
		return

	def AllMandiNext(self, data):
		show = True
		if self.but5 > 0:
			for j in range(0, len(self.mandi_list)):
				if self.Button5[j]['bg'] == 'blue':
					pass
					show = False
					messagebox.showerror("Error","Wrong Option!!!")
					break
		if show:
			print(data)
			WM.NextDay(data,self.city_name)
			pass
	
	def ShortPrediction(self, data):	
		Db_Data = WM.DBData(data)
		if len(Db_Data) == 0:
			messagebox.showerror("Error","No Data!!!")
			pass
		elif len(Db_Data) < 20:
			messagebox.showerror("Error","Not Sufficient Data!!!")
			pass
		else:
			show = WM.Short(Db_Data,self.mandi_name)
			if show == False:
				messagebox.showerror("Error","Not Sufficient Data!!!")
		return

	def LongPrediction(self, data):
		Db_Data = WM.DBData(data)
		if len(Db_Data) == 0:
			messagebox.showerror("Error","No Data!!!")
			pass
		elif len(Db_Data) < 20:
			messagebox.showerror("Error","Not Sufficient Data!!!")
			pass
		else:
			WM.Long(Db_Data,self.mandi_name)
		return

	def Kill5(self):
		for i in range(0,len(self.mandi_list)):
			self.Button5[i].destroy()
		try:
			self.ShortTerm.destroy()
			self.LongTerm.destroy()
			self.PGraph.destroy()
		except Exception as e:
			pass
		self.ExitPriceGraph()
		return		

	def Kill4(self):
		for i in range(0,len(self.type_list)):
			self.Button4[i].destroy()
		try:
			self.ResetButton5.destroy()
			self.NextDay.destroy()
		except Exception as e:
			pass
		return

	def Kill3(self):
		for i in range(0,len(self.Commodity_Values)):
			self.Button3[i].destroy()
		try:
			self.ResetButton4.destroy()
			self.NextDay.destroy()
		except Exception as e:
			pass
		return

	def Kill2(self):
		for i in range(0,len(self.city_list)):
			self.Button2[i].destroy()
		try:
			self.NextDay.destroy()
			self.ResetButton3.destroy()
		except Exception as e:
			pass
		return

	def Mandi_Clear(self):
		for i in range(len(self.mandi_list)):
			if self.Button5[i]['bg'] == 'blue':
				self.Button5[i]['bg'] = "#d9d9d9"
		try:
			self.ShortTerm.destroy()
			self.LongTerm.destroy()
			self.PGraph.destroy()
		except Exception as e:
			pass
		self.ExitPriceGraph()
		return

	def Type_Clear(self):
		for i in range(len(self.type_list)):
			if self.Button4[i]['bg'] == 'blue':
				self.Button4[i]['bg'] = "#d9d9d9"
		try:
			self.NextDay.destroy()
			self.ResetButton5.destroy()
		except Exception as e:
			pass

		if self.but5 > 0:
			self.Kill5()
		return

	def Commodity_Clear(self):
		for i in range(0,len(self.Commodity_Values)):
			if self.Button3[i]['bg'] == 'blue':
				self.Button3[i]['bg'] = "#d9d9d9"
		try:
			self.ResetButton4.destroy()
		except Exception as e:
			pass

		if self.but4 > 0:
			self.Kill4()
			
			if self.but5 > 0:
				self.Kill5()
		return

	def City_Clear(self):
		for i in range(len(self.city_list)):
			if self.Button2[i]['bg'] == 'blue':
				self.Button2[i]['bg'] = "#d9d9d9"
		try:
			self.ResetButton3.destroy()
		except Exception as e:
			pass

		if self.but3 > 0:
			self.Kill3()

			if self.but4 > 0:
				self.Kill4()

				if self.but5 > 0:
					self.Kill5()
		return

	def State_Clear(self):
		for i in range(len(self.State_Values)):
			if self.Button1[i]['bg'] == 'blue':
				self.Button1[i]['bg'] = "#d9d9d9"
		try:
			self.ResetButton2.destroy()
		except Exception as e:
			pass

		if self.but2 > 0:
			self.Kill2()
			
			if self.but3 > 0:
				self.Kill3()

				if self.but4 > 0:
					self.Kill4()

					if self.but5 > 0:
						self.Kill5()
		return

	# Daily Market Price of the Selected Type
	def DailyMarketPrice(self,Mandi):
		self.Mandi = Mandi
		self.mandi_name = Mandi[1]
		# Pair('Commodity_id', 'Mandi_id') to fetch data from DB
		Data = [str(self.price[0]), str(self.Mandi[0])]

		print(self.Mandi)
		self.ResetButton5 = Button(self.Canvas1, text = 'Reset Mandi', command = lambda x = self.Mandi[3]: self.Mandi_Clear()) # Mandi Reset Button
		self.ResetButton5.place(relx = 0.85, rely = 0.85, height = 40, width = 120)

		if self.but5 > 0:
			self.Button5[self.Mandi[3]].configure(bg= 'blue')
			print("{}->{}".format(self.Mandi[0], self.Mandi[1]))

			self.ShortTerm = Button(self.Canvas1, text = 'Short-Term', command = lambda x = Data : self.ShortPrediction(x)) # Short-Term Selection
			self.ShortTerm.place(relx = 0.72, rely = 0.85, height = 40, width = 120)

			self.LongTerm = Button(self.Canvas1, text = 'Long-Term', command = lambda x = Data : self.LongPrediction(x)) # Long-Term Selection
			self.LongTerm.place(relx = 0.62, rely = 0.85, height = 40, width = 120)

			self.PGraph = Button(self.Canvas1, text = 'Price-Graph', command = lambda x = Data : self.Price_Graph(x)) # Short-Term Selection
			self.PGraph.place(relx = 0.671, rely = 0.78, height = 40, width = 120)

		return

	# Mandi Buttons of the selected City
	def CreateMandis(self, price):
		self.mandi_list = []
		self.price = price
		
		def checking5(x):
			for j in range(0, len(self.mandi_list)):
				if self.Button5[j]['bg'] == 'blue':
					pass
					show = False
					messagebox.showerror("Error","Wrong Option!!!")
					return
			self.DailyMarketPrice(x)

		print(self.price)
		self.ResetButton4 = Button(self.Canvas1, text = 'Reset Type', command = lambda x = self.price[3]: self.Type_Clear()) # Type Reset Button
		self.ResetButton4.place(relx = 0.85, rely = 0.80, height = 40, width = 120)

		if self.but4 > 0:
			"""If there exist no Commodity-type for processing, this condition will operate on your selected choise."""
			self.Button4[self.price[3]].configure(bg = 'blue')
			print("{}->{}".format(self.price[0], self.price[1]))

			for lis in self.Mandi_Values:
				if self.city[0] in lis:
					self.mandi_list.append(lis)	
			
			y = self.y
			inc = 0
			i = 0
			
			Data = [self.price[0], self.city[0]]
			self.NextDay = Button(self.Canvas1, text = 'All Mandi Next Day', command = lambda x = Data: self.AllMandiNext(x)) # Short-Term Selection
			self.NextDay.place(relx = 0.66, rely = 0.65, height = 40, width = 150)

			self.Button5 = []
			self.Button5 = [0 for j in range(0,len(self.Mandi_Values))]
			"""
			Creating Mindi Buttons, from Mandis linked with selected City, stored in the database.
			The city_values has value in the form of (['Mandi_Id','Mandi_Name','City_Id','Mandi_No.']).
			Mandi_Id: Used to fetch data from actual Database.
			Mandi_Name: Used to display in GUI.
			City_Id: Is futher linked with next Commodity type button.
			Command Button display the Commodities.
			"""
			
			self.but5 += 1
			for lis in self.mandi_list:
				lis.append(i)
				self.Button5[i] = Button(self.Canvas1, text = lis[1], command = lambda x = lis: checking5(x)) # Mandi Selection
				self.Button5[i].place(relx = 0.85, rely = 0.1+inc, height = self.ButHeight, width = self.ButWidth)
				inc += y
				i+=1

		return

	# Commodity-Types Buttons of the selected Commodity
	def CreateType(self,Comm):
		self.type_list = []
		self.Comm = Comm

		def checking4(x):
			"""
			If you have selected Commodity-Type for processing, this loop will check if there aleady exists selected Commodity-Type or Not.
			if button exist then it will reject your request for processing and display an error message ('Wrong Option!!!')
			And it will stop the next operations.
			"""
			for j in range(0, len(self.type_list)):
				if self.Button4[j]['bg'] == 'blue':
					pass
					show = False
					messagebox.showerror("Error","Wrong Option!!!")
					return			
			self.CreateMandis(x)

		print(self.Comm)
		self.ResetButton3 = Button(self.Canvas1, text = 'Reset Commodity', command = lambda x = self.Comm[1]: self.Commodity_Clear()) # Commodity Reset Button
		self.ResetButton3.place(relx = 0.85, rely = 0.75, height = 40, width = 120)

		if self.but3 > 0:
			"""If there exist no Commodity for processing, this condition will operate on your selected choise."""
			self.Button3[self.Comm[1]].configure(bg = 'blue')
			print("{}->{}".format(self.Comm[0], self.Comm[1]))	
	
			for lis in self.type_value:
				if self.Comm[0] in lis:
					self.type_list.append(lis)

			y = self.y
			inc = 0
			i = 0
			self.Button4 = []
			self.Button4 = [0 for j in range(0,len(self.type_value))]

			"""
			Creating Type of Commodity Buttons, stored in the database,from type linked with selected Commodity.
			The type_value has value in the form of (['Commodity_id','Name_of_Commodity_Type','Commodity_Name','Commodity_Type_No.']).
			Commodity_id: Used to fetch data from actual Database.
			Name_of_Commodity_Type: Used to display in GUI.
			Commodity_Name: Commodity to which this type related.
			Commodity_Type_No: No use
			Command Button display the types of Commodity of selected Commodities.
			"""
			self.but4 +=1
			for lis in self.type_list:
				lis.append(i)
				self.Button4[i] = Button(self.Canvas1, text = lis[1], command = lambda x = lis: checking4(x)) # Commodity-Types Selection
				self.Button4[i].place(relx = 0.67, rely = 0.1+inc, height = self.ButHeight, width = self.ButWidth)
				inc += y
				i += 1
		return

	# Commodity Buttons of the selected Mandi
	def CreateCommodity(self, city):
		show = True
		self.city = city
		self.city_name = city[1]

		def checking3(x):
			"""
			If you have selected Commodity for processing, this loop will check if there aleady exists selected Commodity or Not.
			if button exist then it will reject your request for processing and display an error message ('Wrong Option!!!')
			And it will stop the next operations.
			"""
			for j in range(0, len(self.Commodity_Values)):
				if self.Button3[j]['bg'] == 'blue':
					pass
					show = False
					messagebox.showerror("Error","Wrong Option!!!")
					return
			self.CreateType(x)

		print(self.city)
		self.ResetButton2 = Button(self.Canvas1, text = 'Reset City', command = lambda x = self.city[3]: self.City_Clear()) # City Reset Button
		self.ResetButton2.place(relx = 0.85, rely = 0.70, height = 40, width = 120)

		if self.but2 > 0:
			"""If there exist no city for processing, this condition will operate on your selected choise."""
			self.Button2[self.city[3]].configure(bg= 'blue')
			print("{}->{}".format(self.city[0], self.city[1]))
			
			y = self.y
			inc = 0
			i = 0

			self.Button3 = []
			self.Button3 = [0 for j in range(0,len(self.Commodity_Values))]
			
			"""
			Creating Commodity Buttons, stored in the database.
			The Commodity_Values has value in the form of (['Commodity_Name','Commodity_No.']).
			Commodity_Name: Used to display in GUI.
			Commodity_No: Is futher linked with next types of Commodity button.
			Command Button display the types of Commodity of selected Commodities.
			"""
			self.but3 +=1
			for lis in self.Commodity_Values:
				lis.append(i)
				self.Button3[i] = Button(self.Canvas1, text = lis[0], command = lambda x = lis: checking3(x)) # Commodity Selection
				self.Button3[i].place(relx=0.50, rely=0.1+inc, height=self.ButHeight, width=self.ButWidth)
				inc += y
				i += 1
		return

	# City Buttons of the selected State
	def CreateCities(self, State):
		self.city_list = []
		self.State = State
		show = True

		def checking2(x):
			"""
			If you have selected city for processing, this loop will check if there aleady exists selected city or Not.
			if button exist then it will reject your request for processing and display an error message ('Wrong Option!!!')
			And it will stop the next operations.
			"""
			for j in range(0, len(self.city_list)):
				if self.Button2[j]['bg'] == 'blue':
					pass
					show = False
					messagebox.showerror("Error","Wrong Option!!!")
					return
			self.CreateCommodity(x)
		
		print(self.State)
		self.ResetButton1 = Button(self.Canvas1, text = 'Reset State', command = lambda x = self.State[0] : self.State_Clear()) # State Reset Button
		self.ResetButton1.place(relx = 0.85, rely = 0.65, height = 40, width = 120)

		if self.but1 > 0:
			"""If there exist no state for processing, this condition will operate on your selected choise."""		
			self.Button1[self.State[2]].configure(bg = 'blue')
			print("{}->{}".format(self.State[0],self.State[1]))
			
			for lis in self.City_Values:
				if self.State[0] in lis:
					self.city_list.append(lis)

			y = self.y
			inc = 0
			i = 0
			"""
			Creating City Buttons, from Cities linked with selected state, stored in the database.
			The city_values has value in the form of (['City_Id','City_Name','State_Id','City_No.']).
			City_Name: Used to display in GUI.
			City_Id: Is futher linked with next Commodity type button.
			Command Button display the Commodities.
			"""
			self.Button2 = []
			self.Button2 = [0 for j in range(0,len(self.City_Values))]
			"""
			Since Cities are large in no. so we have used two rows to display the cities in th GUI.
			So we are taking two different location for the cities in GUI (xx1,xx2).
			If 80% of the GUI space is filled with cities in the row for (xx1) then it will form city buttons over (xx2) location.
			"""
			xx1, xx2 = 0.22, 0.33 
			self.but2+=1
			xx = xx1
			no = True
			for lis in self.city_list:
				lis.append(i)
				if 0.1 + inc > 0.8 and no == True:
					xx = xx2
					inc = 0
					no = False

				self.Button2[i] = Button(self.Canvas1, text = lis[1], command = lambda x = lis: checking2(x) ) # City Selection
				self.Button2[i].place(relx=xx, rely=0.1+inc, height=self.ButHeight, width=self.ButWidth)
				inc += y
				i+=1		
		return

	# State Buttons
	def CreteStates(self):
		y = self.y
		inc = 0
		i = 0

		def checking1(x):
			"""
			If you have selected state for processing, this loop will check if there aleady exists selected state or Not.
			if button exist then it will reject your request for processing and display an error message ('Wrong Option!!!')
			And it will stop the next operations.
			"""
			for j in range(0, len(self.State_Values)):
				if self.Button1[j]['bg'] == 'blue':
					show = False
					messagebox.showerror("Error","Wrong Option!!!")
					self.Kill2()
					return
			self.CreateCities(x)

		show = True
		if show:
			self.Button1 = []
			self.Button1 = [0 for j in range(0,len(self.State_Values))]

			self.but1 += 1
			"""
			Creating State Buttons, from states stored in the database.
			The state_value has value in the form of (['State_Id','State_Name','State_No.']).
			State_Name: Used to display in GUI.
			State_Id: Is futher linked with next city type button.
			Command Button display the cities of selected state.
			"""
			for lis in self.State_Values:
				lis.append(i)
				self.Button1[i] = Button(self.Canvas1, text = lis[1], command = lambda x = lis: checking1(x)) # Selection of state Button
				self.Button1[i].place(relx=0.05, rely=0.1+inc, height=self.ButHeight, width=self.ButWidth)
				self.Button1[i].configure(activebackground="#d9d9d9")
				inc += y
				i+=1
		return


	def Page_Making(self):
		# MAIN FRAME CREATION
		self.style = ttk.Style()
		
		self.style.configure('.',background = self._bgcolor)
		self.style.configure('.',foreground = self._fgcolor)
		self.style.map('.',background=
		[('selected', self._fgcolor), ('active',self._ana2color)])

		top.geometry("1440x880+228+134")
		top.title("Commodity Price Forecasting")	
		top.configure(background="black")

		self.Canvas1 = Canvas(top, scrollregion=(0,0,1440,1200))
		self.Canvas1.place(relx = -0.01, rely = -0.01, relheight = 1.03, relwidth = 1.01)
		self.Canvas1.configure(background = self._bgcolor)
		self.Canvas1.configure(borderwidth = "2")
		self.Canvas1.configure(insertbackground = "black")
		self.Canvas1.configure(relief = RIDGE)
		self.Canvas1.configure(selectbackground = "#c4c4c4")
		self.Canvas1.configure(selectforeground = "black")
		self.Canvas1.configure(width = 1440)
		# NAMING FOR HomePage
		self.Label1 = Label(self.Canvas1)
		self.Label1.place(relx = 0.05, rely = 0.005, height = 50, width = 160)
		self.Label1.configure(anchor = W)
		self.Label1.configure(background = self._bgcolor)
		self.Label1.configure(disabledforeground = "#a3a3a3")
		self.Label1.configure(font = self.font11)
		self.Label1.configure(foreground = "#5e5e5e")
		self.Label1.configure(text = '''Homepage''')
		self.Label1.configure(width = 281)

		# NAMING FOR State
		self.Label1 = Label(self.Canvas1)
		self.Label1.place(relx = 0.07, rely = 0.05, height = 50, width = 281)
		self.Label1.configure(anchor = W)
		self.Label1.configure(background = self._bgcolor)
		self.Label1.configure(disabledforeground = "#a3a3a3")
		self.Label1.configure(font = self.font11)
		self.Label1.configure(foreground = "#5e5e5e")
		self.Label1.configure(text = '''State''')
		self.Label1.configure(width = 281)
		
		# NAMING FOR Cities
		self.Label1 = Label(self.Canvas1)
		self.Label1.place(relx = 0.3, rely = 0.05, height = 50, width = 281)
		self.Label1.configure(anchor = W)
		self.Label1.configure(background = self._bgcolor)
		self.Label1.configure(disabledforeground = "#a3a3a3")
		self.Label1.configure(font = self.font11)
		self.Label1.configure(foreground = "#5e5e5e")
		self.Label1.configure(text = '''City''')
		self.Label1.configure(width = 281)

		# NAMING FOR Mandis
		self.Label1 = Label(self.Canvas1)
		self.Label1.place(relx = 0.505, rely = 0.05, height = 50, width = 281)
		self.Label1.configure(anchor = W)
		self.Label1.configure(background = self._bgcolor)
		self.Label1.configure(disabledforeground = "#a3a3a3")
		self.Label1.configure(font = self.font11)
		self.Label1.configure(foreground = "#5e5e5e")
		self.Label1.configure(text = '''Commodity''')
		self.Label1.configure(width = 281)

		# NAMING FOR Commodity
		self.Label1 = Label(self.Canvas1)
		self.Label1.place(relx = 0.70, rely = 0.05, height = 50, width = 281)
		self.Label1.configure(anchor = W)
		self.Label1.configure(background = self._bgcolor)
		self.Label1.configure(disabledforeground = "#a3a3a3")
		self.Label1.configure(font = self.font11)
		self.Label1.configure(foreground = "#5e5e5e")
		self.Label1.configure(text = '''Type''')
		self.Label1.configure(width = 281)

		# NAMING FOR Types
		self.Label1 = Label(self.Canvas1)
		self.Label1.place(relx = 0.87, rely = 0.05, height = 50, width = 281)
		self.Label1.configure(anchor = W)
		self.Label1.configure(background = self._bgcolor)
		self.Label1.configure(disabledforeground = "#a3a3a3")
		self.Label1.configure(font = self.font11)
		self.Label1.configure(foreground = "#5e5e5e")
		self.Label1.configure(text = '''Market''')
		self.Label1.configure(width = 281)
		self.CreteStates()

		# NAMING TO Reset Values
		self.Label1 = Label(self.Canvas1)
		self.Label1.place(relx = 0.835, rely = 0.6, height = 50, width = 281)
		self.Label1.configure(anchor = W)
		self.Label1.configure(background = self._bgcolor)
		self.Label1.configure(disabledforeground = "#a3a3a3")
		self.Label1.configure(font = self.font11)
		self.Label1.configure(foreground = "#5e5e5e")
		self.Label1.configure(text = '''Reset Values''')
		self.Label1.configure(width = 281)
		# self.Canvas1.pack(side=LEFT,expand=True)


	def __init__(self, arg):
		# ALL NECESSARY DECLARATIONS
		# super(GUI, self).__init__()
		self.arg = arg
		'''This class configures and populates the toplevel window.
		   top is the toplevel containing window.'''
		self._bgcolor = '#d9d9d9'  # X11 color: 'gray85'
		self._fgcolor = '#000000'  # X11 color: 'black'
		self._fgcolor = '#000000' # X11 color: 'gray85'
		self._ana1color = '#d9d9d9' # X11 color: 'gray85' 
		self._ana2color = '#d9d9d9' # X11 color: 'gray85' 
		self.font11 = "-family Arial -size 20 -weight normal -slant roman "  \
		"-underline 0 -overstrike 0"
		self.font12 = "-family Arial -size 10 -weight normal -slant italic "  \
		"-underline 0 -overstrike 0"
		self.font13 = "-family Arial -size 10 -weight normal -slant roman "  \
		"-underline 0 -overstrike 0"
		self.font9 = "-family {Segoe UI} -size 9 -weight normal -slant "  \
		"roman -underline 0 -overstrike 0"
		
		self.ButHeight = 20
		self.ButWidth = 140
		self.y = 0.020

		self.messagebox = messagebox
		self.but1 = 0
		self.but2 = 0
		self.but3 = 0
		self.but4 = 0
		self.but5 = 0
		self.mon = [0 for j in range(0,100)]
		self.year = [0 for j in range(0,100)]

		self.Button1 = [0 for j in range(0,100)]
		self.Button2 = [0 for j in range(0,100)]
		self.Button3 = [0 for j in range(0,100)]
		self.Button4 = [0 for j in range(0,100)]
		self.Button5 = [0 for j in range(0,100)]
		self.YearButton = [0 for j in range(0,10)]
		self.MonthButton = [0 for j in range(0,15)]
		self.ResetButton1 = 0
		self.ResetButton2 = 0
		self.ResetButton3 = 0
		self.ResetButton4 = 0
		self.ResetButton5 = 0


		self.State_Values = DV.State_Values
		self.City_Values = DV.City_Values()
		self.city_list = []
		self.Mandi_Values = DV.Mandi_Values()
		self.mandi_list = []
		self.Commodity_Values = [['Oil'], ['Pulses']]
		self.type_value = DV.Commodity_Values
		self.type_list = []
					
		self.Page_Making()

		
if __name__ == '__main__':	
	top = tk.Tk()
	Object = GUI(top)   # Main Call to Class
	top.mainloop()