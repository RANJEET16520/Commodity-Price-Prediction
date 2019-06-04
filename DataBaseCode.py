hostname = 'localhost'
username = 'root'
password = '2000'
database = 'CDAC'

import os
import sys
import pymysql
import HelpingModlueToDB as helpsql 

# Connecting to the Host
connection = pymysql.connect( host=hostname, user=username, passwd=password, db=database, local_infile=True)
cursor = connection.cursor();

ALL_TABLES = []
ALL_COMMODITIES_TABLE = []
ALL_STATE_TABLE = []
ALL_SUBCOMMODITIES_TABLE = []
ALL_DISTRICT_TABLE = []
ALL_MARKET_TABLE = []

MainTable_Value = []
MainTable_field = []
Table_associated_with_MainTable_in_DB = {}
Table_associated_with_State_Oil_Table_in_DB = {}
Table_associated_with_State_Pulse_Table_in_DB = {}
Sub_oil_table, sub_oils_DB_table = {}, {}
Sub_pulse_table, sub_pulse_DB_table = {}, {}


def All_tables():
	print(ALL_COMMODITIES_TABLE)
	print(ALL_STATE_TABLE)
	print(ALL_SUBCOMMODITIES_TABLE)
	print(ALL_DISTRICT_TABLE)
	print(ALL_MARKET_TABLE)

def dict_print(dictionay):
	for key, value in dictionay.items():
		print("{} : {}".format(key, value))
	print()



def list_print(lis):
	for value in lis:
		print(value)



def CreateMarketTable(path, MarketName, Distt_Table_name, Distt_Table_name_fields):
	for Market in MarketName:
		Market_Path = '{}/{}.csv'.format(path, Market)
		Market_table_name = "{}_{}".format(Distt_Table_name, Market)
		# print(Market_Path)
		
		# cursor.execute("DROP TABLE IF EXISTS {}".format(Market_table_name))
		cursor.execute("SHOW TABLES LIKE '{}';".format(Market_table_name))
		result = cursor.fetchone()
		if result:
			pass
			print("Market-Table {} exists!!!".format(Market_table_name))
		else:
			Market_table_name_fields = ['Id', 'ArrivalDate', 'MODALPRICE', 'ArrivalQuantity', 'Temperature', 'Weather']
			cursor.execute('CREATE TABLE {} ({} INT, {} VARCHAR(255) , {} FLOAT(10,4) , {} INT, {} FLOAT(5,2), {} VARCHAR(255));'. format(Market_table_name, Market_table_name_fields[0], Market_table_name_fields[1], Market_table_name_fields[2], Market_table_name_fields[3], Market_table_name_fields[4], Market_table_name_fields[5]))
			cursor.execute("LOAD DATA LOCAL INFILE '{}' INTO TABLE {} FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS;".format(Market_Path, Market_table_name))
			print("{} Table Created!!!".format(Market_table_name))
		
		if Market_table_name not in ALL_TABLES:
			ALL_TABLES.append(Market_table_name)
			ALL_MARKET_TABLE.append(Market_table_name)



def CreateDistrictTables(path, StateNames, sub_commodities_table, CommodityType, Sub_Commodity_TableFields):
	State_DB_Table, sub_comm_DB_tables, sub_comm_table = {}, {}, {}

	if CommodityType is 'Oil':
		State_DB_Table = Table_associated_with_State_Oil_Table_in_DB
		sub_comm_DB_tables = sub_oils_DB_table
		sub_comm_table = Sub_oil_table
	else:
		State_DB_Table = Table_associated_with_State_Pulse_Table_in_DB
		sub_comm_DB_tables = sub_pulse_DB_table
		sub_comm_table = Sub_pulse_table

	for states in StateNames:
	# states = 'Andhra Pradesh'
		Statepath = path + "/{}".format(states)
		states_table = State_DB_Table[states]
		states_table_db = sub_comm_DB_tables[states]
		# print("{}:".format(states_table))

		for subval in sub_comm_table[states_table]:
			sub_commodity_path = Statepath + '/{}'.format(subval)
			# print(subval)
			
			for disttval in states_table_db[subval]:
				# print(disttval)
				distt_path = sub_commodity_path + '/{}'.format(disttval)
				# print(distt_path)

				MarketName = helpsql.FileFinder(distt_path)
				# print(MarketName)

				SubCommTableName = sub_comm_table[states_table][subval]
				Distt_Table_name = SubCommTableName+ "_{}".format(disttval)
				# print(Distt_Table_name)
				
				SubCommTableFields = Sub_Commodity_TableFields[states][subval]
				# print(SubCommTableFields)
				
				Distt_Table_name_fields = ['Distt_{}_{}'.format(SubCommTableFields[0], disttval), 'Market']
				# print(Distt_Table_name_fields)

				# cursor.execute("DROP TABLE IF EXISTS {}".format(Distt_Table_name))
				cursor.execute("SHOW TABLES LIKE '{}';".format(Distt_Table_name))
				result = cursor.fetchone()
				if result:
					pass
					print("District-Table {} exists!!!".format(Distt_Table_name))
				else:
					pass
					cursor.execute("CREATE TABLE {} ({} VARCHAR(255), {} VARCHAR(255) PRIMARY KEY);".format(Distt_Table_name, Distt_Table_name_fields[0], Distt_Table_name_fields[1]))
					cursor.execute("ALTER TABLE {} ADD CONSTRAINT {} FOREIGN KEY ({}) REFERENCES {}({});".format( Distt_Table_name, Distt_Table_name_fields[0], Distt_Table_name_fields[0], SubCommTableName, SubCommTableFields[1]))
					print("{} Table Created!!!".format(Distt_Table_name))
	
				if Distt_Table_name not in ALL_TABLES:
					ALL_TABLES.append(Distt_Table_name)
					ALL_DISTRICT_TABLE.append(Distt_Table_name)


				sql = "INSERT INTO {} ({},{}) VALUES (%s, %s)".format(Distt_Table_name, Distt_Table_name_fields[0], Distt_Table_name_fields[1])
				# print(sql)
				for s in MarketName:
					try:
						v = ( "{}".format(disttval), str(s))
						cursor.execute(sql,v)
						connection.commit()
						# print('Value added!!!')
					except Exception as e:
						pass
						# print('Value exists!!!')

				CreateMarketTable(distt_path,MarketName, Distt_Table_name, Distt_Table_name_fields)
				



def CreateSubCommoditiesTables(path, StateNames, CommTableName, state_to_commodity, state_to_TableField, CommodityType):
	sub_commodities_table = {}
	DB_sub_commodities_table = {}
	District_with_sub_comm = {}
	Sub_Commodity_TableFields = {}

	for states in StateNames:
		Db_Table_name = ""
		
		if CommodityType is 'Oil':
			Db_Table_name = Table_associated_with_State_Oil_Table_in_DB[states]
		else:
			Db_Table_name = Table_associated_with_State_Pulse_Table_in_DB[states]

		Statepath = path + "/{}".format(states)
		sub_commodities = state_to_commodity[states]
		
		set_Db_table_name = {}
		Table_list = []
		distt_value = {}
		sub_comm_value_tablefield = {}

		for sub_comm_value in sub_commodities:
			val = sub_comm_value
			Table_list.append(val)

			sub_commodity_path = Statepath + '/{}'.format(val)
		
			DistrictNames = helpsql.Directory(sub_commodity_path)
			Corrected_DistrictNames = []
			for name in DistrictNames:
				name = helpsql.FilterStateName(name)
				Corrected_DistrictNames.append(name)

			statename = helpsql.FilterStateName(states)
			
			StateTableName = "{}_{}".format(CommTableName, statename)
			StateTableFields = state_to_TableField[statename]
			subcommodityname = helpsql.FilterStateName(val)
			SubCommTableName = "{}_{}_{}".format(CommTableName, statename, subcommodityname)
			set_Db_table_name.update({val:SubCommTableName})
			
			SubCommTableFields = ['Sub_{}_{}_{}'.format(CommTableName,statename,val), 'District']
			sub_comm_value_tablefield.update({val : SubCommTableFields})

			distt_value.update({val : Corrected_DistrictNames})
			
			# cursor.execute("DROP TABLE IF EXISTS {}".format(SubCommTableName))
			cursor.execute("SHOW TABLES LIKE '{}';".format(SubCommTableName))
			result = cursor.fetchone()
			if result:
				pass
				print("Sub-Commodity-Table {} exists!!!".format(SubCommTableName))
			else:
				cursor.execute("CREATE TABLE {} ({} VARCHAR(255), {} VARCHAR(255) PRIMARY KEY);".format(SubCommTableName, SubCommTableFields[0], SubCommTableFields[1]))
				cursor.execute("ALTER TABLE {} ADD CONSTRAINT {} FOREIGN KEY ({}) REFERENCES {}({});".format( SubCommTableName, SubCommTableFields[0], SubCommTableFields[0], StateTableName, StateTableFields[1]))
				print("{} Table Created!!!".format(SubCommTableName))
			
			if SubCommTableName not in ALL_TABLES:
				ALL_TABLES.append(SubCommTableName)
				ALL_SUBCOMMODITIES_TABLE.append(SubCommTableName)

			sql = "INSERT INTO {} ({},{}) VALUES (%s, %s)".format(SubCommTableName, SubCommTableFields[0], SubCommTableFields[1])
			# print(sql)
			for s in Corrected_DistrictNames:
				try:
					v = ( "{}".format(val), str(s))
					cursor.execute(sql,v)
					connection.commit()
					# print('Value added!!!')
				except Exception as e:
					pass
					# print('Value exists!!!')
		District_with_sub_comm.update({states : distt_value})
		Sub_Commodity_TableFields.update({states : sub_comm_value_tablefield})
		sub_commodities_table.update({Db_Table_name:list(Table_list)})
		DB_sub_commodities_table.update({Db_Table_name: (set_Db_table_name)})

	return sub_commodities_table, DB_sub_commodities_table, District_with_sub_comm, Sub_Commodity_TableFields




def CreateStateTables(path, StateNames, ParentTable, ParentTableField, CommodityType):	
	state_to_commodity = {}
	state_to_TableField = {}
	DB_State_Table = {}
	
	for states in StateNames:
		Statepath = path + "/{}".format(states)
		CommodityNames = helpsql.Directory(Statepath)
		Corrected_CommodityNames = []
		
		for name in CommodityNames:
			name = helpsql.FilterStateName(name)
			Corrected_CommodityNames.append(name)

		statename = helpsql.FilterStateName(states)
		StateTableName = "{}_{}".format(ParentTable, statename)
		StateTableFields = [ 'State_{}_{}'.format(CommodityType,statename), "Sub_{}".format(CommodityType) ]
		DB_State_Table.update({states : StateTableName})
		
		# cursor.execute("DROP TABLE {}".format(StateTableName))
		cursor.execute("SHOW TABLES LIKE '{}';".format(StateTableName))
		result = cursor.fetchone()
		if result:
			pass
			print("State-Table {} exists!!!".format(StateTableName))
		else:
			cursor.execute("CREATE TABLE {} ({} VARCHAR(255), {} VARCHAR(255) PRIMARY KEY);".format( StateTableName, StateTableFields[0], StateTableFields[1] ))
			cursor.execute("ALTER TABLE {} ADD CONSTRAINT {} FOREIGN KEY ({}) REFERENCES {}({});".format( StateTableName, StateTableFields[0], StateTableFields[0], ParentTable, ParentTableField[1]))
			print("{} Table Created!!!".format(StateTableName))
		
		if StateTableName not in ALL_TABLES:
			ALL_TABLES.append(StateTableName)
			ALL_STATE_TABLE.append(StateTableName)

		sql = "INSERT INTO {} ({},{}) VALUES (%s, %s)".format(StateTableName, StateTableFields[0], StateTableFields[1])
		
		for s in Corrected_CommodityNames:
			try:
				val = ( "{}".format(states), str(s))
				cursor.execute(sql,val)
				connection.commit()
				# print('Value added!!!')
			except Exception as e:
				pass
				# print('Value exists!!!')

		state_to_commodity.update({states:Corrected_CommodityNames})
		state_to_TableField.update({statename :StateTableFields})
		
	return state_to_commodity, state_to_TableField, DB_State_Table




def CreateCommoditiesTable(path, MainTable, MainTableFields, Tablepath, Tablename):
	path = path + '/{}'.format(Tablepath)
	StateNames = helpsql.Directory(path)
	TableFields = ['{}_Type_Commodity'.format(Tablepath),'State']
	
	# cursor.execute("DROP TABLE {}".format(Tablename))
	cursor.execute("SHOW TABLES LIKE '{}';".format(Tablename))
	result = cursor.fetchone()
	if result:
		pass
		print("Commodity-Table {} exists!!!".format(Tablename))
	else:
		cursor.execute("CREATE TABLE {} ({} VARCHAR(255), {} VARCHAR(255) PRIMARY KEY);".format( Tablename, TableFields[0], TableFields[1] ))
		cursor.execute("ALTER TABLE {} ADD CONSTRAINT {} FOREIGN KEY ({}) REFERENCES {}({});".format( Tablename, TableFields[0], TableFields[0], MainTable, MainTableFields[0]))
		print("{} Table Created!!!".format(Tablename))
	
	if Tablename not in ALL_TABLES:
		ALL_TABLES.append(Tablename)
		ALL_COMMODITIES_TABLE.append(Tablename)

	sql = "INSERT INTO {} ({},{}) VALUES (%s, %s)".format(Tablename, TableFields[0], TableFields[1])
	# print(sql)
	for s in StateNames:
		try:
			val = ("{}".format(Tablepath), str(s))
			cursor.execute(sql,val)
			# print('Value added!!!')
			connection.commit()
		except Exception as e:
			pass
			# print('Value exists!!!')
	Table_associated_with_MainTable_in_DB.update()

	return StateNames, TableFields, path




def MainTable(path, table, TableField):
	# cursor.execute("DROP TABLE {}".format(table))		
	cursor.execute("SHOW TABLES LIKE '{}';".format(table)) # Check wheather table already existed or not?
	result = cursor.fetchone()
	if result:
		pass
		print("Main-Table {} exists!!!".format(table)) # If Table Exists then it will skip the process to create the table
	else:
		cursor.execute("CREATE TABLE {} ({} VARCHAR(255) PRIMARY KEY)".format(table, TableField[0]))
		print("{} Table Created!!!".format(table))
	
	schema = helpsql.Directory(path)
	if table not in ALL_TABLES:
		ALL_TABLES.append(table)

	sql = "INSERT INTO {} ({}) VALUES (%s)".format(table, TableField[0]) # Insert values in the table
	# print(schema)
	for s in schema:
		try:
			cursor.execute(sql,str(s))
			# print('Value added!!!')
			connection.commit()
		except Exception as e:
			pass
			# print('Value exists!!!')

	return schema, TableField


			

MainPath = '/home/ranjeet/Downloads/CDAC/Commodity Price Prediction/6. Schemas'
MainTableName = 'COMMODITIES'
MainTableNameField = ['Commodity']
Oil = "Oil"
Pulses = "Pulses"
Oiltable = 'OIL'
Pulsetable = 'PULSE'




MainTable_Value, MainTable_field = MainTable(MainPath, MainTableName, MainTableNameField)
Table_associated_with_MainTable_in_DB.update({MainTable_Value[0]:Pulsetable})
Table_associated_with_MainTable_in_DB.update({MainTable_Value[1]:Oiltable})
# print("------------------------------------------------------------------------------------------")
# print("Values in the {} Table are : \n{} \n".format(MainTableName, MainTable_Value))
# print("------------------------------------------------------------------------------------------")
# print("Table Names in DataBase associated with {} : ".format(MainTableName))
# print("------------------------------------------------------------------------------------------")
# dict_print(Table_associated_with_MainTable_in_DB)




OilTable_Value, OilTable_Field, OilPath = CreateCommoditiesTable(MainPath, MainTableName, MainTableNameField, Oil, Oiltable)
# Table_associated_with_State_Oil_Table = {}
# Table_associated_with_State_Oil_Table.update( { Oiltable : OilTable_Value})
# print("------------------------------------------------------------------------------------------")
# print("Values in the {} Table are : \n{}\n".format(Oiltable, OilTable_Value))

Oil_StateTable_Values, Oil_StateTable_Fields, Table_associated_with_State_Oil_Table_in_DB = CreateStateTables(OilPath, OilTable_Value, Oiltable, OilTable_Field, Oil)
# print("------------------------------------------------------------------------------------------")
# print("Values in the Oil-State Table are : \n{}\n".format (Oil_StateTable_Values))
# print("------------------------------------------------------------------------------------------")
# print("Table Names in DataBase associated with {} : ".format(Oiltable))
# print("------------------------------------------------------------------------------------------")
# dict_print(Table_associated_with_State_Oil_Table_in_DB)

Sub_Oil_Table_Values, Sub_oil_table, sub_oils_DB_table, Sub_oil_table_Fields = CreateSubCommoditiesTables(OilPath, OilTable_Value, Oiltable, Oil_StateTable_Values, Oil_StateTable_Fields, Oil)
# print("------------------------------------------------------------------------------------------")
# print("Values in the Sub-Oil Tables are : \n{}\n".format(Sub_Oil_Table_Values))
# print("------------------------------------------------------------------------------------------")
# print("Values in the {} Table are : \n{}\n".format(Oiltable, Sub_oil_table))
# print("------------------------------------------------------------------------------------------")
# dict_print(sub_oils_DB_table)
# print("------------------------------------------------------------------------------------------")
# print(Sub_oil_table_Fields)

CreateDistrictTables(OilPath, OilTable_Value, Sub_Oil_Table_Values, Oil, Sub_oil_table_Fields)




PulseTable_Value, PulseTable_Field, PulsePath = CreateCommoditiesTable(MainPath, MainTableName, MainTableNameField, Pulses, Pulsetable)
# # Table_associated_with_State_Pulse_Table = {}
# # Table_associated_with_State_Pulse_Table.update( { Pulsetable : PulseTable_Value})
# # print("------------------------------------------------------------------------------------------")
# # print("Values in the {} Table are : \n{}\n".format(Pulsetable, PulseTable_Value))

Pulse_StateTable_Values, Pulse_StateTable_Fields, Table_associated_with_State_Pulse_Table_in_DB = CreateStateTables(PulsePath, PulseTable_Value, Pulsetable, PulseTable_Field, Pulses)
# # print("------------------------------------------------------------------------------------------")
# # print("Values in the Pulse-State Table are : \n{}\n".format (Pulse_StateTable_Values))
# # print("------------------------------------------------------------------------------------------")
# # print("Table Names in DataBase associated with {} : ".format(Pulsetable))
# # print("------------------------------------------------------------------------------------------")
# # dict_print(Table_associated_with_State_Pulse_Table_in_DB)

Sub_Pulse_Table_Values, Sub_pulse_table, sub_pulse_DB_table, Sub_pulse_table_Fields = CreateSubCommoditiesTables(PulsePath, PulseTable_Value, Pulsetable, Pulse_StateTable_Values, Pulse_StateTable_Fields, Pulses)
# print("------------------------------------------------------------------------------------------")
# print("Values in the Sub-Pulse Tables are : \n{}\n".format(Sub_Pulse_Table_Values))
# print("------------------------------------------------------------------------------------------")
# print("Values in the {} Table are : \n{}\n".format(Pulsetable, Sub_pulse_table))
# print("------------------------------------------------------------------------------------------")
# dict_print(sub_pulse_DB_table)

CreateDistrictTables(PulsePath, PulseTable_Value, Sub_Pulse_Table_Values, Pulses, Sub_pulse_table_Fields)



# All_tables()
print(len(ALL_TABLES))
# Close the Connection
connection.close();

