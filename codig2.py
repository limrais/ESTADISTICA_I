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

try:
    df_est = pd.read_csv("10mil_datos.csv")
    st.success(f"✅ Datos cargados correctamente - {len(df_est)} estudiantes")
except FileNotFoundError:
    st.error("❌ ERROR: No se encontró el archivo '10mil_datos.csv'")
    st.info("Ejecuta primero el script de creación de datos")
    st.stop()
except Exception as e:
    st.error(f"❌ Error al leer el archivo: {e}")
    st.stop()

st.subheader("Vista previa de los datos")
st.dataframe(df_est.head(), use_container_width=True)

# Mostrar estadísticas básicas
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total estudiantes", len(df_est))
with col2:
    st.metric("Carreras diferentes", df_est["carrera"].nunique())
with col3:
    st.metric("Edad promedio", f"{df_est['edad'].mean():.1f} años")
with col4:
    st.metric("Materias promedio", f"{df_est['materias_aprobadas'].mean():.1f}")

# ---------------------------------------------------
# FUNCIÓN PARA AGREGAR TOTAL
# ---------------------------------------------------

def agregar_total(df, columna_nombre):
    """Agrega una fila de totales a la tabla de frecuencias"""
    
    total = {
        columna_nombre: "TOTAL",
        "fi": df["fi"].sum(),
        "Fi": df["Fi"].max() if "Fi" in df.columns else "-",
    }
    
    if "hi" in df.columns:
        total["hi"] = df["hi"].sum()
    if "hip" in df.columns:
        total["hip"] = df["hip"].sum()
    if "Hi" in df.columns:
        total["Hi"] = df["Hi"].max() if len(df) > 0 else "-"
    
    if "marca_clase" in df.columns:
        total["marca_clase"] = "-"
    
    if "intervalos" in df.columns:
        total["intervalos"] = "-"
    
    return pd.concat([df, pd.DataFrame([total])], ignore_index=True)

# ---------------------------------------------------
# CONFIGURACIÓN DE GRÁFICOS
# ---------------------------------------------------

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 11

# ---------------------------------------------------
# FASE 2 - VARIABLE CUALITATIVA: CARRERA
# ---------------------------------------------------

st.header("📋 FASE 2 - Variable Cualitativa: Carrera")

# Calcular frecuencias para TODAS las carreras
frec_cualita = (
    df_est["carrera"]
    .value_counts()
    .sort_index()  # Ordenar alfabéticamente
    .reset_index()
)
frec_cualita.columns = ["carrera", "fi"]

n = len(df_est)
frec_cualita["hi"] = frec_cualita["fi"] / n
frec_cualita["hip"] = frec_cualita["hi"] * 100
frec_cualita["Fi"] = frec_cualita["fi"].cumsum()
frec_cualita["Hi"] = frec_cualita["hi"].cumsum()

# Redondeo
frec_cualita = frec_cualita.round({
    "hi": 4,
    "hip": 2,
    "Hi": 4
})

# Tabla para mostrar
frec_cualita_mostrar = agregar_total(frec_cualita.copy(), "carrera")

st.subheader("Tabla de Frecuencias - Carrera")
st.dataframe(frec_cualita_mostrar, use_container_width=True)

# ---------------------------------------------------
# FASE 3 - VARIABLE DISCRETA: MATERIAS APROBADAS
# ---------------------------------------------------

st.header("📚 FASE 3 - Materias Aprobadas (Variable Discreta)")

# Asegurar que TODOS los valores posibles aparezcan
materias_min = df_est["materias_aprobadas"].min()
materias_max = df_est["materias_aprobadas"].max()
todos_valores = pd.Series(range(materias_min, materias_max + 1), name="Materias_X")

tabla_discreta = (
    df_est["materias_aprobadas"]
    .value_counts()
    .reindex(todos_valores, fill_value=0)
    .sort_index()
    .reset_index()
)
tabla_discreta.columns = ["Materias_X", "fi"]

# Calcular frecuencias
tabla_discreta["hi"] = tabla_discreta["fi"] / n
tabla_discreta["Fi"] = tabla_discreta["fi"].cumsum()
tabla_discreta["Hi"] = tabla_discreta["hi"].cumsum()
tabla_discreta["hip"] = tabla_discreta["hi"] * 100

tabla_discreta = tabla_discreta.round({
    "hi": 4,
    "hip": 2,
    "Hi": 4
})

# Tabla para mostrar
tabla_discreta_mostrar = agregar_total(tabla_discreta.copy(), "Materias_X")

st.subheader("Tabla de Frecuencias - Materias Aprobadas")
st.dataframe(tabla_discreta_mostrar, use_container_width=True)

# ---------------------------------------------------
# FASE 4 - VARIABLE AGRUPADA: EDAD
# ---------------------------------------------------

st.header("🎂 FASE 4 - Variable Agrupada: Edad")

edad_min = df_est["edad"].min()
edad_max = df_est["edad"].max()
rango = edad_max - edad_min

# Regla de Sturges
k = int(np.ceil(1 + 3.322 * np.log10(n)))
amplitud = max(1, int(np.ceil(rango / k)))

# Mostrar información
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("n", n)
with col2:
    st.metric("Edad mínima", edad_min)
with col3:
    st.metric("Edad máxima", edad_max)
with col4:
    st.metric("Rango", rango)
with col5:
    st.metric("N° intervalos (k)", k)

st.write(f"**Amplitud del intervalo:** {amplitud}")

# Crear intervalos
cortes = np.arange(edad_min, edad_max + amplitud + 1, amplitud)

df_est["intervalos"] = pd.cut(
    df_est["edad"],
    bins=cortes,
    include_lowest=True,
    right=False
)

# Tabla agrupada
tabla_agrupada = (
    df_est["intervalos"]
    .value_counts()
    .sort_index()
    .reset_index()
)
tabla_agrupada.columns = ["intervalos", "fi"]

# Marca de clase
tabla_agrupada["marca_clase"] = tabla_agrupada["intervalos"].apply(
    lambda x: round(x.mid, 2)
)

# Frecuencias
tabla_agrupada["hi"] = tabla_agrupada["fi"] / n
tabla_agrupada["hip"] = tabla_agrupada["hi"] * 100
tabla_agrupada["Fi"] = tabla_agrupada["fi"].cumsum()
tabla_agrupada["Hi"] = tabla_agrupada["hi"].cumsum()

tabla_agrupada = tabla_agrupada.round({
    "hi": 4,
    "hip": 2,
    "Hi": 4
})

# Tabla para mostrar
tabla_agrupada_mostrar = agregar_total(tabla_agrupada.copy(), "intervalos")

st.subheader("Tabla de Frecuencias Agrupadas - Edad")
st.dataframe(tabla_agrupada_mostrar, use_container_width=True)

# ---------------------------------------------------
# GRÁFICOS (TODAS LAS CARRERAS)
# ---------------------------------------------------

# 1. GRÁFICO DE BARRAS - TODAS las carreras
st.header("📊 Distribución por Carrera")

fig1, ax1 = plt.subplots(figsize=(14, 7))
colores_bar = sns.color_palette('Set2', len(frec_cualita))
barras = ax1.bar(frec_cualita['carrera'], frec_cualita['fi'], 
                  color=colores_bar, edgecolor='black', linewidth=0.5)

# Agregar valores encima de las barras
for barra in barras:
    altura = barra.get_height()
    ax1.text(barra.get_x() + barra.get_width()/2., altura + 5,
             f'{int(altura)}', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax1.set_title('DISTRIBUCIÓN DE ESTUDIANTES POR CARRERA', fontweight='bold', fontsize=16)
ax1.set_xlabel('Carrera', fontsize=13)
ax1.set_ylabel('Frecuencia Absoluta (N° estudiantes)', fontsize=13)
plt.xticks(rotation=45, ha='right', fontsize=10)
plt.tight_layout()
st.pyplot(fig1)

# 2. GRÁFICO DE BASTONES - Materias aprobadas
st.header("📈 Avance Académico (Materias Aprobadas)")

fig2, ax2 = plt.subplots(figsize=(14, 7))
ax2.vlines(tabla_discreta['Materias_X'], ymin=0, ymax=tabla_discreta['fi'],
           color='navy', linewidth=3, alpha=0.7)
ax2.plot(tabla_discreta['Materias_X'], tabla_discreta['fi'], "o", 
         color='red', markersize=10, markeredgecolor='black', markeredgewidth=1)

# Agregar valores
for i, (x, y) in enumerate(zip(tabla_discreta['Materias_X'], tabla_discreta['fi'])):
    ax2.text(x, y + 20, f'{int(y)}', ha='center', va='bottom', fontsize=10, fontweight='bold')

ax2.set_xticks(tabla_discreta['Materias_X'])
ax2.set_title('DISTRIBUCIÓN DE MATERIAS APROBADAS', fontweight='bold', fontsize=16)
ax2.set_xlabel('Número de Materias Aprobadas', fontsize=13)
ax2.set_ylabel('Frecuencia Absoluta (N° estudiantes)', fontsize=13)
ax2.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()
st.pyplot(fig2)

# 3. HISTOGRAMA + POLÍGONO - Edad
st.header("📊 Histograma y Polígono de Frecuencias - Edad")

fig3, ax3 = plt.subplots(figsize=(14, 7))
ax3.hist(df_est['edad'], bins=cortes, color='#1fcaa0', 
         edgecolor='black', alpha=0.6, linewidth=0.5, label='Histograma')
ax3.plot(tabla_agrupada['marca_clase'], tabla_agrupada['fi'], 
         color='red', marker='D', linewidth=2, markersize=8, 
         markeredgecolor='black', markeredgewidth=0.5, label='Polígono de Frecuencias')

ax3.set_title('DISTRIBUCIÓN DE EDADES DE ESTUDIANTES', fontweight='bold', fontsize=16)
ax3.set_xlabel('Edad (años)', fontsize=13)
ax3.set_ylabel('Frecuencia', fontsize=13)
ax3.legend(loc='upper right', fontsize=11)
ax3.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()
st.pyplot(fig3)

# 4. OJIVA - Frecuencias Acumuladas
st.header("📉 Ojiva de Frecuencias Acumuladas - Edad")

fig4, ax4 = plt.subplots(figsize=(14, 7))
ax4.plot(tabla_agrupada['marca_clase'], tabla_agrupada['Fi'], 
         color='darkred', marker='s', linewidth=2.5, markersize=8, 
         markeredgecolor='black', markeredgewidth=0.5, label='Frecuencia Absoluta Acumulada')
ax4.fill_between(tabla_agrupada['marca_clase'], tabla_agrupada['Fi'], 
                  alpha=0.2, color='red')

# Agregar valores
for i, (x, y) in enumerate(zip(tabla_agrupada['marca_clase'], tabla_agrupada['Fi'])):
    ax4.text(x, y + 100, f'{int(y)}', ha='center', va='bottom', fontsize=9)

ax4.set_title('FRECUENCIA ABSOLUTA ACUMULADA - EDADES', fontweight='bold', fontsize=16)
ax4.set_xlabel('Marca de Clase (Edad en años)', fontsize=13)
ax4.set_ylabel('Frecuencia Acumulada (Fi)', fontsize=13)
ax4.legend(loc='lower right', fontsize=11)
ax4.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()
st.pyplot(fig4)

# 5. GRÁFICO DE TORTA - TODAS las carreras
st.header("🥧 Porcentaje por Carrera")

fig5, ax5 = plt.subplots(figsize=(12, 10))
colores_pie = sns.color_palette('Set3', len(frec_cualita))
wedges, texts, autotexts = ax5.pie(
    frec_cualita['fi'],
    labels=frec_cualita['carrera'],
    autopct='%1.1f%%',
    startangle=90,
    colors=colores_pie,
    textprops={'fontsize': 11},
    pctdistance=0.85
)

# Mejorar visualización de etiquetas
for text in texts:
    text.set_fontweight('bold')
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(10)

# Agregar círculo central (efecto dona)
centre_circle = plt.Circle((0, 0), 0.70, fc='white', linewidth=2, edgecolor='black')
fig5.gca().add_artist(centre_circle)

ax5.set_title('PORCENTAJE DE ESTUDIANTES POR CARRERA', fontweight='bold', fontsize=16, pad=20)
plt.tight_layout()
st.pyplot(fig5)

# ---------------------------------------------------
# ESTADÍSTICAS DESCRIPTIVAS
# ---------------------------------------------------

st.header("📊 Estadísticas Descriptivas")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📏 Edad")
    st.write(f"• **Media:** {df_est['edad'].mean():.2f} años")
    st.write(f"• **Mediana:** {df_est['edad'].median():.2f} años")
    st.write(f"• **Moda:** {df_est['edad'].mode()[0]} años")
    st.write(f"• **Desviación estándar:** {df_est['edad'].std():.2f} años")
    st.write(f"• **Varianza:** {df_est['edad'].var():.2f}")
    st.write(f"• **Mínimo:** {df_est['edad'].min()} años")
    st.write(f"• **Máximo:** {df_est['edad'].max()} años")
    st.write(f"• **Rango:** {df_est['edad'].max() - df_est['edad'].min()} años")

with col2:
    st.subheader("📚 Materias Aprobadas")
    st.write(f"• **Media:** {df_est['materias_aprobadas'].mean():.2f}")
    st.write(f"• **Mediana:** {df_est['materias_aprobadas'].median():.2f}")
    st.write(f"• **Moda:** {df_est['materias_aprobadas'].mode()[0]}")
    st.write(f"• **Desviación estándar:** {df_est['materias_aprobadas'].std():.2f}")
    st.write(f"• **Varianza:** {df_est['materias_aprobadas'].var():.2f}")
    st.write(f"• **Mínimo:** {df_est['materias_aprobadas'].min()}")
    st.write(f"• **Máximo:** {df_est['materias_aprobadas'].max()}")
    st.write(f"• **Rango:** {df_est['materias_aprobadas'].max() - df_est['materias_aprobadas'].min()}")

# ---------------------------------------------------
# TABLA RESUMEN POR CARRERA
# ---------------------------------------------------

st.header("📋 Resumen por Carrera")

resumen_carrera = df_est.groupby('carrera').agg({
    'edad': ['mean', 'min', 'max'],
    'materias_aprobadas': ['mean', 'min', 'max']
}).round(2)

resumen_carrera.columns = ['Edad Promedio', 'Edad Mín', 'Edad Máx', 
                           'Materias Prom', 'Materias Mín', 'Materias Máx']
resumen_carrera = resumen_carrera.sort_index()

st.dataframe(resumen_carrera, use_container_width=True)

st.success("✅ Análisis estadístico completado exitosamente!")