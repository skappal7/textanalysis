# -*- coding: utf-8 -*-
"""Text_analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-jb2PEpQaEKAasqcb5nmTQTeFm03luAl
"""
import streamlit as st
import pandas as pd
import mysql.connector
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import nltk

# Download NLTK resources
nltk.download('punkt')

# Function to perform sentiment analysis using TextBlob
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0:
        return "Positive"
    elif sentiment_score < 0:
        return "Negative"
    else:
        return "Neutral"

# Function to perform named entity recognition using NLTK
def analyze_named_entities(text):
    entities = []
    for chunk in ne_chunk(pos_tag(word_tokenize(text))):
        if isinstance(chunk, Tree):
            entities.append(" ".join([token for token, pos in chunk.leaves()]))
    return entities

# Function to connect to MySQL database
def connect_to_mysql(host, user, password, database):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

# Streamlit app
def main():
    st.set_page_config(
        page_title="Text Analytics",
        layout="wide",
        initial_sidebar_state="expanded",
        page_icon=":memo:",
        )
    st.title("Text Analytics")
    
    # Upload CSV or connect to MySQL
    upload_option = st.radio("Select data source:", ("Upload CSV", "Connect to MySQL"))
    
    # Text analytics options
    st.sidebar.title("Text Analytics Options")
    sentiment_analysis = st.sidebar.checkbox("Sentiment Analysis")
    named_entity_recognition = st.sidebar.checkbox("Named Entity Recognition")
    
    # If MySQL option is selected, ask for credentials
    if upload_option == "Connect to MySQL":
        st.subheader("MySQL Database Connection")
        host = st.text_input("Host")
        user = st.text_input("User")
        password = st.text_input("Password", type="password")
        database = st.text_input("Database")
        conn = connect_to_mysql(host, user, password, database)
        if conn is not None:
            cursor = conn.cursor()
            table_name = st.text_input("Table Name")
            if st.button("Fetch Data"):
                cursor.execute(f"SELECT * FROM {table_name}")
                data = cursor.fetchall()
                df = pd.DataFrame(data, columns=[i[0] for i in cursor.description])
                st.write(df)
    
    # If CSV option is selected, upload file
    else:
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.write(df)
    
    # Perform text analytics based on selected options
    if st.button("Perform Text Analytics"):
        if sentiment_analysis:
            st.subheader("Sentiment Analysis Results")
            if 'text' in df.columns:
                df['Sentiment'] = df['text'].apply(analyze_sentiment)
                st.write(df[['text', 'Sentiment']])
            else:
                st.warning("No 'text' column found in the data.")
        
        if named_entity_recognition:
            st.subheader("Named Entity Recognition Results")
            if 'text' in df.columns:
                df['Entities'] = df['text'].apply(analyze_named_entities)
                st.write(df[['text', 'Entities']])
            else:
                st.warning("No 'text' column found in the data.")
    
    # Visualizations
    st.sidebar.title("Visualizations")
    if st.sidebar.checkbox("Show Histogram"):
        st.subheader("Histogram")
        if 'text' in df.columns:
            text_column = st.sidebar.selectbox("Select column for histogram:", df.columns)
            fig, ax = plt.subplots(figsize=(8, 6))  # Set a smaller figure size
            df[text_column].hist(ax=ax)  # Plot the histogram on the axes
            st.pyplot(fig)  # Display the figure using st.pyplot()
        else:
            st.warning("No data to display.")
    
    if st.sidebar.checkbox("Show Word Cloud"):
        st.subheader("Word Cloud")
        if 'text' in df.columns:
            text = ' '.join(df['text'])
            wordcloud = WordCloud().generate(text)
            fig, ax = plt.subplots(figsize=(8, 6))  # Set a smaller figure size
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis("off")
            st.pyplot(fig)  # Display the figure using st.pyplot()
        else:
            st.warning("No data to display.")

if __name__ == "__main__":
    main()
