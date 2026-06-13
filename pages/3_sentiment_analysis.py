import streamlit as st
import pandas as pd
import plotly.express as px
from utils import compute_app_sentiment

st.title("Sentiment Analysis")

if "apps_df" in st.session_state and not st.session_state["apps_df"].empty:
    df = st.session_state["apps_df"]

    if st.button("Analyze Sentiment"):
        sentiment_results = []
        details_dict = {}

        progress = st.progress(0)
        for i, (_, row) in enumerate(df.iterrows()):
            with st.spinner(f"Analyse de {row['App']}..."):
                avg, details = compute_app_sentiment(row["AppId"], count=10)
                if avg is not None:
                    sentiment_results.append({"App": row["App"], "AppId": row["AppId"], "sentiment_score": avg})
                    details_dict[row["AppId"]] = details
            progress.progress((i + 1) / len(df))

        st.session_state["sentiment_df"] = pd.DataFrame(sentiment_results)
        st.session_state["sentiment_details"] = details_dict
        st.success("Analyse terminée !")

    if "sentiment_df" in st.session_state and not st.session_state["sentiment_df"].empty:
        sentiment_df = st.session_state["sentiment_df"]

        st.subheader("Sentiment Scores")
        st.dataframe(sentiment_df)

        fig = px.bar(sentiment_df, x="App", y="sentiment_score",
                    title="Average Sentiment Score per App",
                    color="sentiment_score", color_continuous_scale="RdYlGn")
        st.plotly_chart(fig)

        st.subheader("Review Details")
        selected = st.selectbox("Voir les avis pour", sentiment_df["App"])
        app_id = sentiment_df[sentiment_df["App"] == selected]["AppId"].values[0]

        details = st.session_state["sentiment_details"].get(app_id, [])
        for d in details:
            color = "green" if d["label"] == "POSITIVE" else "red"
            st.markdown(f":{color}[**{d['label']}** ({d['score']:.2f})] — {d['review']}")

else:
    st.warning("Effectuez une recherche d'abord (page 'results tables').")
