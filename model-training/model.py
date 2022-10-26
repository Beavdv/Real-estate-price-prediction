import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error

df = pd.read_csv('original1.csv')
df.isnull().sum()
df.drop('Specificities SME office exists', axis=1, inplace=True)
df.drop('Transaction Type', axis=1, inplace=True)
df.drop('date', axis=1, inplace=True)
df=df[~df['price'].str.contains('-')]
df.drop(df[df['zip'] == 0].index, inplace=True)

#clean data
df = df.replace(np.nan, 0)
df['Condition is Newly Built'] = df['Condition is Newly Built'].replace(['1.'], 'True')

#change preprocess data
df['zip'] = df['zip'].astype('int')
def new_col_provinces(col):
    if col >= 9000:
        return 'Oost - Vlaanderen'
    if col >= 8000:
        return 'West-Vlaanderen'
    if col >= 7000:
        return 'Hainaut'
    if col >= 6600:
        return 'Luxembourg'
    if col >= 6000:
        return 'Hainaut'
    if col >= 5000:
        return 'Namur'
    if col >= 4000:
        return 'Liege'
    if col >= 3500:
        return 'Limburg'
    if col >= 3000:
        return 'Vlaams-Brabant'
    if col >= 2000:
        return 'Antwerpen'
    if col >= 1501:
        return 'Vlaams-Brabant'
    if col >= 1300:
        return 'Brabon Wallon'
    if col >= 1000:
        return 'Brussel'
df['province'] =pd.DataFrame(df['zip'].apply(new_col_provinces))
df['price'] = df['price'].astype('int')

def new_col_price(col):
    if col >= 2000000:
        return 'more then 2000000'
    if col >= 1500000:
        return 'between 2000000 and 1500000'
    if col >= 1000000:
        return 'between 100000 and 1500000'
    if col >= 500000:
        return 'between 500000 and 1000000'
    if col >= 400000:
        return 'between 400000 and 500000'
    if col >= 300000:
        return 'between 300000 and 400000 '
    if col >= 200000:
        return 'between 200000 and 300000'
    if col >= 100000:
        return 'between 100000 and 200000'
    if col < 100000:
        return 'below 100000'

df['price_cat'] =pd.DataFrame(df['price'].apply(new_col_price))

df=pd.get_dummies(df, columns=['price_cat'], prefix='price_cat')
df=pd.get_dummies(df, columns=['province'], prefix='province')
df=pd.get_dummies(df, columns=['KitchenType'], prefix='KitchenType')
df=pd.get_dummies(df, columns=['Building condition'], prefix='Building condition')
df=pd.get_dummies(df, columns=['energy_heatingType'], prefix='energy_heatingType')
df=pd.get_dummies(df, columns=['type'], prefix='type')
df=pd.get_dummies(df, columns=['subtype'], prefix='subtype')

X = df.drop('price', axis=1)
y = df["price"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
regressor=LinearRegression()
regressor.fit(X_train, y_train)
y_pred = regressor.predict(X_test)
df_preds = pd.DataFrame({'Price': y_test.squeeze(), 'Predicted Price': y_pred.squeeze()})

print(
  'mean_squared_error : ', mean_squared_error(y_test, y_pred))
print(
  'mean_absolute_error : ', mean_absolute_error(y_test, y_pred))
print(regressor.score(X_test, y_test))








































































































































































































































