from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# Função para obter informações da loja
def get_store_info(url):
    driver.get(url)
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'section-hero-header-title')))

    soup = BeautifulSoup(driver.page_source, 'lxml')

    try:
        # Pegando o nome da loja
        Nome_loja = soup.find("h1", class_="DUwDvf lfPIob").text.strip()
    except AttributeError:
        Nome_loja = 'Nome não encontrado'

    try:
        # Pegando a nota da loja
        nota_element = driver.find_element(By.CSS_SELECTOR, '.F7nice > span:nth-child(1) > span:nth-child(1)')
        nota_valor = nota_element.text.strip()
        nota_numero = float(nota_valor.replace(',', '.'))
    except (NoSuchElementException, ValueError):
        nota_numero = None

    try:
        # Pegando as avaliações da loja
        avaliacoes_element = driver.find_element(By.XPATH, '//span[contains(@aria-label, "avaliações")]')
        avaliacoes_valor = avaliacoes_element.text.strip()
        avaliacoes_valor = int(avaliacoes_valor.replace('(', '').replace(')', ''))
    except (NoSuchElementException, ValueError):
        avaliacoes_valor = None

    # Verificando o site
    site_value = 'No Link'
    for tag in soup.find_all("a", href=True):
        aria_label = tag.get('aria-label', '')
        if aria_label and 'Website:' in aria_label:
            site_value = tag['href']
            break

    # Verificando o telefone
    telefone_value = 'No Phone'
    for tag in soup.find_all("div", class_="Io6YTe fontBodyMedium kR99db"):
        telefone_match = re.search(r'(\(?\d{2}\)?\s?)?(\d{4,5}-\d{4})', tag.text)
        if telefone_match:
            telefone_value = telefone_match.group()
            break

    return [url, Nome_loja, nota_numero, avaliacoes_valor, site_value, telefone_value]


# Solicitando informações ao usuário
Pesquisa = str(input("O que deseas pesquisar? "))
qtdPesquisa = int(input("Coloque a quantidade a ser pesquisado: "))

# Iniciando o webdriver
driver = webdriver.Firefox()
driver.get('https://www.google.com.br/maps')

# Pesquisando a loja
search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'searchboxinput')))
search_box.send_keys(Pesquisa)
time.sleep(2)  # Aguardando um pouco antes de submeter a pesquisa
select = driver.find_element(By.XPATH,'//*[@id="searchbox-searchbutton"]').click();

# Coletando os URLs das lojas
urls_set = set()
time.sleep(2)

scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')  #Encontrado a parte onde deve acontecer o scrol dentro da pagina do maps
while len(urls_set) < qtdPesquisa:
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for tag in soup.find_all("a", class_="hfpxzc", href=True):
        if "/place/" in tag['href']:
            urls_set.add(tag['href'])
            if len(urls_set) >= qtdPesquisa:
                break

    # Rolando a página na região role="feed" para carregar mais lojas
    driver.execute_script("arguments[0].scrollBy(0, 200);", scrollable_div)
    time.sleep(2)

print(len(urls_set))

# Coletando as informações das lojas
data = []
for url in list(urls_set):
    data.append(get_store_info(url))

# Fechando o webdriver
driver.quit()

# Criando o DataFrame
df = pd.DataFrame(data, columns=['Url', 'Nome', 'nota', 'avaliacoes', 'site', 'telefone'])

# Exportando o DataFrame para um arquivo Excel
excel_file = 'leads.xlsx'  # Nome do arquivo Excel
df.to_excel(excel_file, index=False)

print("Dados exportados para:", excel_file)

print(df)
df.info()