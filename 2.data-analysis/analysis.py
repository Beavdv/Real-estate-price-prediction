import matplotlib
from tabulate import tabulate
import pandas as pd
# import numpy
# import seaborn
import matplotlib as mlp
import matplotlib.pyplot as plt
import tkinter
#%matplotlib inline

filename = "./original.csv"
my_data=pd.read_csv(filename)
# my_data=my_data.drop(columns=['user_id', 'user_personal_language', 'classified_id', 'classified_visualisationOption', 'customer_id', 'customer_name',
#                               'classified_certificates_primaryEnergyConsumptionLevel', 'classified_specificities_SME_office_exists', ])
# print(tabulate(my_data.head(), headers=my_data.columns))
# my_data=my_data.drop(columns=['customer_family','customer_groupInfo_id', 'customer_groupInfo_name'])
# print(tabulate(my_data.head(), headers=my_data.columns))
# data=my_data.drop(columns=['user_loginStatus', 'user_personal_language', 'customer_networkInfo_name', 'screen_name', 'screen_language'])
print(tabulate(my_data.head(), headers=my_data.columns))
my_data.info()
data_for_graf = my_data[["price","zip","date"]]
data_for_graf.plot(kind='hist')
plt.interactive(True)
plt.title('Price of houses for sale per region')
plt.xlabel('price')
plt.ylabel('region')
plt.show()