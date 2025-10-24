import streamlit as st
import pandas as pd
import plotly.express as px

def show_materiais(df=None):
    st.subheader("📦 Materiais Utilizados")
    
    # Usa DataFrame do session_state se não for passado
    if df is None:
        df = st.session_state.get("materiais_data", pd.DataFrame(columns=["data","obra","material","custo"]))

    if df.empty:
        st.info("Ainda não há registros de materiais.")
        return

    # Certificar que coluna 'data' existe
    if "data" in df.columns:
        st.dataframe(df.sort_values("data"))
    else:
        st.dataframe(df)

    if "material" in df.columns:
        st.markdown("### Custo total por material")
        agg = df.groupby("material")["custo"].sum().reset_index()
        fig = px.bar(agg, x="material", y="custo", title="Custo por material")
        st.plotly_chart(fig, use_container_width=True)
