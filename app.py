import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuração da página para Mobile e Desktop
st.set_page_config(
    page_title="Ironman Tracker",
    page_icon="🚀",
    layout="centered"
)

# Nome do ficheiro de dados
FICHEIRO_TREINOS = 'treinos_ironman.csv'

# --- FUNÇÕES DE APOIO ---
def calcular_ritmo(modalidade, distancia, tempo_str):
    try:
        # Converter HH:MM para minutos totais
        horas, minutos = map(int, tempo_str.split(':'))
        minutos_totais = (horas * 60) + minutos
        
        if distancia <= 0 or minutos_totais <= 0:
            return "N/A"

        if modalidade == "Ciclismo":
            # Velocidade média em km/h
            velocidade = distancia / (minutos_totais / 60)
            return f"{velocidade:.2f} km/h"
        else:
            # Pace em min/km ou min/100m
            pace_decimal = minutos_totais / distancia
            pace_minutos = int(pace_decimal)
            pace_segundos = int((pace_decimal - pace_minutos) * 60)
            return f"{pace_minutos}:{pace_segundos:02d} min/un"
    except:
        return "Erro"

# --- INTERFACE ---
st.title("🚀 Ironman Training Tracker")
st.markdown("Foca no processo, a linha de meta é apenas a consequência.")

# --- FORMULÁRIO DE ENTRADA ---
st.subheader("📍 Registar Novo Treino")
with st.form("form_treino", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        data = st.date_input("Data", datetime.now())
        modalidade = st.selectbox("Modalidade", ["Natação", "Ciclismo", "Corrida"])
    
    with col2:
        distancia = st.number_input("Distância (km ou metros)", min_value=0.0, step=0.1)
        tempo = st.text_input("Tempo (HH:MM)", placeholder="ex: 01:20")

    submetido = st.form_submit_button("Guardar Treino")

    if submetido:
        ritmo = calcular_ritmo(modalidade, distancia, tempo)
        
        # Criar linha de dados
        novo_dado = pd.DataFrame([{
            'Data': data,
            'Modalidade': modalidade,
            'Distancia': distancia,
            'Tempo': tempo,
            'Ritmo': ritmo
        }])
        
        # Salvar no CSV
        if not os.path.isfile(FICHEIRO_TREINOS):
            novo_dado.to_csv(FICHEIRO_TREINOS, index=False)
        else:
            novo_dado.to_csv(FICHEIRO_TREINOS, mode='a', header=False, index=False)
        
        st.success(f"Treino de {modalidade} registado com sucesso!")

# --- VISUALIZAÇÃO DE DADOS ---
st.divider()
st.subheader("📊 Análise de Performance")

if os.path.isfile(FICHEIRO_TREINOS):
    df = pd.read_csv(FICHEIRO_TREINOS)
    df['Data'] = pd.to_datetime(df['Data'])
    
    # Cartões de Métricas (Volume Total)
    totais = df.groupby('Modalidade')['Distancia'].sum()
    
    m1, m2, m3 = st.columns(3)
    m1.metric("🏊 Natação", f"{totais.get('Natação', 0):.0f} m")
    m2.metric("🚴 Ciclismo", f"{totais.get('Ciclismo', 0):.1f} km")
    m3.metric("🏃 Corrida", f"{totais.get('Corrida', 0):.1f} km")

    # Gráfico de Volume
    st.write("### Volume Acumulado")
    st.bar_chart(totais)

    # Tabela de Histórico
    st.write("### Histórico de Atividades")
    st.dataframe(df.sort_values(by='Data', ascending=False), use_container_width=True)
else:
    st.info("Ainda não tens treinos gravados. Começa hoje!")
