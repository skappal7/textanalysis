# -*- coding: utf-8 -*-
"""Text_analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-jb2PEpQaEKAasqcb5nmTQTeFm03luAl
"""
import streamlit as st
import pandas as pd
import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from textblob import TextBlob

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

# Function to perform Sentiment Analysis
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0:
        return 'Positive'
    elif sentiment_score < 0:
        return 'Negative'
    else:
        return 'Neutral'

# Function to perform Named Entity Recognition
def analyze_entities(text):
    entities = []
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        tagged_words = nltk.pos_tag(words)
        chunked = nltk.ne_chunk(tagged_words)
        entities.extend([(c[0], c.label()) for c in chunked if hasattr(c, 'label')])
    return entities

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
        st.write("Text for sentiment analysis:", text)
        sentiment = analyze_sentiment(text)
        st.write("Sentiment:", sentiment)

        # Generate sentiment histogram
        if sentiment:
            sentiments = [analyze_sentiment(row) for row in df[text_column].dropna()]
            sentiment_df = pd.DataFrame(sentiments, columns=['Sentiment'])
            st.write("Sentiment Histogram:")
            st.bar_chart(sentiment_df['Sentiment'].value_counts())

        # Display uploaded data in a table
        st.write("Uploaded Data:")
        st.dataframe(df, height=400)

    # User text input
    text = st.text_area("Or enter text for analysis:")

    # Sidebar for analysis selection
    st.sidebar.title("Analysis Selection")
    ner_analysis = st.sidebar.checkbox("Named Entity Recognition")
    wordcloud_analysis = st.sidebar.checkbox("Word Cloud")

    if st.button("Analyze"):
        # Perform Named Entity Recognition
        if ner_analysis:
            entities = analyze_entities(text)
            entities_df = pd.DataFrame(entities, columns=['Entity', 'Type'])
            st.write("Named Entities:")
            st.dataframe(entities_df)

        # Generate Word Cloud
        if wordcloud_analysis:
            generate_wordcloud(text)

        # Display results in a table
        if ner_analysis:
            st.write("Analysis Results:")
            st.write(pd.DataFrame({'Text': [text]}))

        # Download results as CSV
        if st.button("Download CSV"):
            if ner_analysis:
                pd.DataFrame({'Text': [text]}).to_csv('analysis_results.csv', index=False)
                st.success("Results downloaded successfully!")

if __name__ == "__main__":
    main()
