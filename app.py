import streamlit as st

# Inicializar el estado de la sesión para los filtros
if 'filters' not in st.session_state:
    st.session_state.filters = []

# Función para agregar un nuevo filtro
def add_filter():
    st.session_state.filters.append({
        'field': st.selectbox('Campo', ['Campo1', 'Campo2', 'Campo3'], key=f'field_{len(st.session_state.filters)}'),
        'value': st.text_input('Valor', key=f'value_{len(st.session_state.filters)}')
    })

# Botón para agregar un nuevo filtro
st.button('Agregar Filtro', on_click=add_filter)

# Mostrar los filtros aplicados
for i, filter in enumerate(st.session_state.filters):
    st.write(f"Filtro {i+1}: {filter['field']} = {filter['value']}")

# Función para filtrar los catálogos
def filter_catalogs(catalogs, filters):
    for filter in filters:
        catalogs = [item for item in catalogs if filter['value'] in item[filter['field']]]
    return catalogs

# Ejemplo de catálogos
catalogs = [
    {'Campo1': 'A', 'Campo2': 'B', 'Campo3': 'C'},
    {'Campo1': 'D', 'Campo2': 'E', 'Campo3': 'F'},
    {'Campo1': 'G', 'Campo2': 'H', 'Campo3': 'I'}
]

# Filtrar los catálogos según los filtros aplicados
filtered_catalogs = filter_catalogs(catalogs, st.session_state.filters)

# Mostrar los catálogos filtrados
st.write('Catálogos Filtrados:', filtered_catalogs)
