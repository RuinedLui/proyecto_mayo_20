import pandas as pd
import random
from faker import Faker

fake = Faker('es_ES')
random.seed(42)

# ==========================================
# DIM_EMPLEADOS
# ==========================================

lista_empleados = []

for i in range(1, 11):
    lista_empleados.append({
        "empleado_id":     i,
        "nombre_empleado": fake.name(),
        "cargo":           fake.job(),
        "tipo_contrato":   random.choice(["Permanente", "Temporal"])
    })

dim_empleados = pd.DataFrame(lista_empleados)

print("--- DIM_EMPLEADOS ---")
print(dim_empleados)

# ==========================================
# DIM_DEPARTAMENTOS
# ==========================================

dim_departamentos = pd.DataFrame([
    {"departamento_id": 1, "nombre_departamento": "Tecnologia"},
    {"departamento_id": 2, "nombre_departamento": "Ventas"},
    {"departamento_id": 3, "nombre_departamento": "Recursos Humanos"},
    {"departamento_id": 4, "nombre_departamento": "Finanzas"},
    {"departamento_id": 5, "nombre_departamento": "Operaciones"}
])

print("\n--- DIM_DEPARTAMENTOS ---")
print(dim_departamentos)

# ==========================================
# DIM_TIEMPO
# ==========================================

meses = [
    "Enero", "Febrero", "Marzo", "Abril",
    "Mayo", "Junio", "Julio", "Agosto",
    "Septiembre", "Octubre", "Noviembre", "Diciembre"
]

lista_tiempo = []

for i, mes in enumerate(meses, 1):
    lista_tiempo.append({
        "fecha_id": i,
        "mes":      mes,
        "anio":     2025,
        "semestre": 1 if i <= 6 else 2
    })

dim_tiempo = pd.DataFrame(lista_tiempo)

print("\n--- DIM_TIEMPO ---")
print(dim_tiempo)

# ==========================================
# FACT_SALARIOS
# 10 empleados x 12 meses = 120 registros
# ==========================================

lista_salarios = []
salario_id = 1

for _, emp in dim_empleados.iterrows():
    depto_id         = random.randint(1, 5)
    salario_base_ref = round(random.uniform(800, 3500), 2)

    for fecha_id in range(1, 13):
        bono         = round(random.uniform(0, 500), 2) if random.random() > 0.4 else 0.0
        deducciones  = round(salario_base_ref * 0.10, 2)
        salario_neto = round(salario_base_ref + bono - deducciones, 2)

        lista_salarios.append({
            "salario_id":      salario_id,
            "empleado_id":     emp["empleado_id"],
            "departamento_id": depto_id,
            "fecha_id":        fecha_id,
            "salario_base":    salario_base_ref,
            "bono":            bono,
            "deducciones":     deducciones,
            "salario_neto":    salario_neto
        })
        salario_id += 1

fact_salarios = pd.DataFrame(lista_salarios)

print("\n--- FACT_SALARIOS ---")
print(f"Total registros: {len(fact_salarios)}")
print(fact_salarios.head(10))

# ==========================================
# MODELO ESTRELLA
# ==========================================

modelo = (
    fact_salarios
    .merge(dim_empleados,     on="empleado_id")
    .merge(dim_departamentos, on="departamento_id")
    .merge(dim_tiempo,        on="fecha_id")
)

# ==========================================
# ANALISIS 1: SALARIO PROMEDIO
# ==========================================

print("\n--- Salario promedio ---")
print(f"${modelo['salario_neto'].mean():,.2f}")

# ==========================================
# ANALISIS 2: SALARIO MAXIMO
# ==========================================

print("\n--- Salario maximo ---")
print(f"${modelo['salario_neto'].max():,.2f}")

# ==========================================
# ANALISIS 3: SALARIOS POR DEPARTAMENTO
# ==========================================

por_depto = (
    modelo.groupby("nombre_departamento")["salario_neto"]
    .mean().reset_index()
    .sort_values("salario_neto", ascending=False)
    .reset_index(drop=True)
)
por_depto.index += 1

print("\n--- Salarios por departamento ---")
print(por_depto)

# ==========================================
# ANALISIS 4: SALARIOS POR MES
# ==========================================

por_mes = (
    modelo.groupby("mes")["salario_neto"]
    .sum().reset_index()
    .sort_values("salario_neto", ascending=False)
    .reset_index(drop=True)
)
por_mes.index += 1

print("\n--- Salarios por mes ---")
print(por_mes)

# ==========================================
# ANALISIS 5: TOP 5 EMPLEADOS
# ==========================================

top5 = (
    modelo.groupby("nombre_empleado")["salario_neto"]
    .mean().reset_index()
    .sort_values("salario_neto", ascending=False)
    .head(5).reset_index(drop=True)
)
top5.index += 1

print("\n--- Top 5 empleados con mayor salario ---")
print(top5)