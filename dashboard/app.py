from api.analysis import get_analysis
import streamlit as st
from ui.sidebar import sidebar_filters
from helpers.kpi import (
    tokens_trend, 
    cost_distribution, 
    calculate_kpis,
)
from helpers.format import format_number
from helpers.plots import (
    satisfaction_trend,
)
from helpers.daterange_filter import filter_by_date_range

st.set_page_config(page_title="Monitoramento Chatbot", layout="wide")

df = get_analysis()

selected_motel, selected_analysis_date, selected_session_date = sidebar_filters(motel_df=df[["motel_name",
                                                                                             "motel_id"]],
                                                                                date_df=df[['analysis_created_at',
                                                                                            'session_created_at']])

if selected_motel:
    df = df[df["motel_id"] == selected_motel]

if selected_session_date:
    df = filter_by_date_range(df=df,
                              date_column="session_created_at",
                              date_range=selected_session_date)
if selected_analysis_date:
    df = filter_by_date_range(df=df,
                              date_column="analysis_created_at",
                              date_range=selected_analysis_date)

st.title("📊 Monitoramento de Interação Humano-Chatbot")

kpis = calculate_kpis(df=df)
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("📌 Total de Sessões", format_number(kpis["total_sessions"]))
col2.metric("💬 Média de Satisfação", kpis["avg_satisfaction"])
col3.metric("📝 Tokens Gastos (Entrada/Saída)", f'{format_number(kpis["total_input_tokens"])} / {format_number(kpis["total_output_tokens"])}')
col4.metric("📊 Média de Tokens Gastos (Entrada/Saída)", 
          f'{format_number(kpis["avg_input_tokens"])} / {format_number(kpis["avg_output_tokens"])}')
col5.metric("💲 Custo Total", f"${format_number(kpis['total_cost'])}")

st.subheader("📈 Análises e Insights")

st.pyplot(satisfaction_trend(df=df))

col1, col2 = st.columns(2)
with col1:
    st.pyplot(tokens_trend(df=df))
with col2:
    st.pyplot(cost_distribution(df=df))