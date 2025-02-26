import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Leer datos
oferta = pd.read_csv("dash.csv", encoding='latin-1', index_col='propuesta')
demanda = pd.read_csv("board.csv", encoding='latin-1', index_col='partida')
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

prop = oferta['clave'].nunique()
of = len(oferta[oferta['estatus'] != 'no procedente'])
efect = len(oferta[oferta['estatus'] != 'no procedente'])

adj = len(demanda[demanda['estatus'].isin(['único', 'simultáneo'])])
des = len(demanda[demanda['estatus'] == 'desierta'])
so = len(demanda[demanda['estatus'] == 'sin oferta'])
absim = len(demanda[demanda['estatus'] == 'simultáneo'])

# Definir funciones para crear gráficos
def crear_histograma_oferta(data):
    return px.histogram(data, x="proveedor", title="Distribución de Adjudicación por Proveedor")

def crear_pie_oferta(data):
    return px.pie(data, names='estatus', title='Distribución de Estatus de Oferta')

def crear_hist_of_ad(data):
    return px.histogram(data, x='adjudicación (%)', title='Distribución de Adjudicación (%)')

def crear_histograma_demanda(data):
    return px.histogram(data, x="proveedores", title="Distribución de Proveedores")

def crear_pie_demanda(data):
    return px.pie(data, names='estatus', title='Distribución de Estatus de Demanda')

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
status_options = {
    "General": claves_unicas,
    "Desiertas": "desierta",
    "Adjudicación Única": "único",
    "Abastecimiento Simultáneo": "simultáneo",
    "Sin Oferta": "sin oferta"
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
    selected_status = st.selectbox("Ingrese el estatus", list(status_options.keys()), key="resumen_status")
    stat = status_options[selected_status]

    selected_abasto = st.selectbox("Ingrese tipo de abastecimiento", list(abasto_options.keys()), key="resumen_abasto")
    abastecimiento = abasto_options[selected_abasto]

    selected_type = st.selectbox("Ingrese el tipo de clave", list(type_options.keys()), key="resumen_type")
    ty = type_options[selected_type]

    clave_input = st.selectbox("Ingrese la clave o claves separadas por coma", list(clave_options.keys()), key="resumen_clave")
    cl = [s.strip() for s in clave_input.split(',')]

    # Filtrar datos
    datos_filtrados_oferta = oferta[oferta['clave'].isin(cl)]
    datos_filtrados_demanda = demanda[demanda['clave'].isin(cl)]

    # Crear un contenedor para el recuadro
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("TOTAL DE PROPUESTAS", f"{prop}")
        col2.metric("OFERTAS PARA ANÁLISIS", f"{of}")
        col3.metric("ADJUDICADAS", f"{adj}")
        col4.metric("DESIERTAS", f"{des}")
        
        col5, col6, col7 = st.columns(3)
        col5.metric("PROPUESTAS EFECTIVAS", f"{efect}")
        col6.metric("SIN OFERTA%", f"{so}")
        col7.metric("SIMULTÁNEAS", f"{absim}")

    # Mostrar gráficos 
    st.plotly_chart(crear_histograma_oferta(datos_filtrados_oferta), key="resumen_histogram_oferta")
    st.plotly_chart(crear_pie_oferta(datos_filtrados_oferta), key="resumen_pie_oferta")
    st.plotly_chart(crear_histograma_demanda(datos_filtrados_demanda), key="resumen_histogram_demanda")
    st.plotly_chart(crear_pie_demanda(datos_filtrados_demanda), key="resumen_pie_demanda") 
    st.plotly_chart(crear_hist_of_ad(datos_filtrados_oferta), key="resumen_hist_of_ad")

# Pestaña 2: Oferta
with tab2:
    clave_input = st.selectbox("Ingrese la clave o claves separadas por coma", list(clave_options.keys()), key="oferta_clave")
    cl = [s.strip() for s in clave_input.split(',')]

    selected_proveedor = st.selectbox("Ingrese el proveedor", list(proveedor_options.keys()), key="oferta_proveedor")
    prov = proveedor_options[selected_proveedor]

    selected_status = st.selectbox("Ingrese el estatus", list(status_options.keys()), key="oferta_status")
    stat = status_options[selected_status]

    selected_abasto = st.selectbox("Ingrese tipo de abastecimiento", list(abasto_options.keys()), key="oferta_abasto")
    abastecimiento = abasto_options[selected_abasto]

    selected_type = st.selectbox("Ingrese el tipo de clave", list(type_options.keys()), key="oferta_type")
    ty = type_options[selected_type]

    # Filtrar datos
    datos_filtrados_oferta = oferta[oferta['clave'].isin(cl)]

    # Mostrar gráficos específicos de la oferta
    st.plotly_chart(crear_histograma_oferta(datos_filtrados_oferta), key="oferta_histogram_oferta")
    st.plotly_chart(crear_pie_oferta(datos_filtrados_oferta), key="oferta_pie_oferta")

# Pestaña 3: Demanda
with tab3:
    selected_instituto = st.selectbox("Ingrese el Instituto:", list(instituto_options.keys()), key="demanda_instituto")
    inst = instituto_options[selected_instituto]

    clave_input = st.selectbox("Ingrese la clave o claves separadas por coma", list(clave_options.keys()), key="demanda_clave")
    cl = [s.strip() for s in clave_input.split(',')]

    selected_status = st.selectbox("Ingrese el estatus", list(status_options.keys()), key="demanda_status")
    stat = status_options[selected_status]

    selected_abasto = st.selectbox("Ingrese tipo de abastecimiento", list(abasto_options.keys()), key="demanda_abasto")
    abastecimiento = abasto_options[selected_abasto]

    selected_type = st.selectbox("Ingrese el tipo de clave", list(type_options.keys()), key="demanda_type")
    ty = type_options[selected_type]

    # Filtrar datos
    datos_filtrados_demanda = demanda[demanda['clave'].isin(cl)]

    # Mostrar gráficos específicos de la demanda
    st.plotly_chart(crear_histograma_demanda(datos_filtrados_demanda), key="demanda_histogram_demanda")
    st.plotly_chart(crear_pie_demanda(datos_filtrados_demanda), key="demanda_pie_demanda")

    col4, col5, col6, col7 = st.columns(4)
    col4.metric("ADJUDICADAS", f"{adj}")
    col5.metric("SIN OFERTA%", f"{
    col4, col5, col6, col7 = st.columns(4)
    col4.metric("ADJUDICADAS", f"{adj}")
    col5.metric("SIN OFERTA%", f"{so}")
    col6.metric("DESIERTAS", f"{des}")
    col7.metric("SIMULTÁNEAS", f"{absim}")

    # Mostrar gráficos interactivos
    st.plotly_chart(crear_histograma_demanda(datos_filtrados_demanda), key="demanda_histogram")
    st.plotly_chart(crear_pie_demanda(datos_filtrados_demanda), key="demanda_pie")

    st.header("Demanda")
    st.write(demanda.head())

# Incluir imagen como pie de página
st.image("footer.png", use_container_width=True)
