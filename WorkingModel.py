hostname = 'localhost'
username = 'root'
password = '2000'
database = 'PRICEMODEL'

import os
import sys
import pymysql
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

from statsmodels.tsa.stattools import acf, pacf
import statsmodels.tsa.stattools as ts
from statsmodels.tsa.arima_model import ARIMA

from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Dropout
from sklearn.preprocessing import MinMaxScaler
import functools

# Connecting to the Host
connection = pymysql.connect( host=hostname, user=username, passwd=password, db=database, local_infile=True)
cursor = connection.cursor();
MarketPriceTableName = 'Daily_Market_Price'

Data_list = []
def DBData(Data):
	sql = ("SELECT * FROM {} WHERE Comm_Id = %s and Mandi_Id = %s".format(MarketPriceTableName))
	val = (Data)
	cursor.execute(sql,val)
	records = cursor.fetchall()

	Data_list = []
	for row in records:
		Data_list.append(list(row))
	# print(Data_list[0][:])
	new_list = []
	for lis in Data_list:
		first_id = lis[0]
		# print(first_id)
		key_value = first_id.split('_')
		new_id = int(key_value[3])

		date_id = lis[3]
		new_date = datetime.strptime(date_id, '%Y-%m-%d').date()
		# print(new_date)
		
		new_values = []
		new_values.append(new_id)
		new_values.append(lis[1])
		new_values.append(lis[2])
		new_values.append(new_date)
		new_values.append(lis[4])
		new_values.append(lis[5])
		new_values.append(lis[6])
		new_values.append(lis[7])

		new_list.append(new_values)

	return new_list


def Short(Db_Data):
	df = pd.DataFrame(data = Db_Data, columns = ['Id', 'Mandi_Id', 'Comm_Id', 'ArrivalDate', 'MODALPRICE', 'ArrivalQuantity', 'Temperature', 'Weather'])
	df = df.sort_values('ArrivalDate', ascending=True)
	print(df)

	PRICE = df['MODALPRICE']
	# print(PRICE)
	lnprice=np.log(PRICE)
	price_matrix=lnprice.as_matrix()
	model = ARIMA(price_matrix, order=(0,1,0))
	model_fit = model.fit(disp=0)
	print(model_fit.summary())
	rows,coloums=df.shape
	predictions=model_fit.predict(rows, rows+6, typ='levels')
	predictionsadjusted=np.exp(predictions)
	print(predictions)
	print(predictionsadjusted)
	fig = plt.figure()
	fig.suptitle('Short-Term Predicttion-ARIMA', fontsize = 20)
	plt.plot(predictionsadjusted)
	plt.title('Forecasted Prices')
	plt.xlabel('Days')
	plt.ylabel('Price')
	plt.show()
	return


def Long(Db_Data):
	# dbval = ['Comm_Pulse_BlkGr', 'Mandi_3_City_22_MP']
	# df = WM.DBData(dbval)
	df = pd.DataFrame(data = Db_Data, columns = ['Id', 'Mandi_Id', 'Comm_Id', 'ArrivalDate', 'MODALPRICE', 'ArrivalQuantity', 'Temperature', 'Weather'])
	df = df.sort_values('ArrivalDate', ascending=True)
	df = df.set_index('ArrivalDate')
	# print(df)

	df = df.drop(columns=['Id','Mandi_Id','Comm_Id'])
	df['Weather'] = df['Weather'].map({'clear' : 0.0,'rain' : 1.0})
	cost = df['MODALPRICE']
	cost = pd.DataFrame(cost)
	cost = cost.reset_index()
	cost.ArrivalDate = pd.to_datetime(cost.ArrivalDate)

	cost[['year','month','day']] = cost.ArrivalDate.apply(lambda x: pd.Series(x.strftime("%Y,%m,%d").split(",")))
	print(cost)

	def DaysReturn(month, year):
		if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
			return 31
		elif month == 4 or month == 6 or month == 9 or month == 11:
			return 30
		elif month == 2:
			if year % 100 == 0:
				if year % 400==0:
					return 29
				else:
					return 28
			elif year % 4 == 0:
				return 29
			else:
				return 28  

	def BuildData(df):
		col = ['ArrivalDate', 'MODALPRICE']
		new_df = pd.DataFrame(columns=col)

		cnt = 0
		for i in range(df.shape[0]):
			year = df.iloc[i][0]
			mon = df.iloc[i][1]
			mon_range = DaysReturn(int(mon), int(year))     
			for j in range(1,mon_range+1):
				x = datetime(int(year),int(mon),j)
				x = x.date()
				y = df.iloc[i][2]
				new_df.loc[cnt] = [x] + [y] 
				cnt += 1
		new_df[['year','month','day']] = new_df.ArrivalDate.apply(lambda x: pd.Series(x.strftime("%Y,%m,%d").split(",")))
		new_df.ArrivalDate = pd.to_datetime(new_df.ArrivalDate)
		return new_df


	avgdf = cost.groupby(['year','month']).mean()
	avgdf = avgdf.reset_index()
	modified_cost = BuildData(avgdf)

	# avgdf

	print(modified_cost)

	frames = [cost, modified_cost]
	new_df = pd.concat(frames)

	new_df = new_df.drop_duplicates(['ArrivalDate'])
	new_df = new_df.sort_values('ArrivalDate', ascending=True)
	new_df = new_df.drop(columns=['year','month','day'])

	new_df.reset_index()
	new_df.head(100)

	X = list(new_df['MODALPRICE'])
	print(len(X))

	Data = []
	b_size = 40
	for i in range(0,len(X)-b_size):
		lis = []
		for j in range(b_size):
			lis.append([X[i+j]/10000])
		Data.append(lis)
	Data = np.array(Data, dtype = float)
	print(Data.shape)

	Target = [X[i]/10000 for i in range(b_size, len(X))]
	Target = np.array(Target, dtype = float)
	print(Target.shape)

	x_train, x_test, y_train, y_test = train_test_split(Data, Target, test_size = 0.2, random_state = 2)
	model = Sequential()
	model.add(LSTM(60, input_shape=(x_train.shape[1], x_train.shape[2])))
	model.add(Dense(20))
	model.add(Dense(1))
	model.compile(loss = 'mse', optimizer = 'adam', metrics = ['accuracy'])
	model.summary()

	history = model.fit(x_train, y_train, epochs = 200, batch_size = b_size, validation_data = (x_test, y_test))

	result = model.predict(x_test)
	print(result.shape)
	print(y_test.shape)

	for i in range(0,len(result)):
		print('{} : {}'.format(y_test[i],result[i]))


	# XX = X[:b_size]
	XX = X[len(X)-b_size-10:len(X)-10]
	print(XX)

	predictions = []
	for i in range(40):
		new = [[[XX[j]/10000] for j in range(len(XX)-b_size, len(XX))]]
		new = np.array(new, dtype = float)
		res = model.predict(new)*10000
		predictions.append(res)
		print(res)
		XX.append(res)

	predictionsadjusted = []
	for i in range(len(predictions)):
		for j in predictions[i]:
			predictionsadjusted.append(j)
	predictionsadjusted = predictionsadjusted[10:]

	fig = plt.figure()
	fig.suptitle('Long-Term Predicttion-RNN', fontsize = 20)
	plt.subplot(2,2,1)
	plt.scatter(range(len(result)), result,c = 'r', label = 'Predicted')
	plt.scatter(range(len(y_test)), y_test,c = 'g', label = 'Actual')
	plt.legend()
	plt.title('Predicted Prices')

	plt.subplot(2,2,2)
	plt.plot(history.history['loss'])
	plt.title('Loss')

	plt.subplot(2,2,3)
	plt.plot(history.history['acc'])
	plt.title('Accuracy')

	plt.subplot(2,2,4)
	plt.plot(predictionsadjusted)
	plt.title('Forecasted Prices')
	plt.show()
	return
