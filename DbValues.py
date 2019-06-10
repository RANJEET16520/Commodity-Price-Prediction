import os
import sys
import pandas as pd

Commodity_Values = [['Comm_Oil_GdN', 'Groundnut', 'Oil'],
					['Comm_Oil_Msd', 'Mustard', 'Oil'],
					['Comm_Oil_SfF', 'Safflower', 'Oil'],
					['Comm_Oil_Sbn'	, 'Soyabean', 'Oil'],
					['Comm_Oil_SnF', 'Sunflower', 'Oil'],
					['Comm_Pulse_Arh', 'Arhar', 'Pulses'],
					['Comm_Pulse_BngGr', 'BengalGram', 'Pulses'],
					['Comm_Pulse_BlkGr', 'BlackGram', 'Pulses'],
					['Comm_Pulse_GnGr', 'GreenGram', 'Pulses'],
					['Comm_Pulse_Lntl', 'Lentil', 'Pulses'],
					]

State_Values = [['S_1_AP', 'Andhra Pradesh'],
				['S_2_AS', 'Assam'],
				['S_3_BH', 'Bihar'],
				['S_4_CG', 'chattisgarh'],
				['S_5_GJ', 'Gujarat'],
				['S_6_HR', 'Haryana'],
				['S_7_HP', 'Himachal Pradesh'],
				['S_8_JK', 'Jammu and Kashmir'],
				['S_9_JH', 'Jharkhand'],
				['S_10_KA', 'karnataka'],
				['S_11_KL', 'kerala'],
				['S_12_MP', 'Madhya Pradesh'],
				['S_13_MH', 'Maharashtra'],
				['S_14_MN', 'Manipur'],
				['S_15_MG', 'Meghalaya'],
				['S_16_MZ', 'Mizoram'],
				['S_17_NG', 'Nagaland'],
				['S_18_NcrDel', 'NCT of Delhi'],
				['S_19_OS', 'Orissa'],
				['S_20_PO', 'Pondicherry'],
				['S_21_PB', 'Punjab'],
				['S_22_RJ', 'Rajasthan'],
				['S_23_TN', 'Tamil Nadu'],
				['S_24_TS', 'Telangana'],
				['S_25_TP', 'Tripura'],
				['S_26_UP', 'Uttar Pradesh'],
				['S_27_UK', 'Uttrakhand'],
				['S_28_WB', 'West Bengal'],
				]


cwd = '/home/ranjeet/Downloads/CDAC/Commodity Price Prediction/6. Schemas'
City = []
Mandi = []
def City_Values():	
	City_dict = {}
	count = 0

	for comm in os.listdir(cwd):
		s_path = cwd + '/{}'.format(comm)

		for state in os.listdir(s_path):
			sub_path = s_path + '/{}'.format(state)
			if state not in City_dict:
				City_dict[state] = []

			for sub_comm in os.listdir(sub_path):
				city_path = sub_path + '/{}'.format(sub_comm)

				for city in os.listdir(city_path):
					if city not in City_dict[state]:
						City_dict[state].append(city)
						count+=1
	# print(count)
	
	for key, value in City_dict.items():
		for lis in State_Values:
			if key in lis:
				cv = lis[0]
				_, __, cv1 = cv.split('_')
		
				i = 0
				for val in  value:
					i+=1
					c_id = 'City_{}_{}'.format(cv1,i)
					actCV = [c_id, val, cv]
					City.append(actCV)

	# print(len(City))
	# s = set()
	# for lis in City:
	# 	s.add(lis[0])
	# print(len(s))
	
	return City

def Mandi_Values():
	File_dict = {}
	count = 0
	# City = City_Values()

	for comm in os.listdir(cwd):
		s_path = cwd + '/{}'.format(comm)

		for state in os.listdir(s_path):
			sub_path = s_path + '/{}'.format(state)
			if state not in File_dict:
				File_dict[state] = {}

			for sub_comm in os.listdir(sub_path):
				city_path = sub_path + '/{}'.format(sub_comm)

				for city in os.listdir(city_path):
					mandi_path = city_path + '/{}'.format(city)
					if city not in File_dict[state]:
						File_dict[state].update({city:[]})

					for _, _, files in os.walk(mandi_path):

						for file in files:
							f_name, _ = file.split('.')
							
							if f_name not in File_dict[state][city]:
								File_dict[state][city].append(f_name)
								count+=1

	# print(count)
	
	for key, val in File_dict.items():
		for k, v in val.items():
			for lis in City:
				if k in lis:
					cv = lis[0]
					cvv1, cvv2, cvv3 = cv.split('_')

					i=0
					for vv in v:
						i+=1
						m_id = 'Mandi_{}_{}_{}_{}'.format(i, cvv1, cvv3, cvv2)
						actMV = [m_id, vv, cv]
						Mandi.append(actMV)
					break

	# print(len(Mandi))
	# s = set()
	# for lis in Mandi:
	# 	s.add(lis[0])
	# print(len(s))
	return Mandi


def Price_values():
	Price_Dict = {}
	MAIN_LIST = []
	count = 0

	# Mandi = Mandi_Values()
	
	for comm in os.listdir(cwd):
		s_path = cwd + '/{}'.format(comm)

		for state in os.listdir(s_path):
			sub_path = s_path + '/{}'.format(state)
			if state not in Price_Dict:
				Price_Dict[state] = {}

			for sub_comm in os.listdir(sub_path):
				city_path = sub_path + '/{}'.format(sub_comm)

				for city in os.listdir(city_path):
					mandi_path = city_path + '/{}'.format(city)
					if city not in Price_Dict[state]:
						Price_Dict[state].update({city:{}})

					for _, _, files in os.walk(mandi_path):

						for file in files:
							df_path = mandi_path + '/{}'.format(file)
							f_name, _ = file.split('.')
							if f_name not in Price_Dict[state][city]:
								Price_Dict[state][city].update({f_name:[]})
							
							if sub_comm not in Price_Dict[state][city][f_name]:
								Price_Dict[state][city][f_name].append(sub_comm)
								# count+=1

								for lis1 in Commodity_Values:
									if sub_comm in lis1:
										com_id = lis1[0]
										
										for lis2 in Mandi:
											if f_name in lis2:
												m_id = lis2[0]
												# print('{}:{}, {}:{}'.format(sub_comm, com_id, f_name, m_id))
												com_id_list = com_id.split('_')
												m_id_list = m_id.split('_')
												# print('{}:{}, {}:{}'.format(sub_comm, com_id_list, f_name, m_id_list))
												
												df = pd.read_csv(df_path)
												df = pd.DataFrame(df)

												Sum = df['arrivalquantity'].isnull().sum()
												df['arrivalquantity'] = df['arrivalquantity'].fillna(value = 0.0)

												if Sum>0:
													count+=Sum
													
												df_list = df.values.tolist()
												# print(df_list)

												i = 0
												for lis3 in df_list:
													if lis3 is None:
														break
													i += 1
													lis3 = lis3[1:]
													# print(lis3)
													main_id = '{}_{}_val_{}_{}'.format(com_id_list[2], com_id_list[1], i, m_id)
													# print(main_id)

													CURRENT_LIST = [main_id, m_id, com_id]

													for vvvv in lis3:
														if vvvv is "":
															print(vvvv)
														CURRENT_LIST.append(vvvv)
													# print(CURRENT_LIST)
													MAIN_LIST.append(CURRENT_LIST)								

	print(count)							
	print(len(MAIN_LIST))
	s = set()
	for lis in MAIN_LIST:
		s.add(lis[0])
	print(len(s))
	# for Big_key, Big_value in Price_Dict.items():
	# 	print(Big_key)
	# 	for key, value in Big_value.items():
	# 		print(key)
	# 		for k,v in value.items():
	# 			print('{}:{}'.format(k,v))
	return MAIN_LIST


# Price_values()