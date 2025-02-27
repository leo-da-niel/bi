import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Leer datos
df = pd.read_excel('inst.xlsx', index_col='#')

# Variables
proveedores_unicos = df['PROVEEDOR'].unique()
claves_unicas = df['CLAVES'].unique()
medicamentos = [clave for clave in claves_unicas if int(clave.split('.')[0]) < 60]
material_curacion = [clave for clave in claves_unicas if int(clave.split('.')[0]) >= 60]
unico = df[df['ABASTO'] == 1]
simultaneo = df[df['ABASTO'] < 1]
ab_u = unico['CLAVES'].unique()
ab_s = simultaneo['CLAVES'].unique()

# Definir funciones para crear gráficos
def crear_pie(data):
    return px.pie(data)

def crear_hist(data, columna='CLAVES'):  # Modificación: especificar la columna para el histograma
    return px.histogram(data, x=columna)  # Usamos una columna específica para el histograma

def crear_líneas(data):
    return px.line(data)

# Configuración de la página
st.set_page_config(page_title="Dashboard", layout="wide")

# Incluir imagen como encabezado
st.image("header.png", use_container_width=True)

# Opciones
clave_options = {"TODAS LAS CLAVES": "General", **{clave: clave for clave in claves_unicas}}

instituto_options = {
    "IMSS": "IMSS",
    "IMSS BIENESTAR": "IMSS BIENESTAR",
    "ISSSTE": "ISSSTE",
    "SEMAR": "SEMAR",
    "CENAPRECE": "CENAPRECE",
    "CENISDA": "CENISDA",
    "CNEGRS": "CNEGRS",
    "CONASAMA": "CONASAMA",
    "PEMEX": "PEMEX"
}
proveedor_options = {proveedor: proveedor for proveedor in proveedores_unicos}

abasto_options = {
    "General": claves_unicas,
    "Abastecimiento simultáneo": ab_s,
    "Abastecimiento único": ab_u
}

type_options = {
    "General": claves_unicas,
    "Medicamento": medicamentos,
    "Material de Curación": material_curacion
}

# Pestañas
tab1, tab2, tab3 = st.tabs(["Resumen de licitación", "Oferta", "Demanda"])

# Pestaña 1: Resumen de licitación
with tab1:
    selected_abasto = st.selectbox("Ingrese tipo de abastecimiento", list(abasto_options.keys()), key="resumen_abasto")
    abastecimiento = abasto_options[selected_abasto]

    selected_type = st.selectbox("Ingrese el tipo de clave", list(type_options.keys()), key="resumen_type")
    ty = type_options[selected_type]

    clave_input = st.selectbox("Ingrese la clave o claves separadas por coma", list(clave_options.keys()), key="resumen_clave")
    cl = [s.strip() for s in clave_input.split(',')]

    # Filtrar datos
    datos_filtrados_demanda = df[(df['CLAVES'].isin(cl)) & (df['ABASTO'].isin(abastecimiento))]

    # Crear un contenedor para el recuadro
    with st.container():
        # Mostrar gráficos 
        if datos_filtrados_demanda.empty:
            st.warning("No hay datos para mostrar en el gráfico de demanda.")
        else:
            st.plotly_chart(crear_hist(datos_filtrados_demanda), key="resumen_histogram_demanda")
            st.plotly_chart(crear_pie(datos_filtrados_demanda), key="resumen_pie_demanda")

# Pestaña 2: Oferta
with tab2:
    selected_proveedor = st.selectbox("Ingrese el proveedor", list(proveedor_options.keys()), key="oferta_proveedor")
    prov = proveedor_options[selected_proveedor]

    selected_abasto = st.selectbox("Ingrese tipo de abastecimiento", list(abasto_options.keys()), key="oferta_abasto")
    abastecimiento = abasto_options[selected_abasto]

    selected_type = st.selectbox("Ingrese el tipo de clave", list(type_options.keys()), key="oferta_type")
    ty = type_options[selected_type]

    # Filtrar datos
    datos_filtrados_oferta = df[(df['CLAVES'].isin(cl)) & (df['PROVEEDOR'] == prov) & (df['ABASTO'].isin(abastecimiento))]

    # Verificar si los datos filtrados no están vacíos
    if datos_filtrados_oferta.empty:
        st.warning("No hay datos para mostrar en el gráfico de oferta.")
    else:
        st.plotly_chart(crear_hist(datos_filtrados_oferta), key="oferta_histogram_oferta")
        st.plotly_chart(crear_pie(datos_filtrados_oferta), key="oferta_pie_oferta")

# Pestaña 3: Demanda
with tab3:
    # Histograma general de los proveedores
    px.histogram(df["PROVEEDOR"], title="Distribución de Adjudicación por Proveedor")
    
    # Selección de instituto
    selected_instituto = st.selectbox("Ingrese el Instituto:", list(instituto_options.keys()), key="demanda_instituto")
    inst = instituto_options[selected_instituto]
    
    # Generar los nombres de las columnas de 2025 y 2026
    inst25 = f"{inst}_25"  # Para 2025
    inst26 = f"{inst}_26"  # Para 2026

    # Filtrar los datos para el año 2025 y 2026
    datos_filtrados_demanda25 = df[(df['CLAVES'].isin(cl)) & (df['INSTITUTO_25'] == inst25)]
    datos_filtrados_demanda26 = df[(df['CLAVES'].isin(cl)) & (df['INSTITUTO_26'] == inst26)]

    # Mostrar gráficos para 2025 y 2026
    if not datos_filtrados_demanda25.empty:
        st.plotly_chart(crear_hist(datos_filtrados_demanda25), key="demanda_histogram25")
    else:
        st.warning(f"No hay datos disponibles para el Instituto {inst25} en 2025.")

    if not datos_filtrados_demanda26.empty:
        st.plotly_chart(crear_hist(datos_filtrados_demanda26), key="demanda_histogram26")
    else:
        st.warning(f"No hay datos disponibles para el Instituto {inst26} en 2026.")

    # Incluir imagen como pie de página
    st.image("footer.png", use_container_width=True)
