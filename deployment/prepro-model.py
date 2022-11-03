import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error, mean_absolute_error
import joblib

#clean data
df = pd.read_csv('original2.csv')
df.isnull().sum()
df.drop('Specificities SME office exists', axis=1, inplace=True)
df.drop('Transaction Type', axis=1, inplace=True)
df.drop('constructionYear', axis=1, inplace=True)
df.drop('date', axis=1, inplace=True)
df = df[~df['price'].str.contains('-')]
df.dropna(subset=['Energy Consumption Level', 'zip'], inplace=True)
df.drop(df[df['type'] == 'apartmentgroup'].index, inplace=True)
df.drop(df[df['type'] == 'housegroup'].index, inplace=True)

#change/ preprocess/ filling data
df['Condition is Newly Built'] = df['Condition is Newly Built'].replace(['1.'], [1])
df['Condition is Newly Built'] = df['Condition is Newly Built'].fillna(0)
df['KitchenType'] = df['KitchenType'].fillna('notinstalled')
df['Building_condition'] = df['Building_condition'].fillna('torenovate')
df['energy_heatingType'] = df['energy_heatingType'].fillna('varied')
df['Land_surface'] = df['Land_surface'].fillna(0)
df['Attic_Exists'] = df['Attic_Exists'].fillna(0)
df['Attic_Exists'] = df['Attic_Exists'].replace([True], [1])
df['Basement_Exists'] = df['Basement_Exists'].fillna(0)
df['Basement_Exists'] = df['Basement_Exists'].replace([True],[1])
df['Garden_surface'] = df['Garden_surface'].fillna(0)
df['Outdoor_terrace_exists'] = df['Outdoor_terrace_exists'].fillna(0)
df['Outdoor_terrace_exists'] = df['Outdoor_terrace_exists'].replace([True],[1])
df['Wellness Equipment Swimming Pool'] = df['Wellness Equipment Swimming Pool'].fillna(0)
df['Wellness Equipment Swimming Pool'] = df['Wellness Equipment Swimming Pool'].replace([True],[1])
df['Parking Space Count indoor'] = df['Parking Space Count indoor'].fillna(0)
df['Parking Space Count indoor'] = df['Parking Space Count indoor'].replace([True],[1])
df['Parking SpaceCount outdoor'] = df['Parking SpaceCount outdoor'].fillna(0)
df['Parking SpaceCount outdoor'] = df['Parking SpaceCount outdoor'].replace([True],[1])

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
    if col >= 900000:
        return 'between 800000 and 9000000'
    if col >= 800000:
        return 'between 700000 and 8000000'
    if col >= 700000:
        return 'between 600000 and 7000000'
    if col >= 600000:
        return 'between 500000 and 6000000'
    if col >= 500000:
        return 'between 500000 and 1000000'
    if col >= 400000:
        return 'between 500000 and 1000000'
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

X = df.drop('price_cat', axis=1)
X= X.drop('price', axis=1)
X= X.drop('zip', axis=1)
X=X.drop('id',axis=1)
y = df["price"]
print(X.columns)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
X_col_names = list(X_train.columns)
feature_names = X_col_names
categorical_features=["type", "subtype", 'KitchenType','Building_condition',
                  'energy_heatingType','Attic_Exists','Basement_Exists','Outdoor_terrace_exists',
                  'Wellness Equipment Swimming Pool','Condition is Newly Built','province']
numerical_features=['Energy Consumption Level', 'bedroom_count', 'Land_surface', 'Garden_surface',
                        'Parking Space Count indoor','Parking SpaceCount outdoor']
transformer = ColumnTransformer( transformers=[
        ('imputer', SimpleImputer(fill_value='missing'),numerical_features ),
        ('scaler', StandardScaler(),numerical_features),
        ('onehot', OneHotEncoder(drop='first',handle_unknown='ignore'),categorical_features)])
regressor = Pipeline(steps=[("preprocessor", transformer), ("model", LinearRegression())])
regressor.fit(X_train,y_train)
    #test the model
y_pred = regressor.predict(X_test)
    # save the model to disk
filename = 'finalized_model.sav'
joblib.dump(regressor, filename)

#test the model
df_preds = pd.DataFrame({'Price': y_test.squeeze(), 'Predicted Price': y_pred.squeeze()})
print('mean_squared_error : ', mean_squared_error(y_test, y_pred))
print('mean_absolute_error : ', mean_absolute_error(y_test, y_pred))
print(regressor.score(X_test, y_test))
print(y_pred)





