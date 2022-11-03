import requests


dict = {'type': "house", 'subtype': "house", 'KitchenType': "hyperequipped", 'Building_condition': 'asnew',
           'energy_heatingType': "gas",
           "Energy Consumption Level": 299, 'bedroom_count': 3, 'Land_surface': 500,
           'Attic_Exists': 1, 'Basement_Exists': 1, 'Garden_surface': 250, 'Outdoor_terrace_exists': 1,
           'Wellness Equipment Swimming Pool': 1, 'Parking Space Count indoor': 1, 'Parking SpaceCount outdoor': 2,
           'Condition is Newly Built': 1, 'province': 'Vlaanderen'}
r = requests.post('http://127.0.0.1:5000/predict',dict)
print(r.text)