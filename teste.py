from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re

def get_store_info(driver, url):
    driver.get(url)
    time.sleep(8)

    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Get store info
    Nome_loja = soup.find("h1", class_="DUwDvf lfPIob").text if soup.find("h1", class_="DUwDvf lfPIob") else ' '
    nota_valor = soup.find("span", class_="MW4etd").text if soup.find("span", class_="MW4etd") else ' '
    avaliacoes_valor = soup.find("span", class_="UY7F9").text if soup.find("span", class_="UY7F9") else ' '

    # Get site
    site_value = 'No Link'
    for tag in soup.find_all("a", href=True):
        aria_label = tag.get('aria-label', '')
        if aria_label and 'Website:' in aria_label:
            site_value = tag['href']
            break

    # Get phone
    telefone_value = 'No Phone'
    for tag in soup.find_all("div", class_="Io6YTe fontBodyMedium kR99db"):
        telefone_match = re.search(r'(\\(?\\d{2}\\)?\\s?)?(\\d{4,5}-\\d{4})', tag.text)
        if telefone_match:
            telefone_value = telefone_match.group()
            break

    return [url, Nome_loja, nota_valor, avaliacoes_valor, site_value, telefone_value]

def main():
    Loja = input("Escreva o nome do estabelecimento: ")
    Numero_Lojas = int(input("Escreva a quantidade de lojas pesquisadas: "))

    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 10)

    driver.get('https://www.google.com.br/maps')
    time.sleep(6)

    search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'searchboxinput')))
    search_box.send_keys(Loja)
    time.sleep(5)

    search_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'searchbox-searchbutton')))
    search_button.click()
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Find store links
    urls_set = set()

    while len(urls_set) < Numero_Lojas:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        for tag in soup.find_all("a", href=True):
            if "/place/" in tag['href']:
                urls_set.add(tag['href'])
                # Scroll the screen
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                if len(urls_set) >= Numero_Lojas:
                    break

    lista = list(urls_set)

    # Get store info
    store_info = [get_store_info(driver, url) for url in lista]

    driver.quit()

    # Create DataFrame
    df = pd.DataFrame(store_info, columns=['Url', 'Nome', 'nota', 'avaliacoes', 'site', 'telefone'])

    print(df)

if __name__ == "__main__":
    main()
