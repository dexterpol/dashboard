import streamlit as st
from utils import to_csv_bytes, to_excel_bytes

def export_data(df):
    st.download_button("⬇️ Baixar CSV", data=to_csv_bytes(df), file_name="dados_filtrados.csv", mime="text/csv")
    if st.button("Exportar para Excel"):
        st.download_button("⬇️ Baixar XLSX", data=to_excel_bytes(df), file_name="dados_filtrados.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
