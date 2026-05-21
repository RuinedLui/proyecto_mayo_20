import pandas as pd
import random
from faker import Faker

# Inicializar Faker para datos realistas
fake = Faker('es_ES')

# ==========================================
# 1. DIMENSIÓN DEPARTAMENTOS
# ==========================================
nombres_deptos = ["Recursos Humanos", "Sistemas", "Finanzas", "Ventas", "Operaciones"]
departamentos = []

# departamento_key es nuestra Surrogate Key
for i, nombre in enumerate(nombres_deptos, 1):
    departamentos.append({
        "departamento_key": i,
        "nombre_departamento": nombre,
        "edificio": random.choice(["Torre Norte", "Torre Sur", "Remoto"])
    })

dim_departamentos = pd.DataFrame(departamentos)

# ==========================================
# 2. DIMENSIÓN EMPLEADOS 
# ==========================================
empleados = []

# Creamos 30 empleados ranodwms
for i in range(1, 31): 
    empleados.append({
        "empleado_key": i, # Surrogate Key
        "nombre_empleado": fake.name(),
        "cargo": fake.job(),
        "tipo_contrato": random.choice(["Permanente", "Temporal"])
    })

dim_empleados = pd.DataFrame(empleados)

# ==========================================
# 3. DIMENSIÓN TIEMPO (Año 2025)
# ==========================================
tiempo = []
fecha_key_counter = 1

# 12 meses del 2025
for mes in range(1, 13): 
    tiempo.append({
        "fecha_key": fecha_key_counter, # Surrogate Key
        "mes": mes,
        "anio": 2025,
        "semestre": 1 if mes <= 6 else 2
    })
    fecha_key_counter += 1

dim_tiempo = pd.DataFrame(tiempo)

# ==========================================
# 4. FACT TABLE: SALARIOS (30 empleados * 12 meses = 360 registros)
# ==========================================
salarios_fact = []
salario_id_counter = 1

for empleado in empleados:
    # A cada empleado se le asigna un departamento aleatorio al inicio
    depto_id = random.randint(1, len(nombres_deptos))
    
    # Se le define un salario base que variará un poco cada mes
    salario_base_referencia = random.uniform(800, 3500)
    
    # Generamos su pago para cada uno de los 12 meses de la dimensión tiempo
    for mes_key in range(1, 13):
        # Cálculos de nómina
        salario_base = round(salario_base_referencia, 2)
        bono = round(random.uniform(0, 500), 2) if random.random() > 0.4 else 0.0
        deducciones = round(salario_base * 0.10, 2) # 10% de descuentos de ley
        salario_neto = round(salario_base + bono - deducciones, 2)
        
        # Insertamos el registro conectando las Surrogate Keys
        salarios_fact.append({
            "salario_id": salario_id_counter,          # Primary Key de la Fact
            "empleado_key": empleado["empleado_key"],  # FK a Dim Empleados
            "departamento_key": depto_id,              # FK a Dim Departamentos
            "fecha_key": mes_key,                      # FK a Dim Tiempo
            "salario_base": salario_base,
            "bono": bono,
            "deducciones": deducciones,
            "salario_neto": salario_neto
        })
        salario_id_counter += 1

fact_salarios = pd.DataFrame(salarios_fact)

print(f"Total de registros generados en Fact Salarios: {len(fact_salarios)}\n")
print("--- Muestra de la Fact Table ---")
print(fact_salarios.head())

# ==========================================
# 5. MODELO ANALÍTICO EN ESTRELLA (MERGE)
# ==========================================
# Unimos todas las piezas usando las surrogate keys para poder analizar
modelo_estrella = fact_salarios.merge(
    dim_empleados, on="empleado_key"
).merge(
    dim_departamentos, on="departamento_key"
).merge(
    dim_tiempo, on="fecha_key"
)

# Comprobación de que la unión funciona mostrando columnas clave
print("\n--- Vista del Modelo Final Unido (Muestra) ---")
print(modelo_estrella[['nombre_empleado', 'nombre_departamento', 'mes', 'anio', 'salario_neto']].head())

# Analisis salario promedio general de todo el tiempo
print("\n--- Analisis salario promedio general ---")
promedio_general = modelo_estrella["salario_neto"].mean()
print(f"El salario promedio de toda la empresa es: ${promedio_general:.2f}")

# Salario maximo general de todo el tiempo
print("\n--- Analisis salario maximo ---")
maximo_general = modelo_estrella["salario_neto"].max()
print(f"El salario máximo pagado en la historia es: ${maximo_general:.2f}")
# Salario por departamento (Promedio general sin repetición de meses)
print("\n--- Analisis salario por departamento ---")

# Agrupamos solo por departamento
df_depto = modelo_estrella[["nombre_departamento", "salario_neto"]].groupby("nombre_departamento").mean().reset_index()

# Ordenamos de mayor a menor salario promedio para darle lógica visual
df_depto = df_depto.sort_values("salario_neto", ascending=False).reset_index(drop=True)

# Ajustamos el índice para que empiece en 1
df_depto.index = df_depto.index + 1

print(df_depto)

# Salarios por mes
print("\n--- Analisis salario por mes ---")
df_mes = modelo_estrella[["anio", "mes", "salario_neto"]].groupby(["anio", "mes"]).sum().reset_index()
df_mes.index = df_mes.index + 1
print(df_mes)

# Top 10 empleados mas pagados (índice del 1 al 10)
print("\n--- Top 10 empleados mas pagados ---")
top_10 = modelo_estrella[["nombre_empleado", "salario_neto"]].sort_values("salario_neto", ascending=False).head(10).reset_index(drop=True)
top_10.index = top_10.index + 1
print(top_10)