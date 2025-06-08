import streamlit as st
import pandas as pd
import random
import plotly.express as px

# Set up the page configuration
random.seed(42)  # For reproducibility

data = pd.read_csv("interfaz/app/GH_DataHistory.csv")
data['GraphDate'] = pd.to_datetime(data['GraphDate']).dt.to_period('M')

b1, b2 = st.columns([0.9, 0.1])
b1.empty()
if b2.button("⬅ Volver"):
    st.switch_page("inicio.py")

# Create a unique identifier for each reservation
data['RegId'] = random.sample(range(100000, 999999), len(data))
st.title("Dashboard Interactivo de Clientes")

# Sidebar para selección de variables y tipo de gráfico
st.sidebar.header("Opciones de visualización")

# Selección de variables numéricas y categóricas
num_vars = data.select_dtypes(include=['number']).columns.tolist()
num_vars = [var for var in num_vars if var != 'RegId' and var != 'cluster']

cat_vars = data.select_dtypes(include=['object', 'category']).columns.tolist()
cat_vars = [var for var in cat_vars if var != 'GraphDate']

x_var = st.sidebar.selectbox("Variable en el eje X", options=num_vars + cat_vars, index=0)
y_var = st.sidebar.selectbox("Variable en el eje Y", options=[None] + num_vars, index=0)
graph_type = st.sidebar.selectbox("Tipo de gráfico", options=["Histograma", "Barras", "Dispersión", "Boxplot"])

# Filtros interactivos para variables categóricas
st.sidebar.header("Filtros")

# Botón para resetear filtros
if st.sidebar.button("🔄 Resetear valores"):
    st.experimental_rerun()

filters = {}
for col in cat_vars:
    unique_vals = data[col].dropna().unique().tolist()
    if len(unique_vals) > 1 and len(unique_vals) < 30:
        selected = st.sidebar.multiselect(f"Filtrar {col}", unique_vals, default=unique_vals)
        filters[col] = selected

# Sliders para variables numéricas
num_filters = {}
for col in num_vars:
    min_val = float(data[col].min())
    max_val = float(data[col].max())
    step = (max_val - min_val) / 100 if max_val > min_val else 1
    selected_range = st.sidebar.slider(
        f"Filtrar {col}",
        min_value=min_val,
        max_value=max_val,
        value=(min_val, max_val),
        step=step,
        format="%.2f"
    )
    num_filters[col] = selected_range

# Aplicar filtros
filtered_data = data.copy()
filtered_data = filtered_data.drop(columns=['RegId', 'GraphDate','cluster'], errors='ignore')

for col, vals in filters.items():
    filtered_data = filtered_data[filtered_data[col].isin(vals)]
for col, (min_v, max_v) in num_filters.items():
    filtered_data = filtered_data[(filtered_data[col] >= min_v) & (filtered_data[col] <= max_v)]

# Mostrar gráfico según selección
st.subheader(f"Visualización: {graph_type}")
if graph_type == "Histograma":
    st.plotly_chart(px.histogram(filtered_data, x=x_var), use_container_width=True)
elif graph_type == "Barras":
    st.plotly_chart(px.bar(filtered_data, x=x_var, y=y_var) if y_var else px.bar(filtered_data, x=x_var), use_container_width=True)
elif graph_type == "Dispersión":
    if y_var:
        st.plotly_chart(px.scatter(filtered_data, x=x_var, y=y_var), use_container_width=True)
    else:
        st.info("Selecciona una variable para el eje Y.")
elif graph_type == "Boxplot":
    if y_var:
        st.plotly_chart(px.box(filtered_data, x=x_var, y=y_var), use_container_width=True)
    else:
        st.info("Selecciona una variable para el eje Y.")

st.subheader("Datos Filtrados (muestra de 100):")
st.dataframe(filtered_data.head(100), use_container_width=True, hide_index=True)
