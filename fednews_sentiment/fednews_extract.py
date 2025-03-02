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
def fetch_fednews_comments(sort_by="hot", limit=5, comment_limit=10):
    posts = []
    
    # Select sorting method based on user choice
    if sort_by == "hot":
        subreddit_posts = reddit.subreddit("fednews").hot(limit=limit)
    elif sort_by == "new":
        subreddit_posts = reddit.subreddit("fednews").new(limit=limit)
    elif sort_by == "top":
        subreddit_posts = reddit.subreddit("fednews").top(limit=limit)
    else:
        subreddit_posts = reddit.subreddit("fednews").hot(limit=limit)  # Default fallback
    
    for post in subreddit_posts:
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
            "title": f"[{post.title.replace('|', '&#124;')}](https://www.reddit.com{post.permalink})",
            "sentiment": sentiment_label,
            "comment_score": avg_sentiment,
        })
    
    return pd.DataFrame(posts)

# Streamlit UI
st.title("📊 r/fednews Post Sentiment")

# Dropdown for sorting method
sort_option = st.selectbox("Sort posts by", ["hot", "new", "top"], index=0)

# Sentiment filter selection
sentiment_filter = st.radio("Filter posts by sentiment", ["All", "Positive", "Negative"])

# Number of posts to analyze (fixed)
#num_posts = st.slider("Number of posts to analyze", 1, 10, 5)
num_posts = 15
num_comments = 15

# Fetch & analyze posts
df = fetch_fednews_comments(sort_by=sort_option, limit=num_posts, comment_limit=num_comments)

# Apply sentiment filter
if sentiment_filter == "Positive":
    df = df[df["sentiment"] == "Positive"]
elif sentiment_filter == "Negative":
    df = df[df["sentiment"] == "Negative"]

# Display filtered results
st.write(df.to_markdown(index=False), unsafe_allow_html=True)

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
st.plotly_chart(fig)
