import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import numpy as np
from unidecode import unidecode
from sklearn.feature_extraction.text import TfidfVectorizer
import streamlit as st

# Baixar recursos do NLTK necessários
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Função para baixar e configurar recursos do NLP
@st.cache_data(show_spinner=False, ttl=24*3600, max_entries=5)
def downloads_nlp():
    stop_words = set(stopwords.words('portuguese'))
    lemmatizer = WordNetLemmatizer()
    return stop_words, lemmatizer

# Função para normalizar dados
def normalize(df: pd.DataFrame, column: str):
    """
    Normalização dos dados: stopwords, lowercase e unidecode.

    Recebe:
        df: dataframe com os dados
    Retorna:
        df['processed']: coluna do dataframe que passou por normalização
    """
    stop_words, _ = downloads_nlp()

    palavras_extras = ['pra', 'pro', 'pq', 'https', 'etc', 'dão', 'após', 'apos', 'consigo']
    stop_words = stop_words.union(set(palavras_extras), set(string.punctuation))

    df['processed'] = df[column].apply(lambda x: ' '.join(
        unidecode(word.lower()) for word in word_tokenize(x) if word.lower() not in stop_words))

    return df

# Função para lematizar textos
@st.cache_data(show_spinner=False, ttl=24*3600, max_entries=50)
def lemanization(text: list):
    """
    Lematização dos dados normalizados - Reduz o token ao lema.

    Recebe:
        text: texto a ser lematizado
    Retorna:
        texto lematizado como uma string
    """
    _, lemmatizer = downloads_nlp()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in word_tokenize(text.lower()) if word.isalpha()]
    return ' '.join(lemmatized_tokens)

# Função para processar TF-IDF
@st.cache_data(show_spinner=False, ttl=24*3600, max_entries=50)
def tfidf_processing(sentences: list, gram: int):
    """
    Aplicação da técnica TF-IDF para encontrar as palavras mais relevantes e seus respectivos pesos no corpus
    Criação do dataframe com o bigrama ou trigrama e seu respectivo rank (soma dos pesos TF-IDF).

    Recebe:
        sentences: sentenças
        gram: quantidade de palavras por tokens
    Retorna:
        df_rankeado: dataframe com termos e ranks ordenados
    """
    vec_tdidf = TfidfVectorizer(ngram_range=(gram, gram))
    tfidf = vec_tdidf.fit_transform(sentences)
    features = vec_tdidf.get_feature_names_out()
    
    soma = tfidf.sum(axis=0)
    df_final = []

    for col, term in enumerate(features):
        df_final.append((term, soma[0, col]))
    ranking = pd.DataFrame(df_final, columns=['termo', 'rank'])
    df_rankeado = (ranking.sort_values('rank', ascending=True))
    df_rankeado['termo'] = df_rankeado['termo'].apply(lambda x: x.capitalize())

    return df_rankeado
