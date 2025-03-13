import streamlit as st

# Inicializar el estado de la sesión para los filtros
if 'filters' not in st.session_state:
    st.session_state.filters = []

# Función para agregar un nuevo filtro
def add_filter():
    st.session_state.filters.append({
        'field': st.selectbox('Campo', ['Abasto', 'Tipo', 'Clave', 'Periodo'], key=f'field_{len(st.session_state.filters)}'),
        'value': st.text_input('Valor', key=f'value_{len(st.session_state.filters)}')
    })

# Botón para agregar un nuevo filtro
st.button('Agregar Filtro', on_click=add_filter)

# Mostrar los filtros aplicados
for i, filter in enumerate(st.session_state.filters):
    st.write(f"Filtro {i+1}: {filter['field']} = {filter['value']}")

# Función para filtrar los catálogos
def filter_catalogs(data, filters):
    for filter in filters:
        if filter['field'] == 'Abasto':
            data = data[data['CLAVES'].isin(abasto_options[filter['value']])]
        elif filter['field'] == 'Tipo':
            data = data[data['CLAVES'].isin(type_options[filter['value']])]
        elif filter['field'] == 'Clave':
            data = data[data['CLAVES'].isin([filter['value']])]
        elif filter['field'] == 'Periodo':
            data = data[data['PERIODO'] == filter['value']]
    return data

# Ejemplo de datos
import pandas as pd

# Crear un DataFrame de ejemplo
data = pd.DataFrame({
    'CLAVES': ['A', 'B', 'C', 'D', 'E'],
    'PERIODO': ['2025', '2025', '2026', '2026', 'BIANUAL']
})

# Filtrar los datos según los filtros aplicados
filtered_data = filter_catalogs(data, st.session_state.filters)

# Mostrar los datos filtrados
st.write('Datos Filtrados:', filtered_data)


