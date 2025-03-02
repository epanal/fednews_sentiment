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

# Function to fetch posts and analyze comments' sentiment
def fetch_fednews_comments(limit=5, comment_limit=10):
    posts = []
    for post in reddit.subreddit("fednews").hot(limit=limit):  # Fetch hottest posts
        post.comment_sort = "top"  # Get top comments
        post.comments.replace_more(limit=0)  # Remove "More comments" links
        
        comment_sentiments = []
        for comment in post.comments.list()[:comment_limit]:  # Limit number of comments per post
            score = analyzer.polarity_scores(comment.body)["compound"]
            comment_sentiments.append(score)
        
        # Aggregate sentiment scores (e.g., average)
        avg_sentiment = sum(comment_sentiments) / len(comment_sentiments) if comment_sentiments else 0
        sentiment_label = (
            "Positive" if avg_sentiment > 0.05 else "Negative" if avg_sentiment < -0.05 else "Neutral"
        )
        
        posts.append({
            "title": f"[{post.title}](https://www.reddit.com{post.permalink})",  # Clickable title
            "sentiment": sentiment_label,
            "avg_comment_sentiment_score": avg_sentiment,
        })
    
    return pd.DataFrame(posts)

# Streamlit UI
st.title("📊 Federal News Comments Sentiment Tracker")

# Slider for the number of posts to analyze
num_posts = st.slider("Number of hottest posts to analyze", 1, 10, 5)
num_comments = st.slider("Max comments per post", 1, 20, 10)

# Fetch & analyze posts
df = fetch_fednews_comments(num_posts, num_comments)

# Sentiment Count Plot
sentiment_counts = df["sentiment"].value_counts()

# Define custom colors
color_map = {"Positive": "green", "Neutral": "gray", "Negative": "red"}

# Create pie chart with custom colors
fig = px.pie(
    names=sentiment_counts.index, 
    values=sentiment_counts.values, 
    title="Sentiment Breakdown",
    color=sentiment_counts.index,  # Assign colors based on sentiment
    color_discrete_map=color_map   # Apply custom color mapping
)

# Display results
st.dataframe(df)
st.plotly_chart(fig)