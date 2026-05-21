import pandas as pd
import random
import matplotlib.pyplot as plt
from faker import Faker

fake = Faker()

# ============================================================
# DIM_DEPARTAMENTOS
# ============================================================

departamentos = [
    {"departamento_key": 1, "departamento": "Tecnología"},
    {"departamento_key": 2, "departamento": "Ventas"},
    {"departamento_key": 3, "departamento": "RRHH"},
    {"departamento_key": 4, "departamento": "Finanzas"},
    {"departamento_key": 5, "departamento": "Operaciones"},
]

dim_departamentos = pd.DataFrame(departamentos)

print(dim_departamentos)

# ============================================================
# DIM_SEDES
# ============================================================

sedes = [
    {"sede_key": 1, "sede": "San Salvador"},
    {"sede_key": 2, "sede": "Santa Ana"},
    {"sede_key": 3, "sede": "San Miguel"},
    {"sede_key": 4, "sede": "Sonsonate"},
    {"sede_key": 5, "sede": "Usulután"},
]

dim_sedes = pd.DataFrame(sedes)

print(dim_sedes)

# ============================================================
# DIM_TIEMPO
# ============================================================

tiempo = []

for i in range(1, 13):
    tiempo.append({
        "tiempo_key": i,
        "mes": i,
        "trimestre": f"Q{(i - 1) // 3 + 1}",
        "anio": 2024
    })

dim_tiempo = pd.DataFrame(tiempo)

print(dim_tiempo.head())

# ============================================================
# DIM_EMPLEADOS
# ============================================================

empleados = []

for i in range(1, 51):
    empleados.append({
        "empleado_key": i,
        "nombre": fake.name(),
        "cargo": random.choice(["Analista", "Gerente", "Coordinador", "Asistente"]),
        "departamento_key": random.randint(1, 5),
        "sede_key": random.randint(1, 5)
    })

dim_empleados = pd.DataFrame(empleados)

print(dim_empleados.head())

# ============================================================
# FACT_SALARIOS
# ============================================================

salarios = []

for i in range(1, 1001):

    salario_base = round(random.uniform(600, 4000), 2)
    bono = round(random.uniform(0, 500), 2)
    deduccion = round(salario_base * 0.07, 2)

    salarios.append({
        "salario_id": i,
        "empleado_key": random.randint(1, 50),
        "departamento_key": random.randint(1, 5),
        "sede_key": random.randint(1, 5),
        "tiempo_key": random.randint(1, 12),
        "salario_base": salario_base,
        "bono": bono,
        "deduccion": deduccion,
        "salario_neto": round(salario_base + bono - deduccion, 2)
    })

fact_salarios = pd.DataFrame(salarios)

print(fact_salarios.head())

# ============================================================
# CONSTRUCCIÓN DEL STAR SCHEMA
# ============================================================

modelo = fact_salarios.merge(
    dim_empleados,
    on="empleado_key"
).merge(
    dim_departamentos,
    on="departamento_key"
).merge(
    dim_sedes,
    on="sede_key"
).merge(
    dim_tiempo,
    on="tiempo_key"
)

print(modelo.head())

# ============================================================
# KPI 1 - SALARIOS POR DEPARTAMENTO
# ============================================================

salarios_depto = modelo.groupby(
    "departamento"
)["salario_neto"].sum()

print("\nSALARIOS POR DEPARTAMENTO")
print(salarios_depto)

# ============================================================
# KPI 2 - SALARIOS POR SEDE
# ============================================================

salarios_sede = modelo.groupby(
    "sede"
)["salario_neto"].sum()

print("\nSALARIOS POR SEDE")
print(salarios_sede)

# ============================================================
# KPI 3 - PROMEDIO SALARIAL
# ============================================================

promedio = modelo["salario_neto"].mean()

print("\nPROMEDIO SALARIAL")
print(promedio)

# ============================================================
# KPI 4 - TOP EMPLEADOS
# ============================================================

top_empleados = modelo.groupby(
    "nombre"
)["salario_neto"].sum().sort_values(
    ascending=False
).head(10)

print("\nTOP EMPLEADOS")
print(top_empleados)

# ============================================================
# VISUALIZACIÓN
# ============================================================

salarios_depto.plot(
    kind="bar",
    figsize=(8, 5)
)

plt.title("Salarios por Departamento")
plt.xlabel("Departamento")
plt.ylabel("Total ($)")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()