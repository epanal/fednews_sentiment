import praw
import pandas as pd
import plotly.express as px
import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Read credentials from Streamlit secrets
reddit = praw.Reddit(
    client_id=st.secrets["client_id"],
    client_secret=st.secrets["client_secret"],
    user_agent=st.secrets["user_agent"]
)

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Function to fetch latest posts with sentiment analysis
def fetch_fednews_posts(limit=10):
    posts = []
    for post in reddit.subreddit("fednews").hot(limit=limit):
        sentiment_score = analyzer.polarity_scores(post.title)["compound"]
        sentiment_label = (
            "Positive" if sentiment_score > 0.05 else "Negative" if sentiment_score < -0.05 else "Neutral"
        )
        post_url = f"https://www.reddit.com{post.permalink}"
        posts.append({
            "Title": post.title, 
            "Sentiment": sentiment_label, 
            "Score": sentiment_score, 
            "Reddit Link": post_url
        })
    return pd.DataFrame(posts)

# Streamlit UI
st.title("📊 Federal News Sentiment Tracker")

# User input for number of posts
num_posts = st.slider("Select number of posts to fetch:", min_value=5, max_value=20, value=10)

# Fetch & analyze posts
df = fetch_fednews_posts(num_posts)

# Sentiment Count Plot
sentiment_counts = df["Sentiment"].value_counts()
fig = px.pie(
    names=sentiment_counts.index, 
    values=sentiment_counts.values, 
    title="Sentiment Breakdown",
    color=sentiment_counts.index,
    color_discrete_map={"Positive": "green", "Neutral": "gray", "Negative": "red"}
)

# Display DataFrame with Clickable Links
st.subheader("🔗 Ethan's Sentiment tracker for latest r/fednews")
df_display = df.copy()
df_display["Reddit Link"] = df_display["Reddit Link"].apply(lambda x: f"[🔗 Link]({x})")
st.write(df_display.to_markdown(index=False), unsafe_allow_html=True)

# Show Sentiment Pie Chart
st.plotly_chart(fig)
