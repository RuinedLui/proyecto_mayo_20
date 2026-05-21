import pandas as pd
import random
import matplotlib.pyplot as plt
from faker import Faker

fake = Faker()


departamentos = pd.DataFrame([
    {"departamento_id": 1, "nombre": "Tecnología"},
    {"departamento_id": 2, "nombre": "Ventas"},
    {"departamento_id": 3, "nombre": "RRHH"},
    {"departamento_id": 4, "nombre": "Finanzas"},
    {"departamento_id": 5, "nombre": "Operaciones"},
])

print(departamentos)


empleados = []

for i in range(1, 36):
    empleados.append({
        "empleado_id": i,
        "nombre": fake.name(),
        "departamento_id": random.randint(1, 5)
    })

df_empleados = pd.DataFrame(empleados)

print(df_empleados.head())
