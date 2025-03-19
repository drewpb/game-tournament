import json
from faker import Faker
import random

fake = Faker()

data = []

for _ in range(10000):
    jugador = {
        "model": "catalog.jugador",
        "fields": {
            "nombre": fake.name(),
            "email": fake.email(),
            "dni": fake.unique.random_number(digits=8, fix_len=True),
            "telefono": fake.phone_number(),
            "alias": fake.user_name(),
            "estadisticas": {
                "partidas_ganadas": random.randint(0, 100),
                "partidas_perdidas": random.randint(0, 100),
                "nivel": random.randint(1, 10),
            }
        }
    }
    data.append(jugador)

with open('jugadores.json', 'w') as f:
    json.dump(data, f)

print("Fixture generado con éxito.")
