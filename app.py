import streamlit as st
import json
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Busca Blocos Carnaval SP 2025")

@st.cache_data
def load_data():
    with open('actual_data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    blocks = []
    for entry in data:
        try:
            route_desc = entry['fields']['routeDescription']['content'][0]['content'][0]['value']
        except (KeyError, IndexError, TypeError):
            route_desc = None
        block = {
            'name': entry['fields']['name'],
            'date': pd.to_datetime(entry['fields']['startDate']).strftime('%Y-%m-%d'),
            'start_time': pd.to_datetime(entry['fields']['startDate']).strftime('%H:%M'),
            'end_time': pd.to_datetime(entry['fields']['endDate']).strftime('%H:%M'),
            'address': entry['fields']['address'],
            'neighborhood': entry['fields']['neighborhood'],
            'estimated_audience': entry['fields']['estimatedAudience'],
            'instagram': entry['fields']['instagramLink'] if entry['fields']['instagramLink'] != "https://www.instagram.com/carnamaps/" else None,
            'route_description': route_desc
        }
        blocks.append(block)
    
    return pd.DataFrame(blocks).sort_values(by='name')

# App title
st.title('Busca Blocos do Carnaval de São Paulo 2025')

st.write('''
    O site oficial do carnaval de São Paulo não tem busca muito intuitiva, então obviamente fiz engenharia reversa do site oficial para pegar as informações brutas e fiquei até de madrugada fazendo um sitezinho para buscar os blocos. [O código está disponível no github](https://github.com/tiagofassoni/streamlit-carnaval-sp-2025).

    ### Como utilizar 

    Basta selecionar a data. Selecionando o bloco na tabela, você vai ver mais detalhes sobre o bloco.
    Explore os blocos do Carnaval de São Paulo 2025.
    Você pode filtrar por data e por nome do bloco. Selecionar um bloco mostrará mais detalhes sobre ele.
    Falta um mapa detalhado, que tem no site oficial, mas não aqui, mas era o que tinha pra hoje.

    ### Quem fez

    Oi, sou o Tiago Fassoni. Estou no [Bluesky](https://bsky.app/profile/tiagofassoni.bsky.social/) e no [Instagram](https://instagram.com/tiagofassoni).

    # Selecione a data e veja os blocos:
    
''')

# Load data
df = load_data()

# Format function for date filtering
def format_func(date):
    match date:
        case 'Todos os dias':
            return 'Todos os dias, incluindo os passados'
        case "2025-02-21":
            return "21 de fevereiro"
        case "2025-02-22":
            return "22 de fevereiro"
        case "2025-02-23":
            return "23 de fevereiro"
        case "2025-02-24":
            return "24 de fevereiro"
        case "2025-02-25":
            return "25 de fevereiro"    
        case "2025-02-26":
            return "26 de fevereiro"
        case "2025-02-28":
            return "28 de fevereiro"
        case "2025-03-01":
            return "1o de março"
        case "2025-03-02":
            return "2 de março"
        case "2025-03-03":
            return "3 de março"
        case "2025-03-04":
            return "4 de março"
        case "2025-03-08":
            return "8 de março"
        case "2025-03-09":
            return "9 de março"
        case _:
            return None


# Date filter
available_dates = ['Todos os dias'] + sorted(df['date'].unique())
default_date = datetime.now().strftime('%Y-%m-%d')
default_index = available_dates.index(default_date) if default_date in available_dates else 0
selected_date = st.selectbox('Selecione a data', available_dates, format_func=format_func, index=default_index)
# Search box
name_search = st.text_input('Filtre pelo nome')

# Apply filters
filtered_df = df.copy()
if selected_date != 'Todos os dias':
    filtered_df = filtered_df[filtered_df['date'] == selected_date]
if name_search:
    filtered_df = filtered_df[filtered_df['name'].str.contains(search, case=False)]

# Display the table
selected_indices = st.dataframe(
    filtered_df[['name', 'start_time', 'end_time', 'neighborhood']],
    column_config={
        'name': 'Nome do Bloco',
        'start_time': 'Hora de Início',
        'end_time': 'Hora de Término',	
        'neighborhood': 'Bairro',
        # 'address': 'Endereço',
        # 'date': 'Data',
        # 'estimated_audience': 'Público Estimado',
        # 'instagram': st.column_config.LinkColumn('Instagram'),
        # 'route_description': 'Rota'
    },
    selection_mode="single-row",
    hide_index=False,
    use_container_width=True,
    on_select="rerun",
    # on_click=lambda: None
)


# # Show details card when a row is selected
if len(selected_indices['selection']['rows']) > 0:

    selected_row = filtered_df.iloc[selected_indices['selection']['rows'][0]] 

    with st.container():
        st.markdown("---")
        st.subheader(selected_row['name'])
        
        # col1, col2 = st.columns(2)
        # with col1:
        st.write("📅 Data:", format_func(selected_row['date']))
        st.write("⏰ Horário:", f"{selected_row['start_time']} - {selected_row['end_time']}")
        st.write("📍 Bairro:", selected_row['neighborhood'])
        
        # with col2:
        st.write("🗺️ Endereço:", selected_row['address'])
        # st.write("👥 Público Estimado:", f"{selected_row['estimated_audience']:,}")
        if selected_row['instagram']:
            st.write("📱 Instagram:", f"[{selected_row['instagram']}]({selected_row['instagram']})")
        
        if selected_row['route_description']:
            st.write("🛣️ Rota do Bloco:")
            st.write(selected_row['route_description'])
else:
    st.write("⬆️ Selecione um bloco na tabela para ver mais detalhes.")