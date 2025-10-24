import streamlit as st
import pandas as pd
import plotly.express as px

def show_funcionarios(df=None):
    st.subheader("👷 Funcionários")
    
    # Usa DataFrame do session_state se não for passado
    if df is None:
        df = st.session_state.get("funcionarios_data", pd.DataFrame(columns=["data","obra","funcionario","presente"]))

    if df.empty:
        st.info("Ainda não há registros de presença de funcionários.")
        return

    # Certificar que colunas existem
    st.dataframe(df.sort_values(["obra","data"]) if "data" in df.columns else df)

    if "funcionario" in df.columns and "presente" in df.columns:
        st.markdown("### Presença por funcionário")
        presenca = df.groupby("funcionario")["presente"].sum().reset_index()
        fig = px.bar(presenca, x="funcionario", y="presente", title="Dias presentes por funcionário")
        st.plotly_chart(fig, use_container_width=True)
