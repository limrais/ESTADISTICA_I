import pandas as pd
import numpy as np

# Fijar semilla para reproducibilidad
np.random.seed(42)

# Configuracion
n_estudiantes = 10000

# Carreras con distribuciones realistas
carreras = {
    'Ingenieria Informatica': 0.25,
    'Medicina': 0.20,
    'Administracion de Empresas': 0.15,
    'Derecho': 0.12,
    'Psicologia': 0.10,
    'Arquitectura': 0.08,
    'Ingenieria Civil': 0.06,
    'Economia': 0.04
}

# Generar datos
datos = {
    'carrera': np.random.choice(
        list(carreras.keys()), 
        size=n_estudiantes, 
        p=list(carreras.values())
    ),
    'edad': np.random.normal(22, 3, n_estudiantes).astype(int),
    'materias_aprobadas': np.random.normal(5, 2, n_estudiantes).astype(int)
}

df = pd.DataFrame(datos)

# Ajustar edades para que sean realistas (entre 18 y 35)
df['edad'] = df['edad'].clip(18, 35)

# Ajustar materias aprobadas (entre 1 y 10)
df['materias_aprobadas'] = df['materias_aprobadas'].clip(1, 10)

# Ajustar por carrera (medicina tiende a ser mayor)
df.loc[df['carrera'] == 'Medicina', 'edad'] = df.loc[df['carrera'] == 'Medicina', 'edad'] + 1
df.loc[df['carrera'] == 'Medicina', 'edad'] = df.loc[df['carrera'] == 'Medicina', 'edad'].clip(20, 35)

# Guardar CSV
df.to_csv('10mil_datos.csv', index=False)

print("=" * 50)
print("ARCHIVO CREADO EXITOSAMENTE")
print("=" * 50)
print(f"Archivo: 10mil_datos.csv")
print(f"Registros: {n_estudiantes}")
print(f"\nEstadisticas del dataset:")
print(f"Edad - Media: {df['edad'].mean():.2f}, Min: {df['edad'].min()}, Max: {df['edad'].max()}")
print(f"Materias - Media: {df['materias_aprobadas'].mean():.2f}, Min: {df['materias_aprobadas'].min()}, Max: {df['materias_aprobadas'].max()}")
print(f"\nDistribucion por carrera:")
print(df['carrera'].value_counts())
print("=" * 50)