from PySimpleGUI import PySimpleGUI as sg
import csv
import os
import shutil
# Defino um nome para o diretorio do projeto
diretorio_projeto = os.getcwd()

# Crio um tema baseado nas cores do WhatApp
sg.LOOK_AND_FEEL_TABLE['WhatsApp'] = {
    'BACKGROUND': '#EDEDED',
    'TEXT': '#000000',
    'INPUT': '#FFFFFF',
    'TEXT_INPUT': '#000000',
    'SCROLL': '#FFFFFF',
    'BUTTON': ('#FFFFFF', '#128C7E'),
    'PROGRESS': ('#075E54', '#25D366'),
    'BORDER': 0,
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0
}
# Defino que vou usar o tema que criei
sg.theme('WhatsApp')

# Layout
layout = [
    # Há um botão para anexar a planilha de contatos e um campo de texto no qual o nome do arquivo
    [sg.FileBrowse('Anexar contatos', initial_folder=diretorio_projeto, file_types=[
                   ("CSV Files", "*.csv")]), sg.Input(key='-FILE_CONTATO-', size=(30, 2), disabled=True)],
    # Há um botão para anexar as imagens e um campo de texto no quais os nomes dos arquivos são apresentados
    [sg.FilesBrowse('Anexar Imagens', initial_folder=diretorio_projeto, file_types=[("PNG Files", "*.png"), ("JPEG Files",
                    "*.jpeg *.jpg")]), sg.Input(key='-FILE_IMAGEM-', size=(30, 2), disabled=True)],
    [sg.Button('Confirmar Imagens', visible=False)],
    [sg.Text('Mensagem:')],
    [sg.Multiline(key='mensagem', size=(80, 10)), sg.Button('Enviar mensagem')]
]
# Modal para selecionar imagens
modalImagens=[
    [sg.Text('Selecione as imagens')],
    [sg.FilesBrowse('Selecionar Imagens', initial_folder=diretorio_projeto, file_types=[("PNG Files", "*.png"), ("JPEG Files",
                    "*.jpeg *.jpg")]),sg.Input(key='-FILE_IMAGEM-', size=(30, 2), disabled=True)],
    [sg.Button('Confirmar'),sg.Button('Cancelar')]
]
# Crio uma janela e a nomeio
janela = sg.Window('Envio de mensagens', layout)

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

# Listar todas as imagens no diretório 'imagens'
def salvar_imagens():
    file_list = valores['-FILE_IMAGEM-'].split(';')
    print(file_list)
    campanhas_dir = os.path.join(os.getcwd(), 'imagens_campanhas')
    # Crie o diretório se ele ainda não existir
    directory = os.path.join(campanhas_dir, 'imagens')
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Copie cada imagem selecionada para o diretório de imagens
    for file_path in file_list:
        file_name = os.path.basename(file_path)
        shutil.copy(file_path, os.path.join(directory, file_name))
        sg.popup('As imagens foram salvas em {}'.format(directory))




while True:
    eventos, valores = janela.read()
    if eventos == sg.WINDOW_CLOSED:
        break

    elif eventos == "Enviar mensagem":
        csv_address = valores["-FILE_CONTATO-"]
        acessar_contatos(csv_address)
        imagens = valores['-FILE_IMAGEM-'].split(';');
        salvar_imagens()
        print(contatos)
