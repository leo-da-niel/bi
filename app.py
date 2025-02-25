import streamlit as st

# CSS personalizado para colorear las pestañas
st.markdown(
    """
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        margin-right: 5px;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #d1d5db;
    }
    .stTabs [aria-selected="true"] {
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Crear pestañas
tab1, tab2, tab3 = st.tabs(["Pestaña 1", "Pestaña 2", "Pestaña 3"])

# Contenido de cada pestaña
with tab1:
    st.header("Contenido de la Pestaña 1")
    st.write("¡Hola desde la Pestaña 1!")

with tab2:
    st.header("Contenido de la Pestaña 2")
    st.write("¡Hola desde la Pestaña 2!")

with tab3:
    st.header("Contenido de la Pestaña 3")
    st.write("¡Hola desde la Pestaña 3!")
