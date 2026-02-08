import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuração da página para telemóvel
st.set_page_config(page_title="Ironman Tracker", layout="centered")

FICHEIRO_TREINOS = 'treinos_ironman.csv'

# Título e Estilo
st.title("🚀 Ironman Training Tracker")
st.markdown("Registe o seu caminho até à linha de meta!")

# --- ÁREA DE INPUT ---
st.subheader("Registar Novo Treino")

with st.form("form_treino", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        data = st.date_input("Data do Treino", datetime.now())
        modalidade = st.selectbox("Modalidade", ["Natação", "Ciclismo", "Corrida"])
    
    with col2:
        distancia = st.number_input("Distância (km ou metros)", min_value=0.0, step=0.1)
        tempo = st.text_input("Tempo (HH:MM)", placeholder="01:30")

    submetido = st.form_submit_button("Guardar Treino")

    if submetido:
        # Lógica de cálculo simplificada para o exemplo
        novo_treino = pd.DataFrame([[data, modalidade, distancia, tempo]], 
                                   columns=['Data', 'Modalidade', 'Distancia', 'Tempo'])
        
        # Guardar no CSV (se não existe, cria; se existe, acrescenta)
        if not os.path.isfile(FICHEIRO_TREINOS):
            novo_treino.to_csv(FICHEIRO_TREINOS, index=False)
        else:
            novo_treino.to_csv(FICHEIRO_TREINOS, mode='a', header=False, index=False)
        
        st.success(f"Treino de {modalidade} guardado!")

# --- EXIBIÇÃO E ESTATÍSTICAS ---
st.divider()
st.subheader("📊 O Teu Progresso")

if os.path.isfile(FICHEIRO_TREINOS):
    df = pd.read_csv(FICHEIRO_TREINOS)
    
    # Mostrar Totais Acumulados
    totais = df.groupby('Modalidade')['Distancia'].sum()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("🏊 Natação", f"{totais.get('Natação', 0)} m")
    c2.metric("🚴 Ciclismo", f"{totais.get('Ciclismo', 0)} km")
    c3.metric("🏃 Corrida", f"{totais.get('Corrida', 0)} km")

    # Tabela de Histórico
    st.write("### Histórico de Treinos")
    st.dataframe(df.sort_values(by='Data', ascending=False), use_container_width=True)
else:
    st.info("Ainda não tens treinos registados. Começa agora!")