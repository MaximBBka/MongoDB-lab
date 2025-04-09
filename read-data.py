from pymongo import MongoClient
from pprint import pprint

client = MongoClient("mongodb://root:example123@localhost:27017/")
db = client["practice_db"]
collection = db["users"]

def show_all_users():
    print("\n=== Все пользователи ===")
    for user in collection.find().sort("user_id"):
        pprint(user)

def show_adults():
    print("\n=== Пользователи старше 30 ===")
    for user in collection.find({"age": {"$gt": 30}}):
        print(f"{user['name']} ({user['age']} лет)")

def count_skills():
    pipeline = [
        {"$unwind": "$skills"},
        {"$group": {"_id": "$skills", "count": {"$sum": 1}}}
    ]
    print("\n=== Статистика по навыкам ===")
    for skill in collection.aggregate(pipeline):
        print(f"{skill['_id']}: {skill['count']} пользователей")

try:
    show_all_users()
    show_adults() 
    count_skills()
except Exception as e:
    print(f"❌ Ошибка: {e}")
finally:
    client.close()