# 👥: TCA Client Profiler

Descubre los perfiles de tus clientes y optimiza tus estrategias de negocio con decisiones informadas: analiza comportamientos, identifica tendencias y maximiza tus ingresos.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gdp-dashboard-template.streamlit.app/)

### Estructura del proyecto

A continuación se muestra la estructura principal del repositorio, con señalizaciones para cada componente:

```
C:.
├───deployment         # (3) Despliegue de modelos y notebooks
├───interfaz           # (1) Interfaz de usuario (Streamlit)
│   ├───app            #     Código principal de la app
│   └───images         #     Imágenes utilizadas en la interfaz
└───pipeline           # (2) Pipeline de procesamiento y modelado (Kedro)
    ├───conf           #     Configuración de Kedro
    ├───data           #     Datos en diferentes etapas
    ├───docs           #     Documentación
    ├───notebooks      #     Notebooks de análisis/pruebas
    ├───src            #     Código fuente principal (pipelines)
    └───tests          #     Pruebas unitarias
```

### Cómo ejecutar localmente

Este repositorio contiene tres componentes principales:

#### 1. Interfaz (Streamlit)
La aplicación de usuario está en la carpeta `interfaz/app/`.

```sh
streamlit run streamlit_app.py
```

> **Nota:** Si deseas contenerizar la interfaz, puedes crear un `Dockerfile` en la carpeta `interfaz/app/` siguiendo la estructura de tu aplicación y los requisitos necesarios.

#### 2. Pipeline (Kedro)
El pipeline de procesamiento y modelado está en la carpeta `pipeline/`.
Para ejecutarlo, primero entra a la carpeta y luego corre Kedro:

```sh
cd pipeline
kedro run
```

También puedes ejecutar el pipeline usando Docker:

```sh
cd pipeline
# Construir la imagen
docker build -t kedro-pipeline .
# Ejecutar el contenedor (usando la interfaz de Kedro Docker)
kedro docker run
```

El `Dockerfile` para el pipeline se encuentra en `pipeline/Dockerfile`.

#### 3. Deployment
El despliegue del modelo se puede hacer de dos formas:
- **Como pipeline de Kedro:** Usando el pipeline de deployment dentro de la carpeta `pipeline/src/alephzeropipeline/pipelines/deployment/`.
- **Con Jupyter Notebook:** Usando el notebook `deployment/CloudDeployment.ipynb` para pruebas y despliegue manual en Azure ML.

> **Nota:** Si deseas contenerizar el despliegue, puedes crear un `Dockerfile` en la carpeta `deployment/` según los requisitos de tu entorno de despliegue.

> **Importante:** Algunos archivos de configuración `.json` pueden ser necesarios para la correcta ejecución de los módulos (por ejemplo, archivos de parámetros, credenciales o configuraciones específicas). Si no están presentes en el repositorio, deberás crearlos o solicitarlos al responsable del proyecto antes de ejecutar los códigos.

> **En caso de que tengas problemas para ejecutar el proyecto o falten archivos, puedes consultar el repositorio alternativo:**
> [Repositorio alternativo en GitHub](https://github.com/Tec-A01656059/TCA_AlephZero)

Asegúrate de revisar los requisitos y configuraciones específicas en cada carpeta antes de ejecutar.

