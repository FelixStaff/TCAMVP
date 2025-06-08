import streamlit as st
import pandas as pd
import random
import plotly.graph_objects as go
from functions import average_rate, average_los, kpi_reservations, kpi_revenue
import clasificador

random.seed(42)  # For reproducibility

# CSS styling
with open("interfaz/app/style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load data
data = pd.read_csv("interfaz/app/GH_DataHistory.csv")
data['GraphDate'] = pd.to_datetime(data['GraphDate']).dt.to_period('M')
data['RegId'] = random.sample(range(100000, 999999), len(data))

st.session_state.month = data['GraphDate'].max()

b1, b2 = st.columns([0.9, 0.07])
b1.empty()
if b2.button("⬅ Volver"):
    st.switch_page("interfaz/app/inicio.py")

## Upload new clients
t1,t2 = st.columns([0.4, 0.9])

# Get the date for the report
key_date = t1.date_input("Selecciona mes de reporte", value=pd.to_datetime("2020-01-01"), key="report_date")
key_date = pd.to_datetime(key_date)
key_date = key_date.to_period('M')

# Only allow file upload if key_date is greater than the latest month in the data
if key_date > st.session_state.month:
    new_data = t2.file_uploader("Cargar archivo CSV", type=["csv"])
else:
    new_data = None
    t2.warning("Selecciona un mes posterior al último registrado para cargar un nuevo archivo.")

if new_data is not None:
    # Read the uploaded CSV file
    clientes_noclasificados = pd.read_csv(new_data)

    # Get assigned cluster
    clasificar = clasificador.GuestProfileClassifier('interfaz/app/model.pkl')
    clusters = clasificar.classify(clientes_noclasificados, muestra=len(clientes_noclasificados))

    # Add the clusters to the dataframe
    clientes_clasificados = clientes_noclasificados.copy()
    clientes_clasificados['cluster'] = clusters
    clientes_clasificados['GraphDate'] = [key_date for _ in range(len(clientes_clasificados))]
    clientes_clasificados['Profile'] = clientes_clasificados['cluster'].map({0: 'A', 1: 'B', 2: 'C'})

    existing_reg_ids = set(data['RegId'])
    clientes_clasificados['RegId'] = [f"new_{i}" for i in range(len(clientes_clasificados)) if f"new_{i}" not in existing_reg_ids]

    # Show the dataframe with assigned profiles
    st.subheader("Clasificación de clientes")
    st.dataframe(clientes_clasificados[['Profile', 'Adults', 'Minors', 'FreeMinors', 'Nights', 'LocalCurrencyAmount']])

    c1,c2 = st.columns([0.9, 0.9])

    # Pie chart for profile distribution
    with c1.container():
        profile_counts = data['Profile'].value_counts()
        pie = go.Figure(data=[go.Pie(labels=profile_counts.index, values=profile_counts.values)])
        pie.update_layout(title_text='Distribución de Perfiles de Clientes')
        st.plotly_chart(pie, use_container_width=True)

    # Monthly KPIs
    with c2.container():
        last_month = data['GraphDate'].max()
        current_data = data[data['GraphDate'] == last_month]
        new_data = pd.concat([data, clientes_clasificados], ignore_index=True)

        st.write("### KPIs principales")
        k1, k2 = st.columns(2)

        adr_actual, adr_anterior = average_rate(new_data, 'all')
        k1.metric(
                label="Tarifa promedio por reservación (ADR)", 
                value=f'{adr_actual:.2f} USD',
                delta = f"{adr_actual - adr_anterior:.2f} USD respecto al mes anterior")
            
        los_actual, los_anterior = average_los(new_data, 'all')
        k1.metric(
            label="Longitud de estancia promedio (LOS)", 
           value=f'{los_actual:.2f} noches',
            delta = f"{los_actual - los_anterior:.2f} noches respecto al mes anterior")
            
        res_actual, res_anterior = kpi_reservations(data, 'all')
        k2.metric(
            label="Total de reservaciones",
            value=f"{res_actual} reservaciones",
            delta=f"{res_actual - res_anterior} respecto al mes anterior")
            
        ing_actual, ing_anterior = kpi_revenue(data, 'all')
        k2.metric(
            label="Ingresos totales",
            value=f"${ing_actual:,.2f} USD",
            delta=f"${ing_actual - ing_anterior:.2f} respecto al mes anterior")
    
    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Guardar cambios", use_container_width=True):
        # Save the new data to the CSV file
        new_data.to_csv("interfaz/app/GH_DataHistory.csv", index=False)
        st.success("Datos guardados exitosamente")
