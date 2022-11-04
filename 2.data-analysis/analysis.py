from tabulate import tabulate
import pandas as pd
import matplotlib.pyplot as plt


filename = "./original.csv"
my_data=pd.read_csv(filename)
print(tabulate(my_data.head(), headers=my_data.columns))
my_data.info()
data_for_graf = my_data[["price","zip","date"]]
data_for_graf.plot(kind='hist')
plt.interactive(True)
plt.title('Price of houses for sale per region')
plt.xlabel('price')
plt.ylabel('region')
plt.show()

