import streamlit as st
import plotly.express as px
import pandas as pd

def show_graphs(df, group_by):
    left,right = st.columns((2,1.5))
    with left:
        st.subheader("Gráficos")
        if group_by=="data":
            ts = df.groupby(pd.Grouper(key="data", freq="W")).agg({"custo":"sum"}).reset_index()
            fig_line = px.line(ts, x="data", y="custo", title="Custo por semana")
            st.plotly_chart(fig_line,use_container_width=True)
        else:
            agg = df.groupby(group_by).agg({"custo":"sum"}).reset_index()
            fig_bar = px.bar(agg, x=group_by, y="custo", title=f"Custo por {group_by}")
            st.plotly_chart(fig_bar,use_container_width=True)

        st.subheader("Histograma de Custos")
        fig_hist = px.histogram(df, x="custo", nbins=30, title="Distribuição de custos")
        st.plotly_chart(fig_hist,use_container_width=True)

    with right:
        st.subheader("Mapa de Obras")
        if {"lat","lon"}.issubset(df.columns):
            map_df = df[["lat","lon","custo","obra"]].dropna()
            st.map(map_df.rename(columns={"lat":"latitude","lon":"longitude"}))
            st.markdown("Top 5 registros por custo")
            st.dataframe(df.nlargest(5,"custo")[["data","obra","categoria","custo","progresso","funcionarios"]])
        else:
            st.info("Não há colunas 'lat' e 'lon' para mapa")
