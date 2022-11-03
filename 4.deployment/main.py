import pandas as pd
import joblib


dict={'type':"house", 'subtype':"house", 'KitchenType':"hyperequipped",'Building_condition':'asnew',
          'energy_heatingType':"gas", "Energy Consumption Level":299, 'bedroom_count':3, 'Land_surface':500,
                  'Attic_Exists':1, 'Basement_Exists':1, 'Garden_surface':250, 'Outdoor_terrace_exists':1,
                  'Wellness Equipment Swimming Pool':1, 'Parking Space Count indoor':1, 'Parking SpaceCount outdoor':2,
            'Condition is Newly Built':1, 'province':'Vlaanderen'}

def prediction(dict):
    df=pd.DataFrame([dict])
    filename = "./finalized_model.sav"
    loaded_model = joblib.load(filename)
    predicted_price = loaded_model.predict(df)
    return predicted_price[0]

