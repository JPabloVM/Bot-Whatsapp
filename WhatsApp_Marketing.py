from PySimpleGUI import PySimpleGUI as sg
import shutil
import csv
import os
import time
import pyautogui
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import estilos
# Defino um nome para o diretorio do projeto
diretorio_projeto = os.getcwd()
# Crio a janela e tema de acordo com o que foi criado na pasta estilos
janela = sg.Window('WhatsApp Marketing - By PVMtech',
                   estilos.layout, finalize=True)
estilos.sg.theme('WhatsApp')


def criar_modal():
    # Modal para selecionar imagens
    modalImagens = [
        [sg.Text('Selecione as imagens')],
        [sg.FilesBrowse('Selecionar Imagens', initial_folder=diretorio_projeto, file_types=[("PNG Files", "*.png"), ("JPEG Files",
                        "*.jpeg *.jpg")]), sg.Input(key='-FILE_IMAGEM-', size=(30, 2), disabled=True)],
        [sg.Button('Confirmar'), sg.Button('Fechar Modal')]
    ]
    janela_modal = sg.Window('Modal', modalImagens, modal=True)
    # loop da janela modal
    while True:
        evento_modal, valores_modal = janela_modal.read()
        if evento_modal == 'Confirmar':
            salvar_imagens(valores_modal)
            janela_modal.close()

        if evento_modal == sg.WIN_CLOSED or evento_modal == 'Fechar Modal':
            # fecha a janela modal
            janela_modal.close()
            break

# Inicio da função para preencher os contatos


# Esse array se trata do array com os contatos da planilha selecionada
contatos = []
# Essa função percorre toda a planilha e preenche o array de contatos com todos contatos da planilha


def acessar_contatos(csv_address):
    file = open(csv_address)
    csv_reader = csv.reader(file)
    header = next(csv_reader)
    for row in csv_reader:
        contatos.append(row[0])
        # print(contatos)
    file.close()
    return contatos
# Fim da função para preencher os contatos


def salvar_imagens(valores_modal):
    file_list = valores_modal['-FILE_IMAGEM-'].split(';')
    campanhas_dir = os.path.join(os.getcwd(), 'imagens_campanhas')
    # Crie o diretório com o nome da campanha
    directory = os.path.join(campanhas_dir, nome_campanha)
    # Caso não exista nenhuma pasta com o mesmo nome da campanha será criado um novo diretorio e as imagens serão incluídas no mesmo
    if not os.path.exists(directory):
        os.makedirs(directory)
        # Estou copiando todas imagens selecionadas para dentro do diretorio
        for file_path in file_list:
            file_name = os.path.basename(file_path)
            shutil.copy(file_path, os.path.join(directory, file_name))
            sg.popup('Imagens salvas com sucesso')
    else:
        sg.popup('Já há uma campanha com este nome. Altere o nome da campanha')


def buscar_contato(contato):
    try:
        campo_pesquisa = driver.find_element(
            "xpath", '//p[contains(@class,"selectable-text copyable-text")]')
        time.sleep(3)
        campo_pesquisa.click()
        campo_pesquisa.send_keys(contato)
        time.sleep(3)
        try:
            # Procura o elemento que contém o texto "Nenhuma conversa, contato ou mensagem encontrada"
            no_results = driver.find_element(
                "xpath", '//span[contains(text(),"Nenhuma conversa, contato ou mensagem encontrada")]')
            print('Contato não encontrado')
            if no_results:
                campo_pesquisa.send_keys(Keys.ESCAPE)
                return False
        except NoSuchElementException:
            print('Cai no Except')
            campo_pesquisa.send_keys(Keys.ENTER)
            print('Cliquei no enter')
            time.sleep(1)
            return True
    except:
        print('Não encontrei o campo de pesquisa')
        #  Dou um tempo antes de tentar encontrar o campo de pesquisa dnv
        time.sleep(30)
        # E depois inicio a busa pelo contato
        buscar_contato(contato)


def enviar_mensagem(mensagem):
    print('Entrei na função para enviar a mensagem')
    campo_mensagem = driver.find_elements(
        "xpath", '//p[contains(@class,"selectable-text copyable-text")]')
    print('Encontrei o campo para enviar mensagem')
    campo_mensagem[1].click()
    time.sleep(3)
    campo_mensagem[1].send_keys(mensagem)
    print('Era pra digitar a mensagem')
    time.sleep(3)
    campo_mensagem[1].send_keys(Keys.ENTER)
    print('Enviei a mensagem dentro da função enviar mensagem')
    time.sleep(5)


def enviar_imagem(imagem):
    campo_mensagem = driver.find_element(
        "xpath", '//p[contains(@class,"selectable-text copyable-text")]')
    campo_mensagem.click()
    time.sleep(3)
    # Clicar no botão "Anexar"
    anexar_button = driver.find_element(By.XPATH, '//div[@title="Anexar"]')
    anexar_button.click()
    time.sleep(2)
    # Selecionar a opção "Imagem"
    imagem_button = driver.find_element(
        By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
    imagem_button.send_keys(os.path.abspath(imagem))
    pyautogui.write('\n')
    # Esperar o upload da imagem ser concluído
    time.sleep(10)
    # Clicar no botão "Enviar"
    enviar_button = driver.find_element(By.XPATH, '//span[@data-icon="send"]')
    enviar_button.click()
    time.sleep(3)


while True:
    eventos, valores = janela.read()
    # Pego o nome da campanha para criar um diretorio novo com ele
    if eventos == sg.WINDOW_CLOSED:
        break
    # Quando a pessoa clicar no OK para confirmar nome da campanha
    elif eventos == '-CONFIRMAR_CAMPANHA-':
        nome_campanha = valores['-NOME_CAMPANHA-']
        # Se estiver vazio peço para digitar um nome
        if not nome_campanha:
            sg.popup('Digite um nome para a campanha')
        else:
            diretorio_imagens = os.path.join(os.getcwd(), 'imagens_campanhas')
            # Crie o diretório com o nome da campanha
            diretorio_campanha = os.path.join(diretorio_imagens, nome_campanha)
            if not os.path.exists(diretorio_campanha):
                janela['-ANEXAR_IMAGEM-'].update(
                    disabled=not valores['-NOME_CAMPANHA-'])
                janela['-ANEXAR_CONTATOS-'].update(
                    disabled=not valores['-NOME_CAMPANHA-'])
                janela['-MENSAGEM-'].update(
                    disabled=not valores['-NOME_CAMPANHA-'])
            else:
                sg.popup('Já existe uma campanha com este nome! Tente outro nome')
    elif eventos == "-ANEXAR_IMAGEM-":
        criar_modal()
    elif eventos == "-FILE_CONTATO-":
        janela['-ENVIAR_MENSAGEM-'].update(
            disabled=not valores['-FILE_CONTATO-'])
    elif eventos == "-ENVIAR_MENSAGEM-":
        # Listar todas as imagens no diretório 'da campanha
        # diretorio = 'imagens_campanhas/'
        if os.path.exists(diretorio_campanha):
            imagens = [os.path.join(diretorio_campanha, f) for f in os.listdir(
                diretorio_campanha) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
            
        csv_address = valores["-FILE_CONTATO-"]
        acessar_contatos(csv_address)
        mensagem1 = valores["-MENSAGEM-"]
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get('https://web.whatsapp.com/')
        time.sleep(3)
        # Percorro toda a planilha de contato a contato
        for contato in contatos:
            #    Chamo a função enquanto passo uma condição, se ela retornar true é pq encontrou o contato
            if buscar_contato(contato) == True:
                print('A função de buscar contato retornou true')
                # Verifico se existe alguma mensagem de texto a ser enviada
                if len(mensagem1) != 0:
                    # Se existir chamo a função para enviar mensagem passando essa mensagem
                    print('Vou chamar a função para mandar mensagem')
                    enviar_mensagem(mensagem1)
                    print('Deveria ter enviado a mensagem')
                # Verifico se existe o array de imagens
                if 'imagens' in locals() or 'imagens' in globals():
                    # Se existir percorro as imagens
                    for imagem in imagens:
                        # E em seguida chamo a função para enviar imagem passando a imagem atual que estou percorrendo
                        enviar_imagem(imagem)
            #  Caso a função buscar contato retornar False é pq não existia aquele contato, então espero um tempo antes de procurar pelo próximo contato, para evitar travamento
            else:
                time.sleep(5)
        driver.close()
        sg.popup('Campanha finalizada')
