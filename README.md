# Perfil antropométrico en adultos mayores – Estudio ENASEM

**Investigadores:**

- Samuel Fallas — C5E975
- Anny Navarro — C5H831
- Susan Porras Castillo — C5I423

## Descripción del proyecto

Este proyecto consiste en una aplicación web desarrollada en Python mediante Shiny para Python, que permite explorar y analizar datos antropométricos provenientes del estudio ENASEM (Encuesta Nacional sobre Salud y Envejecimiento en México).

La ENASEM es un estudio longitudinal que evalúa el proceso de envejecimiento, el impacto de las enfermedades y la mortalidad en adultos mexicanos. La investigación inició en el año 2001 y realiza un seguimiento de la población estudiada a lo largo del tiempo.

La aplicación ofrece herramientas de análisis y visualización interactiva para estudiar distintas relaciones entre variables antropométricas de los adultos mayores.

## Objetivo

El objetivo del proyecto es facilitar el análisis exploratorio de datos antropométricos, permitiendo investigar las siguientes preguntas:

1. ¿Existen diferencias en la relación cintura-cadera entre hombres y mujeres?
2. ¿Qué relación existe entre el perímetro de cintura y el perímetro de cadera en los adultos mayores?
3. ¿Cómo varía el perímetro de cadera entre los distintos grupos de edad de los adultos mayores?
4. ¿Existen diferencias en el perímetro de cadera entre hombres y mujeres, considerando sus grupos de edad?
5. ¿Qué relación existe entre el índice de masa corporal (IMC) y la relación cintura-estatura de los individuos?
6. ¿Qué patrones de correlación existen entre las diferentes medidas antropométricas de los individuos?

## Tecnologías utilizadas

- Python
- Shiny para Python
- Pandas
- Plotly
- Shinywidgets

## Estructura del proyecto

- `app.py` → Aplicación principal Shiny (interfaz y servidor).
- `antropometria.csv` → Conjunto de datos utilizado.
- `requirements.txt` → Dependencias necesarias para ejecutar la aplicación.
- `README.md` → Documentación del proyecto.

## Funcionalidades principales

### 1. Filtrado interactivo de datos

La aplicación cuenta con un filtro por sexo que permite seleccionar entre hombres, mujeres o la totalidad de las observaciones.

### 2. Análisis estadístico

La aplicación permite explorar las relaciones entre distintas medidas antropométricas mediante herramientas de análisis descriptivo y visualización interactiva.

## Funcionamiento de la aplicación

La aplicación está desarrollada en Shiny para Python y utiliza:

- `reactive.calc()` para realizar operaciones reactivas, como el filtrado dinámico de los datos.
- `render_widget()` para generar gráficos interactivos.
- Pandas para la manipulación y transformación de los datos.
- Plotly para la construcción de visualizaciones interactivas.

Los filtros permiten modificar los datos utilizados en el análisis de manera dinámica.

## Nota metodológica
### Índice de masa corporal (IMC)

El índice de masa corporal (IMC) es una medida utilizada para relacionar el peso de una persona con su estatura.

Se calcula mediante la siguiente fórmula:

\[
IMC = \frac{\text{Peso (kg)}}{\text{Altura (m)}^2}
\]

Para realizar el cálculo, la altura debe expresarse en metros. Si los datos originales están registrados en centímetros, es necesario dividirlos entre 100 antes de aplicar la fórmula.
### Índice cintura-cadera (ICC)

El índice cintura-cadera (ICC) es una medida antropométrica que expresa la relación entre el perímetro de la cintura y el perímetro de la cadera.

Se calcula mediante la siguiente fórmula:

\[
ICC = \frac{\text{Perímetro de cintura}}{\text{Perímetro de cadera}}
\]

Ambas medidas deben expresarse en la misma unidad, por ejemplo, centímetros.

Este indicador permite estudiar la proporción entre ambas medidas corporales y analizar sus diferencias entre los grupos de interés.

## Cómo ejecutar la aplicación

### 1. Requisitos previos

Tener instalado Python y contar con los archivos del proyecto.

### 2. Instalar las dependencias

Desde la terminal, ubicarse en la carpeta del proyecto y ejecutar:

```bash
py -m pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

Utilizar el siguiente comando:

```bash
py -m shiny run --reload --port 8000 app:app
```

### 4. Acceder a la aplicación

Una vez iniciado el servidor, abrir la siguiente dirección en el navegador:

```text
http://127.0.0.1:8000
```

## Autoría

Proyecto desarrollado como parte del curso de Programación para Estadística II de la Universidad de Costa Rica.

## Comentario final

Este proyecto permite explorar datos antropométricos de adultos mayores mediante herramientas de análisis estadístico y visualización interactiva. A través de las preguntas de investigación planteadas, se busca estudiar las relaciones entre distintas medidas corporales y comprender mejor sus variaciones en la población analizada.
