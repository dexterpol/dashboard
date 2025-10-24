import streamlit as st
from modules.notas_crud import adicionar_nota, deletar_nota, atualizar_nota
import pandas as pd
from datetime import date

def show_notas(df=None):
    st.subheader("📝 Notas / Observações")

    if df is None:
        df = st.session_state.get("notas_data", pd.DataFrame(columns=["data","obra","observacoes"]))

    if df.empty:
        st.info("Ainda não há notas registradas.")
        return

    # Adicionar nova nota
    with st.expander("➕ Adicionar nova nota"):
        if "obras" in st.session_state and not st.session_state["obras"].empty:
            obra_sel = st.selectbox("Selecione a obra", st.session_state["obras"]["obra"], key="nota_obra")
            observacoes = st.text_area("Observações", key="nota_obs")
            data_nota = st.date_input("Data da nota", value=date.today(), key="nota_data")

            if st.button("Adicionar nota"):
                adicionar_nota(obra_sel, observacoes, data_nota)

    # Exibir notas
    st.markdown("### Histórico de notas")
    st.dataframe(df.sort_values("data", ascending=False).reset_index(drop=True))
