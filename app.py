from lxml import html
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd

Loja = str(input("Escreva o nome do estabelecimento: "))
Numero_Lojas = int(input("Escreva a quantidade de lojas pesquisadas: "))

driver = webdriver.Firefox()

driver.get('https://www.google.com.br/maps')
time.sleep(4)

select = driver.find_element(By.XPATH,'//*[@id="searchboxinput"]')  # Colocando o acesso de login
select.send_keys(Loja)
time.sleep(1)

select = driver.find_element(By.XPATH,'//*[@id="searchbox-searchbutton"]').click();
time.sleep(4)

soup = BeautifulSoup(driver.page_source, 'lxml')

lista = []

# Encontrando os links dos estabelecimentos

for tag in soup.find_all("a", href=True):
    if "/place/" in tag['href']:
        lista.append(tag['href'])
        if len(lista) == Numero_Lojas:
            break
    

################################ Pegando os Post's

Nome = []
nota = []
#loja = []
avaliacoes = []
site = []
telefone = []

for i, url in enumerate(lista):

    driver.get(url)
    time.sleep(6)

    # Pegando a flag presente nos posts

    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Alocando o conteudo em memória por meio de lista para otimizar

    # Pegando o título do estabelecimento
    Nome_loja = soup.find("h1", class_="DUwDvf lfPIob").text if soup.find("h1", class_="DUwDvf lfPIob") else ' '
    Nome.append(Nome_loja)

    # Pegando a nota do estabelecimento
    nota_valor = soup.find("span", class_="MW4etd").text if soup.find("span", class_="MW4etd") else ' '
    nota.append(nota_valor)

    # Pegando o nome do estabelecimentoF
    #loja_tipo = soup.find("button", class_="DkEaL ").text if soup.find("button", class_="DkEaL ") else ' '
    #loja.append(loja_tipo)

    # Pegando as avaliações
    avaliacoes_valor = soup.find("span", class_="UY7F9").text if soup.find("span", class_="UY7F9") else ' '
    avaliacoes.append(avaliacoes_valor)

    # Verificando o site
    site_value = 'No Link'
    for tag in soup.find_all("a", href=True):
        aria_label = tag.get('aria-label', '')
        if aria_label and 'Website:' in aria_label:
            site_value = tag['href']
            break
    site.append(site_value)


    # Verificando o telefone
    telefone_value = 'No Phone'
    for tag in soup.find_all("div", class_="Io6YTe fontBodyMedium kR99db"):
        telefone_match = re.search(r'(\(?\d{2}\)?\s?)?(\d{4,5}-\d{4})', tag.text)
        if telefone_match:
            telefone_value = telefone_match.group()
            break
    telefone.append(telefone_value)


driver.quit()

# Estruturando um Dataframe

df = pd.DataFrame(lista, columns=['Url'])
df['Nome_loja'] = Nome
df['nota'] = nota
#df['loja_tipo'] = loja
df['avaliacoes'] = avaliacoes
df['site'] = site
df['telefone'] = telefone

print(df)
df.info()
# Salvando o DataFrame em um arquivo CSV
#df.to_csv('dados_estabelecimentos.csv', index=False)

#print("Os dados foram salvos em dados_estabelecimentos.csv")

