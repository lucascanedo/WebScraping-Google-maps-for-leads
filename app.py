from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd


Loja = input("Escreva o nome do estabelecimento: ")
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

for i in range(2,len(str(soup).split('hfpxzc')) -1):
    lista.append(str(soup).split('hfpxzc')[i].split('href="')[1].split('" ')[0])

################################ Pegando os Post's

driver = webdriver.Firefox()

nome_unidade = []
nota = []
loja = []
avaliacoes = []
localizacao = []
site = []
telefone = []
    
for i in range(0,len(lista[:Numero_Lojas])):
    
    driver.get(lista[i])
    time.sleep(4)

    # Pegando a flag presente nos posts 

    soup = BeautifulSoup(driver.page_source, 'lxml')
    
    # Alocando o conteudo em memória por meio de lista para otimizar 

    try:
        nome_unidade.append(str(soup).split('<title>')[1].split('</title>')[0])
    except:
        nome_unidade.append(' ')
           
    try:
        nota.append(str(soup).split('class="F7nice"')[1].split('</span>')[0].rsplit('>')[-1])
    except:
        nota.append(' ')
            
    try:
        loja.append(str(soup).split('class="DkEaL"')[1].split('</button>')[0].rsplit('>')[-1])
    except:
        loja.append(' ')
        
        
    try:
        avaliacoes.append(str(soup).split('class="rFrJzc UpDOYb"></span></span>')[1].split(' avaliações')[0].split('label="')[1])
    except:
        avaliacoes.append(' ')

    try:
        localizacao.append(str(soup).split('Io6YTe fontBodyMedium kR99db')[1].split('</div>')[0].split('">')[1])
    except:
        localizacao.append(' ')
        
    # Verificando o site
    site_value = 'No Link'
    for index in range(2, 8):
        try:
            site_value = str(soup).split('Io6YTe fontBodyMedium kR99db')[index].split('</div>')[0].split('">')[1]
            if ".com" in site_value:
                break  # Interrompe o loop se encontrar um link válido
        except:
            pass
    site.append(site_value if ".com" in site_value else 'No Link')

    # Verificando o telefone
    telefone_value = 'No Phone'
    for index in range(2, 7):
        try:
            telefone_value = str(soup).split('Io6YTe fontBodyMedium kR99db')[index].split('</div>')[0].split('">')[1]
            if any(char.isdigit() for char in telefone_value):
                break  # Interrompe o loop se encontrar um número de telefone válido
        except Exception as e:
                print(e)
    telefone.append(telefone_value)
        
driver.quit()

# Estruturando um Dataframe

df = pd.DataFrame (lista ,columns=['Url'])
df['nome_unidade'] = nome_unidade
df['nota'] = nota
df['loja'] = loja
df['avaliacoes'] = avaliacoes
df['localizacao'] = localizacao
df['site'] = site
df['telefone'] = telefone

print(df)