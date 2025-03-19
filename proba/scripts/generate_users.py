from faker import Faker
import random
from proba1.catalog.models import Jugador  # Ajusta la ruta según tu estructura
from django.db import IntegrityError  # Para manejar errores de integridad (violaciones de UNIQUE)

fake = Faker()

# Listas para almacenar los valores generados
generated_emails = set()
generated_aliases = set()
generated_dnis = set()

# Definir cuántos usuarios queremos generar
total_usuarios = 10000
usuarios_creados = 0

while usuarios_creados < total_usuarios:
    try:
        # Generar los datos para un nuevo usuario
        nombre = fake.name()
        email = fake.email()
        dni = fake.unique.random_number(digits=8, fix_len=True)
        telefono = fake.phone_number()
        alias = fake.user_name()

        # Verificar que los valores no se hayan generado ya
        if email in generated_emails or alias in generated_aliases or dni in generated_dnis:
            continue  # Si hay duplicados, generar otro usuario

        # Estadísticas ficticias
        estadisticas = {
            "partidas_ganadas": random.randint(0, 100),
            "partidas_perdidas": random.randint(0, 100),
            "nivel": random.randint(1, 10),
        }

        # Intentar crear el usuario
        jugador = Jugador(
            nombre=nombre,
            email=email,
            dni=dni,
            telefono=telefono,
            alias=alias,
            estadisticas=estadisticas
        )
        jugador.save()

        # Si se ha creado correctamente, agregar los valores generados a las listas
        generated_emails.add(email)
        generated_aliases.add(alias)
        generated_dnis.add(dni)

        # Aumentar el contador de usuarios creados
        usuarios_creados += 1
        print(f'Jugador "{alias}" creado con éxito. Total creados: {usuarios_creados}/{total_usuarios}')

    except IntegrityError:
        # Si ocurre un error de integridad (por UNIQUE), lo capturamos y seguimos creando otros usuarios
        print(f'Error: El usuario con email "{email}" o alias "{alias}" ya existe. Intentando otro...')

print("Generación de usuarios completada.")
