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

df_empleados["salario"] = [
    random.randint(500, 3000) for _ in range(len(df_empleados))
]

print(df_empleados.head())

df_final = pd.merge(
    df_empleados,
    departamentos,
    on="departamento_id"
)

print(df_final.head())

df_final = df_final.rename(columns={
    "nombre_x": "empleado",
    "nombre_y": "departamento"
})

print(df_final.head())

promedio_salario = df_final["salario"].mean()

print("Salario promedio general:")
print(promedio_salario)

salario_maximo = df_final["salario"].max()

print("Salario máximo:")
print(salario_maximo)

promedio_departamento = df_final.groupby(
    "departamento"
)["salario"].mean()

print("Promedio salarial por departamento:")
print(promedio_departamento)

promedio_departamento.plot(kind="bar")

plt.title("Salario Promedio por Departamento")
plt.xlabel("Departamento")
plt.ylabel("Salario Promedio")

plt.show()
