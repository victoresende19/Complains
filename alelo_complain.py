import pandas as pd
import streamlit as st
import nltk
import spacy.cli
from utils.topic import normalize, lemanization, tfidf_processing
from utils.style import style
from utils.plots import bar_plot
from utils.web_scrapping import web_scrapping

@st.cache_data(show_spinner=False, ttl=24*3600, max_entries=5)
def nlp_download():
    nltk.download('wordnet')
    nltk.download('punkt')
    nltk.download('stopwords')

nlp_download()

st.set_page_config(layout="wide", page_icon='https://yt3.googleusercontent.com/ytc/AIdro_n0FdMVgTUfGUXHFP32qlpqUEoqGvq77Sm9VwrNXA=s900-c-k-c0x00ffffff-no-rj', page_title='Reclame aqui - Alelo')
st.markdown(style(), unsafe_allow_html=True)

st.markdown("<h1 style='text-align: left; font-size:52px; color: white'>ReclameAqui - Alelo</h1>", unsafe_allow_html=True)
st.markdown("""<p style='text-align: left; font-size:16px'>No Brasil, quando consumidores enfrentam problemas com empresas, frequentemente recorrem ao ReclameAqui para registrar suas reclamações. Esta aplicação permite explorar os tópicos mais reclamados sobre a Alelo, fornecendo acesso a dados detalhados, incluindo o teor das reclamações, status e links diretos para cada registro no <a href='https://www.reclameaqui.com.br/empresa/alelo/lista-reclamacoes/' target='_blank'>ReclameAqui - Alelo</a>.</p>""", unsafe_allow_html=True)
topics_tab = st.tabs(["Tópicos com mais reclamações", "Reclamações"])
n_pages = 100

with st.spinner(f'Extraindo dados de {n_pages} reclamações do ReclameAqui - Alelo. Isso pode levar alguns minutos...'):
    df = web_scrapping(range_pag=n_pages)

    with topics_tab[0]:
        st.write('')
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Quantidade de reclamações", f"{len(df)}".replace(',', '.'))
        col2.metric("Reclamações não respondidas", f"{len(df[df['Status'] == 'Não respondida']):,}".replace(',', '.'))
        col3.metric("Reclamações respondidas", f"{len(df[df['Status'] == 'Respondida']):,}".replace(',', '.'))
        col4.metric("Reclamações resolvidas", f"{len(df[df['Status'] == 'Resolvido']):,}".replace(',', '.'))

        st.write('')
        st.write('')
        st.write('')

        sentences_normalized = normalize(df, 'Title')
        preprocessed_sentences = [lemanization(sentence) for sentence in sentences_normalized['processed'].to_list()]

        try:
            gram_df = tfidf_processing(preprocessed_sentences, 2)
        
            st.write('')
            st.write('')
            st.write('')

            st.plotly_chart(bar_plot(gram_df, 'rank', 'termo', 'Tópicos mais reclamados Alelo (Relevância TF-IDF)'))

        except ValueError as e:
            st.error('🚨 Não foi possível identificar tópicos de reclamações para esse filtro. Tente outra combinação 🚨')

    with topics_tab[1]:
        df = df[['Title', 'Text', 'Status', 'Link']].rename(columns={'Title': 'Título', 'Text': 'Texto'}).sort_values(by='Status')
        
        with st.form(key='cluster'):
            with st.expander("Faça filtros para encontrar as reclamações", True):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    status = st.multiselect('Filtrar por Status', df.Status.unique(), placeholder='Escolha uma opção de status', label_visibility='visible')
                with col2:
                    title_filter = st.text_input('Filtrar por Título', placeholder='Digite uma palavra-chave no título')
                with col3:
                    text_filter = st.text_input('Filtrar por Texto', placeholder='Digite uma palavra-chave no texto')

            submit_button = st.form_submit_button(label='Filtrar reclamações 🚨')

            if submit_button:
                filtered_df = df.copy()

                if status:
                    filtered_df = filtered_df[filtered_df['Status'].isin(status)]

                if title_filter:
                    filtered_df = filtered_df[filtered_df['Título'].str.contains(title_filter, case=False, na=False)]

                if text_filter:
                    filtered_df = filtered_df[filtered_df['Texto'].str.contains(text_filter, case=False, na=False)]

                st.table(filtered_df)

            st.table(df)
