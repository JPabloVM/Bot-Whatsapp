import csv
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://web.whatsapp.com/')
time.sleep(30)
contatos = []
with open('contatos.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        contatos.append(row[0])
mensagem = 'Boa tarde'

def buscar_contato(contato):
    campo_pesquisa = driver.find_element("xpath",'//p[contains(@class,"selectable-text copyable-text")]')
    time.sleep(3)
    campo_pesquisa.click()
    campo_pesquisa.send_keys(contato)
    campo_pesquisa.send_keys(Keys.ENTER)

    
def enviar_mensagem(mensagem):
       campo_mensagem = driver.find_elements("xpath",'//p[contains(@class,"selectable-text copyable-text")]')
       campo_mensagem[1].click()
       time.sleep(3)
       campo_mensagem[1].send_keys(mensagem)
       time.sleep(3)
       campo_mensagem[1].send_keys(Keys.ENTER)
       time.sleep(5)
       
for contato in contatos:
    buscar_contato(contato)
    enviar_mensagem(mensagem)

