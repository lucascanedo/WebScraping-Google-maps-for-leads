from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# Função para obter informações da loja
def get_store_info(url):
    driver.get(url)
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'section-hero-header-title')))

    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Pegando o nome da loja
    Nome_loja = soup.find("h1", class_="DUwDvf lfPIob").text if soup.find("h1", class_="DUwDvf lfPIob") else ' '
    # Pegando a nota da loja
    nota_valor = soup.find("span", class_="MW4etd").text if soup.find("span", class_="MW4etd") else ' '
    # Pegando as avaliações da loja
    avaliacoes_valor = soup.find("span", class_="UY7F9").text if soup.find("span", class_="UY7F9") else ' '

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

    return [url, Nome_loja, nota_valor, avaliacoes_valor, site_value, telefone_value]

# Solicitando informações ao usuário
Loja = str(input("Escreva o nome do estabelecimento: "))
Numero_Lojas = int(input("Escreva a quantidade de lojas pesquisadas: "))

# Iniciando o webdriver
driver = webdriver.Firefox()
driver.get('https://www.google.com.br/maps')

# Pesquisando a loja
search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'searchboxinput')))
search_box.send_keys(Loja)
time.sleep(2)  # Aguardando um pouco antes de submeter a pesquisa
select = driver.find_element(By.XPATH,'//*[@id="searchbox-searchbutton"]').click();

# Coletando os URLs das lojas
urls_set = set()
while len(urls_set) < Numero_Lojas:
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for tag in soup.find_all("a", href=True):
        if "/place/" in tag['href']:
            urls_set.add(tag['href'])
            if len(urls_set) >= Numero_Lojas:
                break
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

print(len(urls_set))
# Coletando as informações das lojas
data = []
for url in list(urls_set):
    data.append(get_store_info(url))

# Fechando o webdriver
driver.quit()

# Criando o DataFrame
df = pd.DataFrame(data, columns=['Url', 'Nome_loja', 'nota', 'avaliacoes', 'site', 'telefone'])

print(df)
df.info()
