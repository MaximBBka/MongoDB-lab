from pymongo import MongoClient
from datetime import datetime
import random

# Подключение к MongoDB (используем те же credentials, что и в docker-compose)
client = MongoClient("mongodb://root:example123@localhost:27017/")
db = client["practice_db"]  # Создаём/выбираем базу для практики
collection = db["users"]    # Коллекция "users"

# Генерация тестовых данных
users = []
for i in range(1, 6):
    user = {
        "user_id": i,
        "name": f"User_{i}",
        "age": random.randint(18, 60),
        "email": f"user_{i}@test.com",
        "registration_date": datetime.now(),
        "skills": ["Python", "MongoDB"] if i % 2 == 0 else ["Java", "SQL"]
    }
    users.append(user)

# Вставка данных с обработкой ошибок
try:
    result = collection.insert_many(users)
    print(f"✅ Вставлено {len(result.inserted_ids)} документов")
    print(f"Первый ID: {result.inserted_ids[0]}")
except Exception as e:
    print(f"❌ Ошибка: {e}")
finally:
    client.close()