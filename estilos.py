from PySimpleGUI import PySimpleGUI as sg
import os
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
diretorio_projeto = os.getcwd()
sg.theme('WhatsApp')
# Crio o layout da janela principal
layout = [
    # Usamos o nome da campanha para criar um diretorio de imagens para a campanha
    [sg.Text('Nome da campanha'), sg.InputText(key='-NOME_CAMPANHA-',enable_events=True),sg.Button('Confirmar',key='-CONFIRMAR_CAMPANHA-')],
    # Há um botão para anexar a planilha de contatos e um campo de texto no qual o nome do arquivo
    [sg.FileBrowse('Anexar contatos', initial_folder=diretorio_projeto, file_types=[
                   ("CSV Files", "*.csv")],key='-ANEXAR_CONTATOS-',disabled=True), sg.InputText(key='-FILE_CONTATO-', size=(30, 2), disabled=True,enable_events=True)],
    # Há um botão para anexar as imagens e um campo de texto no quais os nomes dos arquivos são apresentados
    [sg.Button('Anexar Imagens',disabled=True,key='-ANEXAR_IMAGEM-')],
    [sg.Text('Mensagem:')],
    [sg.Multiline(key='-MENSAGEM-', size=(80, 10),disabled=True),
     sg.Button('Enviar mensagem',disabled=True,key='-ENVIAR_MENSAGEM-')]
]
# # Crio uma janela e a nomeio
# janela = sg.Window('Envio de mensagens', layout, finalize=True)