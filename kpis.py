# kpis.py
import streamlit as st

def show_kpis(df_filtrado, df_funcionarios):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Custo (R$)", f"{df_filtrado['custo'].sum():,.2f}" if not df_filtrado.empty else "0")
    with col2:
        st.metric("Média Progresso (%)", f"{df_filtrado['progresso'].mean():.2f}" if not df_filtrado.empty else "0")
    with col3:
        st.metric("Total Funcionários", f"{df_funcionarios['funcionario'].nunique()}" if not df_funcionarios.empty else "0")
    with col4:
        st.metric("Última Data", f"{df_filtrado['data'].max() if not df_filtrado.empty else '—'}")
