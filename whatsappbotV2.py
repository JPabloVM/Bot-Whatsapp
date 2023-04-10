import csv
import os
import time
import pyautogui
from selenium import webdriver
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
imagens = ['imagem1.png', 'imagem2.png', 'imagem3.png']

def buscar_contato(contato):
    campo_pesquisa = driver.find_element("xpath",'//p[contains(@class,"selectable-text copyable-text")]')
    time.sleep(3)
    campo_pesquisa.click()
    campo_pesquisa.send_keys(contato)
    campo_pesquisa.send_keys(Keys.ENTER)

    
def enviar_mensagem(imagens, indice):
    campo_mensagem = driver.find_element("xpath",'//p[contains(@class,"selectable-text copyable-text")]')
    campo_mensagem.click()
    time.sleep(3)
    # Clicar no botão "Anexar"
    anexar_button = driver.find_element("xpath",'//span[contains(@data-icon,"clip")]')
    anexar_button.click()
    time.sleep(2)
    # Selecionar a opção "Imagem"
    imagem_button = driver.find_element("xpath",'//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
    imagem_button.send_keys(os.path.abspath(imagens[indice]))
    pyautogui.write('\n')
    # Esperar o upload da imagem ser concluído
    time.sleep(10)
    # Clicar no botão "Enviar"
    enviar_button = driver.find_element("xpath",'//span[@data-icon="send"]')
    enviar_button.click()
    time.sleep(3)
    
for contato in contatos:
    buscar_contato(contato)
    for i in range(len(imagens)):
        enviar_mensagem(imagens, i)