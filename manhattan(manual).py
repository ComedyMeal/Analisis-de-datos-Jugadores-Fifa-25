# -*- coding: utf-8 -*-
"""manhattan(manual).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1iEGzjZ4mo5fYZQtb9PpWWGso8zjQ4VUx

## Preprocesamiento de lo datos
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# publicar los datos en la web

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSCcLYUfHCYwv1-XrJIUqtbbJpSQvUMp9L7VQLgkE821RrJ6KWGdEU6u5sHi6y26MNnlR8oFSFzulGB/pub?output=csv"
data = pd.read_csv(url) #guarda todos los datos en esa variable
data.head()

columnas_objetivo = ['Name', 'OVR', 'PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY', 'Acceleration',
       'Sprint Speed', 'Positioning', 'Finishing', 'Shot Power', 'Long Shots',
       'Volleys', 'Penalties', 'Vision', 'Crossing', 'Free Kick Accuracy',
       'Short Passing', 'Long Passing', 'Curve', 'Dribbling', 'Agility',
       'Balance', 'Reactions', 'Ball Control', 'Composure', 'Interceptions',
       'Heading Accuracy', 'Def Awareness', 'Standing Tackle',
       'Sliding Tackle', 'Jumping', 'Stamina', 'Strength', 'Aggression',
       'Weak foot', 'Skill moves', 'Age', 'GK Diving', 'GK Handling',
       'GK Kicking', 'GK Positioning', 'GK Reflexes', 'Preferred foot',
       'Nation', 'Position']
columnas = data.columns

for col in columnas:
  if col not in columnas_objetivo:
    data.drop(col, axis = 1, inplace = True)
  else:
    data[col] = data[col]

"""## Imputación de datos faltantes"""

# imputar datos faltantes para las categorias de GK cambiando NaN por 0
gk_columns =   ["GK Diving","GK Handling","GK Kicking","GK Positioning","GK Reflexes"]
data [gk_columns] = data [gk_columns].fillna(0)

# Ahora extraeremos los datos
X = data.iloc [:, 1:].values # filas, columnas

# lo que "DEBERIA" dar es = 17737 (datos), 45 (columnas)
X.shape

data.iloc[:, -7]

df = pd.DataFrame(X)
for col in df.columns:
  #Convertir a numérico, forzando errores a NaN
  df[col] = pd.to_numeric(df[col], errors = "coerce")

X = df.values
X

from sklearn.impute import SimpleImputer #algo esta raro con esta
imputer = SimpleImputer(missing_values=np.nan, strategy ="median")
imputer.fit(X)
X = imputer.transform(X)
X

X_ = X

X_ = X[:,: -1] #Eligiendo todos los datos exepto la nacionalidad
X_

X_ = pd.DataFrame(X_)
# Exportar el conjunto de datos
X_.to_csv("datos_totales_imputados.csv", index=False)

"""## PCA"""

from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA

# Imputar los datos faltantes con la mediana
imputer = SimpleImputer(missing_values=np.nan, strategy="median")
X_ = imputer.fit_transform(X_)  # Imputar NaN

# Crear un objeto PCA y ajustar los datos
pca = PCA(n_components=3)  # Queremos las tres primeras componentes principales
X_pca = pca.fit_transform(X_)

varianza = pca.explained_variance_ratio_
print(sum(varianza))

# con lo de PCA graficamos

from sklearn.cluster import KMeans

# Supongamos que ya has realizado PCA y tienes X_pca
# Definir el número de clusters
n_clusters = 4  # Cambia esto según tus necesidades

# Paso 1: Ajustar el modelo KMeans y predecir los clusters
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
clusters_manuales_mahalanobis = kmeans.fit_predict(X_pca)  # Aquí se define la variable
#definir la variable y numero de clusters
# Paso 2: Convertir a tipo int
clusters_manuales_mahalanobis = clusters_manuales_mahalanobis.astype(int)

# Verifica los resultados
print(clusters_manuales_mahalanobis)

"""## Grafico 2D"""

# Crear un gráfico de dispersión 2D usando las dos primeras componentes
plt.figure(figsize=(10, 6))
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1],
                hue=clusters_manuales_mahalanobis, palette='viridis',
                alpha=0.6, s=100)  # Cambia clusters por clusters_manuales_mahalanobis
plt.title('Visualización 2D de la Clusterización (PCA)', fontsize=16)
plt.xlabel('Componente Principal 1')
plt.ylabel('Componente Principal 2')
plt.grid(True)
plt.legend(title='Cluster')
plt.show()

"""## Grafico 3D"""

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

# Crear un gráfico de dispersión 3D usando las tres primeras componentes
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Graficar los puntos
scatter = ax.scatter(X_pca[:, 0], X_pca[:, 1], X_pca[:, 2], c=clusters_manuales_mahalanobis, cmap='viridis', s=50)

# Etiquetas de los ejes y título
ax.set_title('Visualización 3D de la Clusterización (PCA)', fontsize=16)
ax.set_xlabel('Componente Principal 1')
ax.set_ylabel('Componente Principal 2')
ax.set_zlabel('Componente Principal 3')

# Crear la leyenda
unique_clusters = np.unique(clusters_manuales_mahalanobis)
colors = scatter.get_array()

# Añadir la leyenda manualmente
handles = []
for cluster in unique_clusters:
    handle = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=scatter.cmap(scatter.norm(cluster)), markersize=10, label=f'Cluster {cluster}')
    handles.append(handle)

ax.legend(handles=handles, title='Clusters', loc='best')

plt.show()

"""## K-means distancia Mahalanobis(Manual)"""

import random

### Distancia de Manhattan

def distancia_L1(x, c):
    return np.sum(np.abs(x - c))  # Suma de las diferencias absolutas

### Distancia de Manhattan

def distancia_L1(x, c):
    return np.sum(np.abs(x - c))  # Suma de las diferencias absolutas

# Paso 1: Número de clusters
k = 4  # Por heurística de los datos y método del codo

# Paso 2: Elección de centroides
## Centroides
dimension = X_.shape[0]  # Número de jugadores (filas del DataFrame)
centroids = X_[random.sample(range(dimension), k)]
print(data.iloc[centroids[:,0],0])
print(data.iloc[centroids[:,1],0])
print(data.iloc[centroids[:,2],0])

### Almacenamiento de etiquetas
clusters_manuales = np.zeros(dimension)  ## vector nulo para almacenar etiquetas
### Almacenamiento de distancias
distancias = np.zeros((dimension, k))     ## Matriz nula para almacenar distancias

# Paso 3: Implementación del método y criterios de convergencia
tol = 1e-6
error = 100

# Repetir hasta que los centroides dejen de moverse significativamente
while error > tol:
    # Asignación de puntos a los clusters más cercanos
    for i in range(dimension):  ## Iterar sobre las filas. La i representa jugador
        for j in range(k):      ## Iterar sobre las columnas. La j representa centroide
            distancias[i, j] = distancia_L1(X_[i], centroids[j])
        clusters_manuales[i] = np.argmin(distancias[i])

    # Almacenar los centroides previos antes de actualizarlos
    centroids_prev = np.copy(centroids) ## Creación variable auxiliar para comparar con los nuevos centroides

    # Actualizar centroides
    for l in range(k):  ### Iteramos sobre los clusters (k = 4)
        puntos_cluster = X_[clusters_manuales == l] ### Estamos tomando todos los puntos que tengan la etiqueta L

        # Si el cluster no está vacío, recalcula el centroide
        if len(puntos_cluster) > 0:
            centroids[l] = np.mean(puntos_cluster, axis=0)  ### Promedia los puntos que pertenecen al cluster, columna por columna
        else:
            print(f"Cluster {l} vacío, reasignando centroide aleatoriamente")
            centroids[l] = X_[np.random.choice(dimension)]

    # Calcular el error como el cambio promedio en los centroides
    error = np.mean([distancia_L1(centroids[l], centroids_prev[l]) for l in range(k)])
    print(error)