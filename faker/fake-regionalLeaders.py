from faker import Faker
from faker.providers import internet
from pymongo import MongoClient
from pymongo import UpdateOne
from pymongo import UpdateMany

mongo_user = #SECRET
mongo_pwd = #SECRET

pop_list = ['None', 'unclaimed']

fake = Faker()
fake.add_provider(internet)

client = MongoClient('mongodb+srv://'+mongo_user+':'+mongo_pwd+'@lasagna-class-project-d.ljwaj.mongodb.net/endless-pastabilities?retryWrites=true&w=majority')['endless-pastabilities']

cName = 'regions'

if __name__ == "__main__":
    c = client.get_collection(cName)
    existingName = list(c.distinct("Regional Leader"))

    for p in pop_list:
        existingName.pop(existingName.index(p))

    newName = []
    for n in existingName:
        w = fake.name()
        newName.append(
            UpdateMany({'Regional Leader': n},
                        {'$set':
                            {'Regional Leader':w}}))
        print(n + " : " + w)
    c.bulk_write(newName)
