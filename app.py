from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd


search = input("O que desejas encontar: ")
num_linhas_desejado = int(input("Quantidade de linhas desejadas: "))

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.google.com.br/maps")

dados_titles = []

def remove_dup(lista):
    lista = set(lista)
    return lista

def search_place():
    # Utilizando By.CLASS_NAME para encontrar o elemento pela classe
    place = driver.find_element(By.CLASS_NAME, "searchboxinput")
    place.send_keys(search)
    submit = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[8]/div[3]/div[1]/div[1]/div/div[2]/div[1]/button/span")
    submit.click()

# Adicionando um tempo de espera para que a página tenha tempo de carregar completamente
sleep(5)

search_place()

sleep(2)

scroll = driver.find_element(By.CSS_SELECTOR,".Nv2PK")

try:
    scroll.execute_script("window.scrollTo(0,document.body.scrollHeight)")
except:
    pass

sleep(3)

links = driver.find_elements(By.CSS_SELECTOR,".Nv2PK") 

for link in links:
    sleep(2)
    text = link.find_element(By.CSS_SELECTOR,".hfpxzc")
    text_link = text.get_attribute("href")
    dados_titles.append(text_link)

lista = remove_dup(dados_titles)

sleep(5)

dados = []
linhas_coletadas = 0


for dado in lista:
    if linhas_coletadas >= num_linhas_desejado:
        break  # Sai do loop se atingir o número desejado de linhas
    driver.get(dado)
    sleep(3)

    for attribute in driver.find_elements(By.CSS_SELECTOR,".WNBkOb"):
        
        try:
            text = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/h1/span[1]").text
        except:
            text = None

        try:
            review = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[1]/span[1]").text
        except:
            review = None
        
        try:
            count_review = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div[1]/div[2]/span[2]/span/span").text
        except:
            count_review = None
        
        try:
            phone = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div[8]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[9]/div[6]/button/div/div[2]/div[1]").text
        except:
            phone = None
        
        try:
            website = driver.find_element(By.CSS_SELECTOR, ".rllt__link")
            website_link = website.get_attribute("href")
        except:
            website_link = None
        
        dados_final = {
            "Nome": text,
            "Avaliacao": review,
            "Qauantidade de avaliacoes": count_review,
            "Numero": phone,
            "Site": website_link
        }
        dados.append(dados_final)
        linhas_coletadas += 1

driver.close()


df = pd.DataFrame(dados)
df.drop_duplicates(inplace=True)
df.to_csv('leads_googleMaps.csv', index=False)

# Move o arquivo para um local específico, se necessário
# Você pode personalizar o caminho conforme necessário
import shutil
shutil.move('leads_googleMaps.csv', 'C:/Users/Lucas/OneDrive/Documentos/Estudos Lucas/WebScraping/leads_googleMaps.csv')

print(f'O arquivo "leads_googleMaps.csv" foi salvo com sucesso!')