# -*- coding: utf-8 -*-
"""Text_analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-jb2PEpQaEKAasqcb5nmTQTeFm03luAl
"""
import streamlit as st
import pandas as pd
import nltk
from nltk import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns

# Download NLTK resources
nltk.download('punkt')
nltk.download('vader_lexicon')

# Function to perform Sentiment Analysis
def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = []
    words = word_tokenize(text)
    for word in words:
        score = sia.polarity_scores(word)['compound']
        sentiment_scores.append(score)
    return sentiment_scores

# Function to generate Word Cloud
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color ='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot()

# Main function
def main():
    st.title("Text Analysis App")

    # Option to upload a CSV file for sentiment analysis
    uploaded_file = st.file_uploader("Upload CSV file for sentiment analysis:", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        text_column = st.selectbox("Select text column:", df.columns)
        text = ' '.join(df[text_column].dropna())
        st.write("Uploaded Data:")
        st.dataframe(df, height=400)  # Display uploaded data in a table format

        # Analyze sentiment
        sentiment_scores = analyze_sentiment(text)
        st.write("Sentiment Scores:", sentiment_scores)

        # Generate sentiment histogram
        if sentiment_scores:
            plt.figure(figsize=(8, 5))
            sns.histplot(sentiment_scores, bins=20, kde=True)
            plt.xlabel('Sentiment Score')
            plt.ylabel('Frequency')
            st.pyplot()

        # Perform word frequency analysis
        word_freq = Counter(word_tokenize(text))
        word_freq_df = pd.DataFrame.from_dict(word_freq, orient='index', columns=['Frequency'])
        word_freq_df.index.name = 'Word'
        word_freq_df = word_freq_df.reset_index()
        st.write("Word Frequency Analysis:")
        st.dataframe(word_freq_df)

        # Generate Word Cloud
        wordcloud_analysis = st.checkbox("Generate Word Cloud")
        if wordcloud_analysis:
            generate_wordcloud(text)

if __name__ == "__main__":
    main()
