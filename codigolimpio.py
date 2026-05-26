import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

df_est = pd.read_csv("estimated_data.csv")
print(df_est.head())

# ========== FASE 2: VARIABLE CUALITATIVA (CARRERAS) ==========
frec_cualita = df_est["carrera"].value_counts().reset_index()
frec_cualita.columns = ["carrera", "fi"]
frec_cualita["hi"] = frec_cualita["fi"] / len(df_est)
frec_cualita["hip"] = frec_cualita["hi"] * 100
frec_cualita["Fi"] = frec_cualita["fi"].cumsum()
frec_cualita["Hi"] = frec_cualita["hi"].cumsum()
print("TABLA DE FRECUENCIAS: CARRERAS")
print(frec_cualita)

# ========== FASE 3: VARIABLE DISCRETA (MATERIAS APROBADAS) ==========
tabla_discreta = df_est["materias_aprobadas"].value_counts().sort_index().reset_index()
tabla_discreta.columns = ["Materias_X", "fi"]
tabla_discreta["hi"] = tabla_discreta["fi"] / len(df_est)
tabla_discreta["Fi"] = tabla_discreta["fi"].cumsum()
tabla_discreta["Hi"] = tabla_discreta["hi"].cumsum()
tabla_discreta["hip"] = tabla_discreta["hi"] * 100
print("TABLA DE FRECUENCIAS: MATERIAS APROBADAS")
print(tabla_discreta)

# ========== FASE 4: VARIABLE CONTINUA (EDAD) - AGRUPACIÓN ==========
n = len(df_est)
rango = df_est['edad'].max() - df_est['edad'].min()
k = int(np.ceil(1 + 3.322 * np.log10(n)))
amplitud = rango / k
print(f"n: {n}, Rango: {rango}, k: {k}, Amplitud: {amplitud}")
cortes = np.arange(df_est["edad"].min(), df_est["edad"].max() + amplitud, amplitud)

df_est["intervalos"] = pd.cut(df_est["edad"], bins=cortes, include_lowest=True, right=False)
tabla_agrupada = df_est["intervalos"].value_counts().sort_index().reset_index()
tabla_agrupada.columns = ["intervalos", "fi"]
tabla_agrupada["marca_clase"] = tabla_agrupada["intervalos"].apply(lambda x: x.mid)
tabla_agrupada["hi"] = tabla_agrupada["fi"] / len(df_est)
tabla_agrupada["hip"] = tabla_agrupada["hi"] * 100
tabla_agrupada["Fi"] = tabla_agrupada["fi"].cumsum()
tabla_agrupada["Hi"] = tabla_agrupada["hi"].cumsum()
print(tabla_agrupada)

# ========== FASE 5: REPRESENTACIÓN GRÁFICA ==========
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 12

# --- GRÁFICO 1: BARRAS (CARRERAS) ---
fig, ax = plt.subplots(figsize=(12,6))
ax.bar(frec_cualita['carrera'], frec_cualita['fi'], color='skyblue')
ax.set_title('DISTRIBUCIÓN POR CARRERA', fontweight='bold')
ax.set_xlabel('Carreras Universitarias')
ax.set_ylabel('Cantidad de Estudiantes (fi)')
plt.show()

# --- GRÁFICO 2: BASTONES (MATERIAS APROBADAS) ---
fig, ax = plt.subplots(figsize=(12,6))
ax.vlines(tabla_discreta['Materias_X'], ymin=0, ymax=tabla_discreta['fi'], color='navy', linewidth=2)
ax.plot(tabla_discreta['Materias_X'], tabla_discreta['fi'], "o", color='red')
ax.set_xticks(tabla_discreta['Materias_X'])
ax.set_title('AVANCE ACADEMICO (VARIABLES DISCRETAS)', fontweight='bold')
ax.set_xlabel('Número de Materias Aprobadas')
ax.set_ylabel('Frecuencia Absoluta (fi)')
plt.show()

# --- GRÁFICO 3: HISTOGRAMA + POLÍGONO (EDAD) ---
fig, ax = plt.subplots(figsize=(12, 6))
ax.hist(df_est['edad'], bins=cortes, color='#1fcaa0', edgecolor='white', alpha=0.6, label='Histograma')
ax.plot(tabla_agrupada['marca_clase'], tabla_agrupada['fi'], color='red', marker='D', linewidth=2, label='Polígono')
ax.set_title('ANÁLISIS DE DISTRIBUCIÓN DE EDADES (DATOS AGRUPADOS)', fontweight='bold')
ax.set_xticks(cortes)
ax.set_xlabel('Intervalos de Clase (años) / Marca de Clase (Xi)')
ax.set_ylabel('Frecuencia Absoluta (fi)')
ax.legend()
plt.show()

# --- GRÁFICO 4: OJIVA (EDAD - FRECUENCIA ACUMULADA) ---
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(tabla_agrupada['marca_clase'], tabla_agrupada['Fi'], color='red', marker='s', linewidth=2, label='Ojiva')
ax.fill_between(tabla_agrupada['marca_clase'], tabla_agrupada['Fi'], color='purple', alpha=0.3)
ax.set_title('ANÁLISIS DE DISTRIBUCIÓN DE EDADES (DATOS AGRUPADOS)', fontweight='bold')
ax.set_xticks(cortes)
ax.set_xlabel('Intervalos de Clase (años)')
ax.set_ylabel('Frecuencia Absoluta Acumulada (Fi)')
ax.legend()
plt.show()

# --- GRÁFICO 5: PASTEL (CARRERAS - FRECUENCIA RELATIVA) ---
fig, ax = plt.subplots(figsize=(10,5))
ax.pie(frec_cualita['hi'], labels=frec_cualita['carrera'], autopct='%1.1f%%',
       startangle=90, colors=sns.color_palette('pastel'))
ax.set_title("PORCENTAJE DE ESTUDIANTES POR CARRERA", fontweight="bold")
plt.show()