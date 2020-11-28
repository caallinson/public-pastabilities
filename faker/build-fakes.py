import lob
from geocodio import GeocodioClient
from faker import Faker
from faker.providers import internet
from pymongo import MongoClient
import numpy as np
import pandas as pd
import json
import datetime

lob.api_key = #SECRET
geocodio_key = #SECRET

mongo_user = #SECRET
mongo_pwd = #SECRET

fake = Faker()
fake.add_provider(internet)

geocodio = GeocodioClient(geocodio_key)

client = MongoClient('mongodb+srv://'+mongo_user+':'+mongo_pwd+'@lasagna-class-project-d.ljwaj.mongodb.net/endless-pastabilities?retryWrites=true&w=majority')

def build_requestors(build_num, base_lat, base_long, radius, cohort=None):
    """
    Build Number, Base Latitude, Base Longitude, Radius, Cohort (optional)
    """
    col_names = ['name', 'address', 'city', 'state', 'zip_code', 
                'email', 'phone',
                'special_veg', 'special_vgn', 'special_dairy', 'special_gluten', 
                'special_nut', 'special_other', 'describe', 'lat', 'long', 
                'lasagna_mama', 'date_delivered', 'cohort', 'active', 'num_adults',
                'num_kids', 'quantity']

    df = pd.DataFrame(columns=col_names, index=list(range(build_num)))

    for i in range(build_num):

        noise = np.random.normal(0, radius/200, 2)
        new_lat = base_lat + noise[0]
        new_long = base_long + noise[1]

        reverse_address = geocodio.reverse((new_lat, new_long))

        if 'number' in reverse_address.best_match['address_components']:
            df.loc[i, 'name'] = fake.name()
            df.loc[i, 'address'] = reverse_address.best_match['address_components']['number'] + ' ' + reverse_address.best_match['address_components']['formatted_street']
            df.loc[i, 'city'] = reverse_address.best_match['address_components']['city']
            df.loc[i, 'state'] = reverse_address.best_match['address_components']['state']
            df.loc[i, 'zip_code'] = reverse_address.best_match['address_components']['zip']

            df.loc[i, 'email'] = fake.email()
            df.loc[i, 'phone'] = fake.phone_number()

            df.loc[i, 'lat'] = new_lat
            df.loc[i, 'long'] = new_long

            served = np.random.randint(0, high=100)
            df.loc[i, 'quantity'] = 0
            if served < 10:
                df.loc[i, 'lasagna_mama'] = fake.name()
            elif served < 20:
                df.loc[i, 'lasagna_mama'] = fake.name()
                df.loc[i, 'date_delivered'] = str(datetime.datetime.now() - datetime.timedelta(weeks=np.random.randint(0,high=6)))
            elif served < 30:
                df.loc[i, 'date_delivered'] = str(datetime.datetime.now() - datetime.timedelta(weeks=np.random.randint(0,high=6)))
            else:
                df.loc[i, 'quantity'] = 1 #int(max(1,np.random.normal(0,2)+1))

            df.loc[i, 'special_veg'] = (np.random.randint(0, high = 10) > 7)
            df.loc[i, 'special_vgn'] = (np.random.randint(0, high = 10) > 7)
            df.loc[i, 'special_dairy'] = (np.random.randint(0, high = 10) > 7)
            df.loc[i, 'special_gluten'] = (np.random.randint(0, high = 10) > 7)
            df.loc[i, 'special_nut'] = (np.random.randint(0, high = 10) > 7)
            df.loc[i, 'special_other'] = (np.random.randint(0, high = 10) > 8)
            df.loc[i, 'num_adults'] = np.random.randint(1,high=3)
            df.loc[i, 'num_kids'] = np.random.randint(0,high=6)

            df.loc[i, 'active'] = True

            df.loc[i, 'describe'] = 'none'

            if cohort is None:
                df.loc[i, 'cohort'] = df.loc[i, 'city']
            else:
                df.loc[i, 'cohort'] = cohort

    return df


def build_suppliers(build_num, base_lat, base_long, radius, cohort=None):
    """
    Build Number, Base Latitude, Base Longitude, Radius, Cohort (optional)
    """
    col_names = ['name', 'address', 'city', 'state', 'zip_code', 
                'email', 'phone', 'frequency',
                'special_veg', 'special_vgn', 'special_dairy', 'special_gluten', 
                'special_nut', 'special_other', 'lat', 'long', 'miles', 'cohort', 'url', 'active', 'quantity']

    df = pd.DataFrame(columns=col_names, index=list(range(build_num)))

    for i in range(build_num):

        noise = np.random.normal(0, radius/200, 2)
        new_lat = base_lat + noise[0]
        new_long = base_long + noise[1]

        reverse_address = geocodio.reverse((new_lat, new_long))

        if 'number' in reverse_address.best_match['address_components']:
            df.loc[i, 'name'] = fake.name()
            df.loc[i, 'address'] = reverse_address.best_match['address_components']['number'] + ' ' + reverse_address.best_match['address_components']['formatted_street']
            df.loc[i, 'city'] = reverse_address.best_match['address_components']['city']
            df.loc[i, 'state'] = reverse_address.best_match['address_components']['state']
            df.loc[i, 'zip_code'] = reverse_address.best_match['address_components']['zip']

            df.loc[i, 'email'] = fake.email()
            df.loc[i, 'phone'] = fake.phone_number()
            df.loc[i, 'url'] = 'https://bit.ly/3nrat6E'

            df.loc[i, 'lat'] = new_lat
            df.loc[i, 'long'] = new_long

            freq = np.random.randint(0, high=100)
            if freq < 10:
                df.loc[i, 'frequency'] = 'just this once'
            elif freq < 50:
                df.loc[i, 'frequency'] = 'each week'
            elif freq < 75:
                df.loc[i, 'frequency'] = 'every other week'
            else:
                df.loc[i, 'frequency'] = 'once a month'

            df.loc[i, 'miles'] = int(np.random.normal(5, 2))
            df.loc[i, 'special_veg'] = (np.random.randint(0, high = 10) > 7)
            df.loc[i, 'special_vgn'] = (np.random.randint(0, high = 10) > 7)
            df.loc[i, 'special_dairy'] = (np.random.randint(0, high = 10) > 7)
            df.loc[i, 'special_gluten'] = (np.random.randint(0, high = 10) > 7)
            df.loc[i, 'special_nut'] = (np.random.randint(0, high = 10) > 7)
            df.loc[i, 'special_other'] = (np.random.randint(0, high = 10) > 8)
            df.loc[i, 'quantity'] = int(max(1,np.random.normal(0,1)+3))

            if (np.random.randint(0, high = 10) > 8):
                df.loc[i, 'active'] = False
                df.loc[i, 'quantity'] = 0
            else:
                df.loc[i, 'active'] = True

            if cohort is None:
                df.loc[i, 'cohort'] = df.loc[i, 'city']
            else:
                df.loc[i, 'cohort'] = cohort

    return df

def push_requestors(df, destructive=False):
    collection = client['endless-pastabilities']
    if destructive:
        collection.garfield.drop()
    post = df.dropna(subset=['name', 'lat', 'long']).to_json(orient='records')
    print('Garfields:')
    print(df.head())
    collection.garfield.insert_many(json.loads(post))

def push_suppliers(df, destructive=False):
    collection = client['endless-pastabilities']
    if destructive:
        collection.mama.drop()
    post = df.dropna(subset=['name', 'lat', 'long']).to_json(orient='records')
    print('Mamas:')
    print(df.head())
    collection.mama.insert_many(json.loads(post))

def update_quantities():
    collection = client['endless-pastabilities']
    for item in collection.garfield.find(projection={"_id"}):
        collection.garfield.update_one(item, {'$set' : {'quantity': int(max(1,np.random.normal(0,2)+1))}})
    for item in collection.mama.find(projection={"_id"}):
        collection.mama.update_one(item, {'$set' : {'quantity': int(max(1,np.random.normal(0,1)+3))}})

def add_request_dates():
    collection = client['endless-pastabilities']
    for item in collection.garfield.find(projection={"_id"}):
        r = int(7*np.random.default_rng().normal(0, 1))
        d = datetime.date.today() - datetime.timedelta(days=r)
        collection.garfield.update_one(item, {'$set' : {'request_date': str(d)}})

if __name__ == "__main__":

    # (garf, mama) = (np.random.randint(100, high=300), np.random.randint(20, high=100))
    # print('Making ' + str(garf) + ' Garfields and ' + str(mama) + ' Mamas')
    # df_req = build_requestors(garf, 42.3760734, -71.1341768, 5, 'boston')
    # df_sup = build_suppliers(mama, 42.3760734, -71.1341768, 5, 'boston')
    # push_requestors(df_req, destructive=True)
    # push_suppliers(df_sup, destructive=True)

    # (garf, mama) = (np.random.randint(100, high=300), np.random.randint(20, high=100))
    # print('Making ' + str(garf) + ' Garfields and ' + str(mama) + ' Mamas')
    # df_req = build_requestors(garf, 37.8759058, -122.2522485, 15, 'bae area')
    # df_sup = build_suppliers(mama, 37.8759058, -122.2522485, 15, 'bae area')
    # push_requestors(df_req, destructive=False)
    # push_suppliers(df_sup, destructive=False)

    # (garf, mama) = (np.random.randint(100, high=300), np.random.randint(20, high=100))
    # print('Making ' + str(garf) + ' Garfields and ' + str(mama) + ' Mamas')
    # df_req = build_requestors(garf, 29.7484656, -95.3823262, 15, 'houston')
    # df_sup = build_suppliers(mama, 29.7484656, -95.3823262, 15, 'houston')
    # push_requestors(df_req, destructive=False)
    # push_suppliers(df_sup, destructive=False)

    # (garf, mama) = (np.random.randint(100, high=300), np.random.randint(20, high=100))
    # print('Making ' + str(garf) + ' Garfields and ' + str(mama) + ' Mamas')
    # df_req = build_requestors(garf, 39.0184608, -77.2689106, 10, 'DC')
    # df_sup = build_suppliers(mama, 39.0184608, -77.2689106, 10, 'DC')
    # push_requestors(df_req, destructive=False)
    # push_suppliers(df_sup, destructive=False)

    # df_req = build_requestors(20, 39.0184608, -77.2689106, 10, 'faker-DC')
    # df_sup = build_suppliers(10, 39.0184608, -77.2689106, 10, 'faker-DC')
    # push_requestors(df_req, destructive=False)
    # push_suppliers(df_sup, destructive=False)

    #update_quantities()

    add_request_dates()
