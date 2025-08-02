import streamlit as st

st.set_page_config(page_title="GoWhere", layout="wide")
st.title("🌍 GoWhere - Trova il tuo paese ideale")

st.markdown("Rispondi a poche domande e scopri in quali paesi potresti vivere meglio!")

sex = st.selectbox("Qual è il tuo sesso?", ["Male", "Female"])
origin_country = st.text_input("Inserisci il tuo paese di origine (es. ITA):")

st.subheader("Cosa vuoi migliorare?")
income = st.slider("Reddito", 0, 5, 3)
jobs = st.slider("Opportunità di lavoro", 0, 5, 3)
safety = st.slider("Sicurezza", 0, 5, 3)

st.subheader("Cosa ti interessa di più?")
life = st.slider("Soddisfazione di vita", 0, 5, 3)
env = st.slider("Ambiente", 0, 5, 2)

if st.button("🔍 Scopri i paesi migliori"):
    st.success("🚀 Qui appariranno i risultati personalizzati!")
