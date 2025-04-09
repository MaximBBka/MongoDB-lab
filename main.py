from pymongo import MongoClient

client = MongoClient("mongodb://root:example123@localhost:27017/")
products_db = client["products-db"] # Создай такую базу
products = products_db["products"] # Создай такую колекцию

# Играйся с командами и синтаксисом.

products.delete_many({})

products.insert_many([
    {
        "name": "Milk",
        "price": 93,
    },
    {
        "name": "Kefir",
        "price": 50,
    }
])

data = products.find({
    "price":{
        "$gt": 40
    }
})

for document in data:
    print(f"{document=}")

