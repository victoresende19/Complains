import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import streamlit as st

@st.cache_data(show_spinner=False, ttl=24*3600, max_entries=10)
def web_scrapping(range_pag) -> pd.DataFrame:
    """
    Faz o web scrapping do reclame aqui

    Recebe:
        df: dataframe com os dados
    Retorna:
        df: dados após o processamento
    """

    # Headers ajustados para o site Reclame Aqui
    headers = {
        "authority": "www.reclameaqui.com.br",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "pt-BR,pt;q=0.9",
        "cache-control": "max-age=0",
        "content-type": "text/html; charset=utf-8",
        "origin": "https://www.reclameaqui.com.br",
        "referer": "https://www.reclameaqui.com.br/",
        "sec-ch-ua": '"Not.A/Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    title_list = []
    text_list = []
    status_list = []
    link_list = []

    # Loop para iterar pelas páginas
    for page in range(1, range_pag):
        time.sleep(1.25)
        url = f'https://www.reclameaqui.com.br/empresa/alelo/lista-reclamacoes/?pagina={page}'
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            html_content = response.content
            soup = BeautifulSoup(html_content, 'html.parser')
            extract_data(soup, title_list, text_list, status_list, link_list)
        else:
            print(f'A solicitação não foi bem-sucedida na página {page}. Código de status:', response.status_code)
    
    data = {
        'Title': title_list,
        'Text': text_list,
        'Status': status_list,
        'Link': link_list
    }
    return pd.DataFrame(data)


# @st.cache_data(show_spinner=False, ttl=24*3600, max_entries=10)
def extract_data(soup, title_list, text_list, status_list, link_list):
    """
    Faz o web scrapping do reclame aqui

    Recebe:
        df: dataframe com os dados
    Retorna:
        df: dados após o processamento
    """

    for item in soup.find_all('div', class_='sc-1pe7b5t-0 eJgBOc'):
        title = item.find('h4').text.strip() if item.find('h4') else ''
        text = item.find('p', class_='sc-1pe7b5t-2 fGresJ').text.strip()  if item.find('p', class_='sc-1pe7b5t-2 fGresJ') else ''
        status_div = item.find('div', class_='sc-1pe7b5t-3 gkhqVK')
        status = status_div.find('span').text.strip() if status_div and status_div.find('span') else ''
        link_div = item.find('div', class_='sc-1pe7b5t-0 eJgBOc')
        link = item.find('a')['href'] if item.find('a') else ''


        title_list.append(title)
        text_list.append(text)
        status_list.append(status)
        link_list.append(f"https://www.reclameaqui.com.br{link}")
