import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --- FUNZIONE ---
def consiglia_paesi(df, user_input, top_n=5):
    orig = user_input["origin_country"]
    sex = user_input["sex"]
    migliora = user_input["indici_da_migliorare"]
    desidera = user_input["indici_desiderati"]

    df_user = df[(df["country_of_birth"] == orig) & (df["sex"] == sex)].copy()

    def calcola_punteggio(r):
        score = 0
        motivi = []

        for ind, peso in migliora.items():
            delta = r[f"dest_{ind}"] - r[f"origin_{ind}"]
            contrib = max(delta, 0) * peso
            score += contrib
            if delta > 0:
                motivi.append(f"{ind} ↑ (+{delta:.2f})")

        for ind, peso in desidera.items():
            val = r[f"dest_{ind}"]
            contrib = val * peso
            score += contrib
            motivi.append(f"{ind} = {val:.2f}")

        return pd.Series({"score": score, "motivi": ", ".join(motivi)})

    df_user[["score", "motivi"]] = df_user.apply(calcola_punteggio, axis=1)

    min_score = df_user["score"].min()
    max_score = df_user["score"].max()
    df_user["score_norm"] = (df_user["score"] - min_score) / (max_score - min_score + 1e-9)

    ranking = (
        df_user.groupby("country_of_destination")
        .agg({
            "score_norm": "mean",
            "motivi": lambda x: x.mode().iloc[0] if not x.mode().empty else x.iloc[0]
        })
        .sort_values("score_norm", ascending=False)
        .reset_index()
        .head(top_n)
    )
    return ranking

# --- INTERFACCIA APP ---
st.set_page_config(page_title="GoWhere", layout="wide")
st.title("🌍 GoWhere - Trova il tuo paese ideale")
st.markdown("Rispondi a poche domande e scopri in quali paesi potresti vivere meglio!")

# Input
sex = st.selectbox("Qual è il tuo sesso?", ["Male", "Female"])
origin_country = st.text_input("Inserisci il tuo paese di origine (es. ITA):", "ITA")

st.subheader("Cosa vuoi migliorare?")
income = st.slider("Reddito", 0, 5, 3)
jobs = st.slider("Opportunità di lavoro", 0, 5, 3)
safety = st.slider("Sicurezza", 0, 5, 3)

st.subheader("Cosa ti interessa di più?")
life = st.slider("Soddisfazione di vita", 0, 5, 3)
env = st.slider("Ambiente", 0, 5, 2)

# Bottone
if st.button("🔍 Scopri i paesi migliori"):
    try:
        df = pd.read_csv("dataset_final.csv")  # deve stare nella stessa repo
        user_input = {
            "sex": sex,
            "origin_country": origin_country,
            "indici_da_migliorare": {
                "Income": income,
                "Safety": safety,
                "Jobs": jobs
            },
            "indici_desiderati": {
                "Life satisfaction": life,
                "Environment": env
            }
        }

        risultato = consiglia_paesi(df, user_input)

        st.subheader("🔝 Paesi consigliati:")
        st.dataframe(risultato)

        # Grafico
        st.subheader("📊 Punteggi Normalizzati")
        fig, ax = plt.subplots()
        ax.barh(risultato["country_of_destination"], risultato["score_norm"], color="mediumseagreen")
        ax.set_xlabel("Punteggio normalizzato (0–1)")
        ax.set_title("Top Paesi Consigliati")
        ax.invert_yaxis()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Errore nel caricamento dei dati o calcolo: {e}")

