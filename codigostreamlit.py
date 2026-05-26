import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# ---------------------------------------------------
# CONFIGURACIÓN GENERAL
# ---------------------------------------------------

st.set_page_config(
    page_title="Análisis Estadístico",
    layout="wide"
)

st.title("📊 Análisis Estadístico de Estudiantes")

# ---------------------------------------------------
# CARGA DE DATOS
# ---------------------------------------------------

df_est = pd.read_csv("estimated_data.csv")

st.subheader("Vista previa de los datos")
st.dataframe(df_est.head())

# ---------------------------------------------------
# FUNCIÓN PARA AGREGAR TOTAL
# ---------------------------------------------------

def agregar_total(df, columna_nombre):

    total = {
        columna_nombre: "TOTAL",
        "fi": df["fi"].sum(),
        "hi": df["hi"].sum(),
        "hip": df["hip"].sum(),
        "Fi": df["Fi"].max(),
        "Hi": df["Hi"].max()
    }

    if "marca_clase" in df.columns:
        total["marca_clase"] = "-"

    return pd.concat(
        [df, pd.DataFrame([total])],
        ignore_index=True
    )

# ---------------------------------------------------
# CONFIGURACIÓN DE GRÁFICOS
# ---------------------------------------------------

plt.style.use('seaborn-v0_8-whitegrid')

plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 12

# ---------------------------------------------------
# FASE 2 - VARIABLE CUALITATIVA
# ---------------------------------------------------

st.header("FASE 2 - Variable Cualitativa: Carrera")

frec_cualita = (
    df_est["carrera"]
    .value_counts()
    .reset_index()
)

frec_cualita.columns = ["carrera", "fi"]

# ordenar
frec_cualita = frec_cualita.sort_values("carrera")

# frecuencia relativa
frec_cualita["hi"] = (
    frec_cualita["fi"] / len(df_est)
)

# frecuencia porcentual
frec_cualita["hip"] = (
    frec_cualita["hi"] * 100
)

# frecuencia acumulada
frec_cualita["Fi"] = (
    frec_cualita["fi"].cumsum()
)

# frecuencia relativa acumulada
frec_cualita["Hi"] = (
    frec_cualita["hi"].cumsum()
)

# redondeo
frec_cualita = frec_cualita.round({
    "hi": 4,
    "hip": 2,
    "Hi": 4
})

# tabla SOLO para mostrar
frec_cualita_mostrar = agregar_total(
    frec_cualita.copy(),
    "carrera"
)

st.subheader("Tabla de Frecuencias - Carrera")
st.dataframe(frec_cualita_mostrar)

# ---------------------------------------------------
# FASE 3 - VARIABLE DISCRETA
# ---------------------------------------------------

st.header("FASE 3 - Materias Aprobadas")

tabla_discreta = (
    df_est["materias_aprobadas"]
    .value_counts()
    .sort_index()
    .reset_index()
)

tabla_discreta.columns = ["Materias_X", "fi"]

tabla_discreta["hi"] = (
    tabla_discreta["fi"] / len(df_est)
)

tabla_discreta["Fi"] = (
    tabla_discreta["fi"].cumsum()
)

tabla_discreta["Hi"] = (
    tabla_discreta["hi"].cumsum()
)

tabla_discreta["hip"] = (
    tabla_discreta["hi"] * 100
)

tabla_discreta = tabla_discreta.round({
    "hi": 4,
    "hip": 2,
    "Hi": 4
})

# tabla SOLO para mostrar
tabla_discreta_mostrar = agregar_total(
    tabla_discreta.copy(),
    "Materias_X"
)

st.subheader("Tabla de Frecuencias - Materias Aprobadas")
st.dataframe(tabla_discreta_mostrar)

# ---------------------------------------------------
# FASE 4 - VARIABLE AGRUPADA
# ---------------------------------------------------

st.header("FASE 4 - Variable Agrupada: Edad")

n = len(df_est)

edad_min = df_est["edad"].min()
edad_max = df_est["edad"].max()

rango = edad_max - edad_min

# regla de sturges
k = int(np.ceil(1 + 3.322 * np.log10(n)))

# amplitud
amplitud = int(np.ceil(rango / k))

st.write(f"**n:** {n}")
st.write(f"**Edad mínima:** {edad_min}")
st.write(f"**Edad máxima:** {edad_max}")
st.write(f"**Rango:** {rango}")
st.write(f"**Número de intervalos (k):** {k}")
st.write(f"**Amplitud:** {amplitud}")

# cortes
cortes = np.arange(
    edad_min,
    edad_max + amplitud + 1,
    amplitud
)

# crear intervalos
df_est["intervalos"] = pd.cut(
    df_est["edad"],
    bins=cortes,
    include_lowest=True,
    right=False
)

# tabla agrupada
tabla_agrupada = (
    df_est["intervalos"]
    .value_counts()
    .sort_index()
    .reset_index()
)

tabla_agrupada.columns = ["intervalos", "fi"]

# marca de clase
tabla_agrupada["marca_clase"] = (
    tabla_agrupada["intervalos"]
    .apply(lambda x: round(x.mid, 2))
)

# frecuencia relativa
tabla_agrupada["hi"] = (
    tabla_agrupada["fi"] / len(df_est)
)

# frecuencia porcentual
tabla_agrupada["hip"] = (
    tabla_agrupada["hi"] * 100
)

# frecuencia acumulada
tabla_agrupada["Fi"] = (
    tabla_agrupada["fi"].cumsum()
)

# frecuencia relativa acumulada
tabla_agrupada["Hi"] = (
    tabla_agrupada["hi"].cumsum()
)

tabla_agrupada = tabla_agrupada.round({
    "hi": 4,
    "hip": 2,
    "Hi": 4
})

# tabla SOLO para mostrar
tabla_agrupada_mostrar = agregar_total(
    tabla_agrupada.copy(),
    "intervalos"
)

st.subheader("Tabla de Frecuencias Agrupadas")
st.dataframe(tabla_agrupada_mostrar)

# ---------------------------------------------------
# GRÁFICO DE BARRAS
# ---------------------------------------------------

st.header("📌 Distribución por Carrera")

fig1, ax1 = plt.subplots(figsize=(12, 6))

ax1.bar(
    frec_cualita['carrera'],
    frec_cualita['fi'],
    color='skyblue'
)

ax1.set_title(
    'DISTRIBUCIÓN POR CARRERA',
    fontweight='bold'
)

ax1.set_xlabel('Carreras')

ax1.set_ylabel('Frecuencia Absoluta')

plt.xticks(rotation=20)

st.pyplot(fig1)

# ---------------------------------------------------
# GRÁFICO DE BASTONES
# ---------------------------------------------------

st.header("📌 Avance Académico")

fig2, ax2 = plt.subplots(figsize=(12, 6))

ax2.vlines(
    tabla_discreta['Materias_X'],
    ymin=0,
    ymax=tabla_discreta['fi'],
    color='navy',
    linewidth=2
)

ax2.plot(
    tabla_discreta['Materias_X'],
    tabla_discreta['fi'],
    "o",
    color='red'
)

ax2.set_xticks(tabla_discreta['Materias_X'])

ax2.set_title(
    'AVANCE ACADÉMICO',
    fontweight='bold'
)

ax2.set_xlabel(
    'Materias Aprobadas'
)

ax2.set_ylabel(
    'Frecuencia Absoluta'
)

st.pyplot(fig2)

# ---------------------------------------------------
# HISTOGRAMA + POLÍGONO
# ---------------------------------------------------

st.header("📌 Histograma y Polígono")

fig3, ax3 = plt.subplots(figsize=(12, 6))

ax3.hist(
    df_est['edad'],
    bins=cortes,
    color='#1fcaa0',
    edgecolor='white',
    alpha=0.7,
    label='Histograma'
)

ax3.plot(
    tabla_agrupada['marca_clase'],
    tabla_agrupada['fi'],
    color='red',
    marker='D',
    linewidth=2,
    label='Polígono'
)

ax3.set_title(
    'DISTRIBUCIÓN DE EDADES',
    fontweight='bold'
)

ax3.set_xlabel('Edad')

ax3.set_ylabel('Frecuencia')

ax3.legend()

st.pyplot(fig3)

# ---------------------------------------------------
# OJIVA
# ---------------------------------------------------

st.header("📌 Ojiva")

fig4, ax4 = plt.subplots(figsize=(10, 5))

ax4.plot(
    tabla_agrupada['marca_clase'],
    tabla_agrupada['Fi'],
    color='red',
    marker='s',
    linewidth=2,
    label='Ojiva'
)

ax4.fill_between(
    tabla_agrupada['marca_clase'],
    tabla_agrupada['Fi'],
    alpha=0.3
)

ax4.set_title(
    'FRECUENCIA ACUMULADA',
    fontweight='bold'
)

ax4.set_xlabel('Marca de Clase')

ax4.set_ylabel('Fi')

ax4.legend()

st.pyplot(fig4)

# ---------------------------------------------------
# GRÁFICO DE TORTA
# ---------------------------------------------------

st.header("📌 Porcentaje por Carrera")

fig5, ax5 = plt.subplots(figsize=(10, 6))

ax5.pie(
    frec_cualita['hi'],
    labels=frec_cualita['carrera'],
    autopct='%1.1f%%',
    startangle=90,
    colors=sns.color_palette('pastel')
)

ax5.set_title(
    'PORCENTAJE DE ESTUDIANTES POR CARRERA',
    fontweight='bold'
)

st.pyplot(fig5)