import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
from wordcloud import WordCloud

st.title("Visualizations")

if "apps_df" in st.session_state and not st.session_state["apps_df"].empty:
    df = st.session_state["apps_df"]

    # Sidebar filter by App ID
    app_ids = df["AppId"].unique()
    selected_app = st.sidebar.selectbox("Select App", app_ids)
    filtered_df = df[df["AppId"] == selected_app]

    st.subheader("Filtered App")
    st.dataframe(filtered_df)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ratings by App")
        st.bar_chart(df.set_index("App")["Score"])

    with col2:
        st.subheader("Free vs Paid")
        free_counts = df["Free"].value_counts()
        fig, ax = plt.subplots()
        ax.pie(free_counts, labels=free_counts.index.map({True: "Free", False: "Paid"}),
            autopct="%1.1f%%")
        st.pyplot(fig)

    st.subheader("Word Cloud (App Names)")
    text = " ".join(df["App"].tolist())
    wc = WordCloud(width=800, height=400, background_color="white").generate(text)
    fig_wc, ax_wc = plt.subplots()
    ax_wc.imshow(wc)
    ax_wc.axis("off")
    st.pyplot(fig_wc)

    st.subheader("Ratings Distribution")
    fig2 = px.histogram(df, x="Score", title="Ratings Distribution", nbins=10)
    st.plotly_chart(fig2)

    st.subheader("Top Apps by Score")
    top_apps = df.sort_values(by="Score", ascending=False).head(10)
    fig3 = px.bar(top_apps, x="App", y="Score", title="Top Apps by Score")
    st.plotly_chart(fig3)

    st.subheader("Score vs Installs")
    fig4 = px.scatter(df, x="Installs", y="Score", text="App", size="Score",
                    color="Free", title="Score vs Installs")
    fig4.update_traces(textposition="top center")
    st.plotly_chart(fig4)

    st.subheader("Installs Treemap")
    fig5 = px.treemap(df, path=["Genre", "App"], values="Installs", color="Score",
                    title="Market Share by Installs")
    st.plotly_chart(fig5)

else:
    st.warning("Effectuez une recherche d'abord (page 'results tables').")
