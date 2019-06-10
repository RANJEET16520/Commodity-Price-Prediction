hostname = 'localhost'
username = 'root'
password = '2000'
database = 'PRICEMODEL'

import os
import sys
import pymysql
import HelpingModlueToDB as helpsql 
import DbValues as DV

# Connecting to the Host
connection = pymysql.connect( host=hostname, user=username, passwd=password, db=database, local_infile=True)
cursor = connection.cursor();


class  Tables:

	"""docstring for  Tables"""

	def MarketPriceTable(self):
		self.MartetPriceValues = DV.Price_values()

		self.MarketPriceTableName = 'Daily_Market_Price'
		self.MarketPriceTableFields = ['Id', self.MandiTableFields[0], self.CommodityTableFields[0], 'ArrivalDate', 'MODALPRICE', 'ArrivalQuantity', 'Temperature', 'Weather']
		
		cursor.execute("SHOW TABLES LIKE '{}';".format(self.MarketPriceTableName))
		result = cursor.fetchone()
		if result:
			pass
			print("{} Table exists!!!".format(self.MarketPriceTableName))
		else: 
			cursor.execute('CREATE TABLE {} ( {} VARCHAR(255) PRIMARY KEY, {} VARCHAR(255), {} VARCHAR(255), {} VARCHAR(255) , {} FLOAT(10,4) , {} FLOAT(5,2), {} FLOAT(5,2), {} VARCHAR(255));'.format(self.MarketPriceTableName, self.MarketPriceTableFields[0], 
											self.MarketPriceTableFields[1], self.MarketPriceTableFields[2], self.MarketPriceTableFields[3], self.MarketPriceTableFields[4], self.MarketPriceTableFields[5], self.MarketPriceTableFields[6], self.MarketPriceTableFields[7])) 
			
			cursor.execute("ALTER TABLE {} ADD CONSTRAINT {} FOREIGN KEY ({}) REFERENCES {}({});".format( self.MarketPriceTableName, self.MarketPriceTableFields[1], self.MarketPriceTableFields[1], self.MandiTableName, self.MandiTableFields[0]))
			cursor.execute("ALTER TABLE {} ADD CONSTRAINT {} FOREIGN KEY ({}) REFERENCES {}({});".format( self.MarketPriceTableName, self.MarketPriceTableFields[2], self.MarketPriceTableFields[2], self.CommodityTableName, self.CommodityTableFields[0]))
			print("{} Table Created!!!".format(self.MarketPriceTableName))	

		# print(self.MartetPriceValues)
		
		sql = "INSERT INTO {} ({}, {}, {}, {}, {}, {}, {}, {}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)".format(self.MarketPriceTableName, self.MarketPriceTableFields[0], self.MarketPriceTableFields[1], self.MarketPriceTableFields[2],
										 							self.MarketPriceTableFields[3], self.MarketPriceTableFields[4], self.MarketPriceTableFields[5], self.MarketPriceTableFields[6], self.MarketPriceTableFields[7]) 
		
		for listval in self.MartetPriceValues:
			try:
				v = (listval)
				cursor.execute(sql,v)
				connection.commit()
				# print('Value added!!!')
			except Exception as e:
				pass
				# print('Value exists!!!')
				print(v)
		print(len(self.MartetPriceValues))



	def MandiTable(self):
		self.MandiValue = DV.Mandi_Values()

		self.MandiTableName = 'Markets'
		self.MandiTableFields = ['Mandi_Id', 'Mandi_Name', self.CityTableFields[0]]

		cursor.execute("SHOW TABLES LIKE '{}';".format(self.MandiTableName))
		result = cursor.fetchone()
		if result:
			pass
			print("{} Table exists!!!".format(self.MandiTableName))
		else: 
			cursor.execute('CREATE TABLE {} ( {} VARCHAR(255) PRIMARY KEY, {} VARCHAR(255), {} VARCHAR(255));'.format(self.MandiTableName, self.MandiTableFields[0], self.MandiTableFields[1], self.MandiTableFields[2])) 
			cursor.execute("ALTER TABLE {} ADD CONSTRAINT {} FOREIGN KEY ({}) REFERENCES {}({});".format( self.MandiTableName, self.MandiTableFields[2], self.MandiTableFields[2], self.CityTableName, self.CityTableFields[0]))
			print("{} Table Created!!!".format(self.MandiTableName))	

			sql = "INSERT INTO {} ({},{},{}) VALUES (%s, %s, %s)".format(self.MandiTableName, self.MandiTableFields[0], self.MandiTableFields[1], self.MandiTableFields[2])
				
			for listval in self.MandiValue:
				try:
					v = (listval)
					cursor.execute(sql,v)
					connection.commit()
					# print('Value added!!!')
				except Exception as e:
					pass
				# print('Value exists!!!')
				# print(v)

		self.MarketPriceTable()


	def CityTable(self):
		self.CityValue = DV.City_Values()
		
		self.CityTableName = 'Cities'
		self.CityTableFields = ['City_Id', 'City_Name', self.StateTableFields[0]]
		
		cursor.execute("SHOW TABLES LIKE '{}';".format(self.CityTableName))
		result = cursor.fetchone()
		if result:
			pass
			print("{} Table exists!!!".format(self.CityTableName))
		else: 
			cursor.execute('CREATE TABLE {} ( {} VARCHAR(255) PRIMARY KEY, {} VARCHAR(255), {} VARCHAR(255));'.format(self.CityTableName, self.CityTableFields[0], self.CityTableFields[1], self.CityTableFields[2])) 
			cursor.execute("ALTER TABLE {} ADD CONSTRAINT {} FOREIGN KEY ({}) REFERENCES {}({});".format( self.CityTableName, self.CityTableFields[2], self.CityTableFields[2], self.StateTableName, self.StateTableFields[0]))
			print("{} Table Created!!!".format(self.CityTableName))	

			sql = "INSERT INTO {} ({},{},{}) VALUES (%s, %s, %s)".format(self.CityTableName, self.CityTableFields[0], self.CityTableFields[1], self.CityTableFields[2])
		
			for listval in self.CityValue:
				try:
					v = (listval)
					cursor.execute(sql,v)
					connection.commit()
					# print('Value added!!!')
				except Exception as e:
					pass
				# print('Value exists!!!')
				# print(v)

		self.MandiTable()


	def StateTable(self):
		self.StateValue = DV.State_Values

		self.StateTableName = 'States'
		self.StateTableFields = ['State_Id', 'State_Name']
		
		cursor.execute("SHOW TABLES LIKE '{}';".format(self.StateTableName))
		result = cursor.fetchone()
		if result:
			pass
			print("{} Table exists!!!".format(self.StateTableName))
		else: 
			cursor.execute('CREATE TABLE {} ( {} VARCHAR(255) PRIMARY KEY, {} VARCHAR(255));'.format(self.StateTableName, self.StateTableFields[0], self.StateTableFields[1])) 
			print("{} Table Created!!!".format(self.StateTableName))	

			sql = "INSERT INTO {} ({},{}) VALUES (%s, %s)".format(self.StateTableName, self.StateTableFields[0], self.StateTableFields[1])

			for listval in self.StateValue:
				try:
					v = (listval)
					cursor.execute(sql,v)
					connection.commit()
					# print('Value added!!!')
				except Exception as e:
					pass
					# print('Value exists!!!')
				# print(v)

		self.CityTable()


	def __init__(self, arg):
		# super( Tables, self).__init__()
		self.arg = arg
		self.CommodityValue = DV.Commodity_Values

		self.CommodityTableName = 'Commodity'
		self.CommodityTableFields = ['Comm_Id', 'Commodity_Name', 'Type']

		cursor.execute("SHOW TABLES LIKE '{}';".format(self.CommodityTableName))
		result = cursor.fetchone()
		if result:
			pass
			print("{} Table exists!!!".format(self.CommodityTableName))
		else: 
			cursor.execute('CREATE TABLE {} ( {} VARCHAR(255) PRIMARY KEY, {} VARCHAR(255), {} VARCHAR(255));'.format(self.CommodityTableName, self.CommodityTableFields[0], self.CommodityTableFields[1], self.CommodityTableFields[2])) 
			print("{} Table Created!!!".format(self.CommodityTableName))	

			sql = "INSERT INTO {} ({},{},{}) VALUES (%s, %s, %s)".format(self.CommodityTableName, self.CommodityTableFields[0], self.CommodityTableFields[1], self.CommodityTableFields[2])
			
			for listval in self.CommodityValue:
				try:
					v = (listval)
					cursor.execute(sql,v)
					connection.commit()
					# print('Value added!!!')
				except Exception as e:
					pass
					# print('Value exists!!!')

		self.StateTable()


if __name__ == '__main__':
	Object = Tables(cursor)
