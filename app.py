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

#, names, title):
#names, title)
#, x, title):
# , x, title)
#, x, y, color):
#, x, y, color)
def crear_pie(data):
    return px.pie(data)


def crear_hist(data):
    return px.histogram(data)


def crear_líneas(data):
    return px.line(data)

#def crear_pie_demanda(data):
 #   return px.pie(data, names='estatus', title='Distribución de Estatus de Demanda')

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
tab1, tab2, tab3 = st.tabs(["Claves", "Proveedores", "Institutos"])

# Pestaña 1: Resumen de licitación
with tab1:
    selected_abasto = st.selectbox("Ingrese tipo de abastecimiento", list(abasto_options.keys()), key="resumen_abasto")
    abastecimiento = abasto_options[selected_abasto]

    selected_type = st.selectbox("Ingrese el tipo de clave", list(type_options.keys()), key="resumen_type")
    ty = type_options[selected_type]

    clave_input = st.selectbox("Ingrese la clave o claves separadas por coma", list(clave_options.keys()), key="resumen_clave")
    cl = [s.strip() for s in clave_input]

    # Filtrar datos
    datos_filtrados = df[(df['CLAVES'].isin(cl)) & (df['ABASTO'].isin(abastecimiento)) & (df['CLAVES'].isin(ty))]

    # Crear un contenedor para el recuadro

    # Mostrar gráficos 
    st.plotly_chart(crear_hist(datos_filtrados), key="resumen_histogram_oferta")
    st.plotly_chart(crear_pie(datos_filtrados), key="resumen_pie_oferta")

# Pestaña 2: Oferta
with tab2:
    px.histogram(df["PROVEEDOR"],  title="Distribución de Adjudicación por Proveedor")

    selected_proveedor = st.selectbox("Ingrese el proveedor", list(proveedor_options.keys()), key="oferta_proveedor")
    prov = proveedor_options[selected_proveedor]

    selected_abasto = st.selectbox("Ingrese tipo de abastecimiento", list(abasto_options.keys()), key="oferta_abasto")
    abastecimiento = abasto_options[selected_abasto]

    selected_type = st.selectbox("Ingrese el tipo de clave", list(type_options.keys()), key="oferta_type")
    ty = type_options[selected_type]

    # Filtrar datos
    datos_filtrados_oferta = df[(df['CLAVES'].isin(cl)) & (df['PROVEEDOR'] == prov) & (df['ABASTO'].isin(abastecimiento))]

    # Mostrar gráficos específicos de la oferta
    st.plotly_chart(crear_histograma_oferta(datos_filtrados_oferta), key="oferta_histogram_oferta")
    st.plotly_chart(crear_pie_oferta(datos_filtrados_oferta), key="oferta_pie_oferta")

# Pestaña 3: Demanda
with tab3:
    px.histogram(df["PROVEEDOR"],  title="Distribución de Adjudicación por Proveedor")
    
    selected_instituto = st.selectbox("Ingrese el Instituto:", list(instituto_options.keys()), key="demanda_instituto")
    inst = instituto_options[selected_instituto]
    inst25 = int+"_25"
    inst26 = int+"_26"
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.bar(df_grouped[df_grouped["inst25"] > 1000000], x="CLAVES", y="inst25", title="CANTIDADES DEMANDADAS POR IMSS PARA 2025")
        fig2 = px.bar(df_grouped[(df_grouped["inst25"] > 50000) & (df_grouped["inst25"] < 1000000)], x="CLAVES", y="inst25")
        fig3 = px.bar(df_grouped[(df_grouped["inst25"] > 1000) & (df_grouped["inst25"] < 50000)], x="CLAVES", y="inst25")
        fig4 = px.bar(df_grouped[(df_grouped["inst25"] > 0) & (df_grouped["inst25"] < 1000)], x="CLAVES", y="inst25")
        st.write(fig1)
        st.write(fig2)
        st.write(fig3)
        st.write(fig4)

    with col2:
        fig5 = px.bar(df_grouped[df_grouped["inst26"] > 1000000], x="CLAVES", y="inst26", title="CANTIDADES DEMANDADAS POR IMSS PARA 2025")
        fig6 = px.bar(df_grouped[(df_grouped["inst26"] > 50000) & (df_grouped["inst26"] < 1000000)], x="CLAVES", y="inst26")
        fig7 = px.bar(df_grouped[(df_grouped["inst26"] > 1000) & (df_grouped["inst26"] < 50000)], x="CLAVES", y="inst26")
        fig8 = px.bar(df_grouped[(df_grouped["inst26"] > 0) & (df_grouped["inst26"] < 1000)], x="CLAVES", y="inst26")
        st.write(fig5)
        st.write(fig6)
        st.write(fig7)
        st.write(fig8)

    selected_abasto = st.selectbox("Ingrese tipo de abastecimiento", list(abasto_options.keys()), key="demanda_abasto")
    abastecimiento = abasto_options[selected_abasto]

    selected_type = st.selectbox("Ingrese el tipo de clave", list(type_options.keys()), key="demanda_type")
    ty = type_options[selected_type]

    # Filtrar datos
    datos_filtrados_demanda25 = df[(df['CLAVES'].isin(cl)) & (df['INSTITUTO'] == inst25) & (df['ABASTO'].isin(abastecimiento))]
    datos_filtrados_demanda26 = df[(df['CLAVES'].isin(cl)) & (df['INSTITUTO'] == inst26) & (df['ABASTO'].isin(abastecimiento))]

    col25, col26 = st.columns(2)
    st.plotly_chart(crear_hist(datos_filtrados_demanda25), key="demanda_histogram")
    st.plotly_chart(crear_pie(datos_filtrados_demanda26), key="demanda_pie")

    st.header("Demanda")
    st.write(demanda.head())

# Incluir imagen como pie de página
st.image("footer.png", use_container_width=True)
