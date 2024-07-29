import pandas as pd
import nltk
from nltk import word_tokenize, download
import string
import numpy as np
from unidecode import unidecode
import spacy.cli
from sklearn.feature_extraction.text import TfidfVectorizer
import pt_core_news_sm
import streamlit as st

@st.cache_data(show_spinner=False, ttl=24*3600, max_entries=5)
def downloads_nlp():
    nlp = pt_core_news_sm.load()

    return nlp

def normalize(df: pd.DataFrame, column: str):
    """
    Normalizacao dos dados: stopwords, lowercase e unidecode.

    Recebe:
        df: dataframe com os dados
    Retorna:
        df['processed']: coluna do dataframe que passou por normalizacao
    """

    stopwords = nltk.corpus.stopwords.words('portuguese')
    palavras_extras = ['pra', 'pro', 'pq', 'https', 'etc', 'dão', 'após', 'apos', 'consigo']
    stopwords = np.concatenate([stopwords, palavras_extras, list(string.punctuation)])

    df['processed'] = df[column].apply(lambda x: ' '.join(
        unidecode(word.lower()) for word in word_tokenize(x) if word.lower() not in stopwords))

    return df

@st.cache_data(show_spinner=False, ttl=24*3600, max_entries=50)
def lemanization(text: list):
    """
    Lematização dos dados normalizados - Reduz o token ao lema.

    Recebe:
        text: texto a ser lematizado
    Retorna:
        texto lematizado como uma string
    """

    nlp = downloads_nlp()
    doc = nlp(text.lower())
    lemmatized_tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]
    return ' '.join(lemmatized_tokens)

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
