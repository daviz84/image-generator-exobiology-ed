import os

import kivy.uix.widget
from kivy.clock import mainthread
from kivy.config import Config

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '200')
Config.set('graphics', 'resizable', False)

import requests
import pyscreenshot
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from kivy.core.window import Window
import json
from threading import Thread
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import datetime
from playsound import playsound
from os import path
import tkinter as tk
from pynput.keyboard import Key, Listener

# INSTANCIAÇÃO DOS ELEMENTOS GRÁFICOS

Window.clearcolor = "white"

layoutMain = BoxLayout()
layoutMain.orientation = "vertical"
layoutMain.padding = (50, 50, 50, 50)
layoutMain.minimum_height = 600

txtInputJournal = TextInput()
txtInputJournal.id = "idTxtInput"

buttonGerar = Button()

layoutForm = BoxLayout()
layoutForm.width = 700
layoutForm.height = 100
layoutForm.size_hint = (None, None)

layoutImage = BoxLayout()
layoutImage.width = 700
layoutImage.height = 400
layoutImage.size_hint = (None, None)
layoutImage.orientation = "vertical"

imageEdit = AsyncImage()
imageEdit.size_hint = (None, None)
imageEdit.width = 700
imageEdit.height = 350
imageEdit.padding = (0, 0, 0, 0)
imageEdit.fit_mode = "fill"

layoutBottom = BoxLayout()
layoutBottom.spacing = 400
layoutBottom.size_hint = (None, None)
layoutBottom.width = 700
layoutBottom.height = 50

layoutBottomOptions = BoxLayout()
layoutBottomOptions.size_hint = (None, None)

txtInputCoord = TextInput()
txtInputCoord.disabled = True
txtInputCoord.size_hint = (0, 0)
txtInputCoord.width = 100
txtInputCoord.height = 50

#RETORNA O DIRETORIO DO USUARIO E COMPLEMENTA COM A PASTA DE REGISTROS DO PROGRAMA
pathOrigin = path.join(path.expanduser("~"), "Documents/image-generator-exobiology-ed").replace("\\", "/")
pathED = path.join(path.expanduser("~"), "Saved Games/Frontier Developments/Elite Dangerous").replace("\\", "/")


class MeuAplicativo(App):

    def build(self):
        self.title = "Image Generation Exobiology ED"

        buttonGerar = ButtonGerar()

        buttonReload = ButtonReload()

        buttonSalvar = ButtonSalvar()

        layoutBottomOptions.add_widget(buttonReload)
        layoutBottomOptions.add_widget(buttonSalvar)

        layoutBottom.add_widget(txtInputCoord)
        layoutBottom.add_widget(layoutBottomOptions)

        layoutImage.add_widget(imageEdit)
        layoutImage.add_widget(layoutBottom)

        layoutForm.add_widget(txtInputJournal)
        layoutForm.add_widget(buttonGerar)

        layoutMain.add_widget(layoutForm)

        layoutMain.add_widget(UpdatePos())  # BoxLayout adicionado para manter a posição do mouse atualizada

        return layoutMain

    def on_start(self):
        print("INICIANDO PROGRAMA")
        createObserverKeyboard()

        #INSTANCIA E INICIA O WATCHDOG EM OUTRA THREAD (RESPONSAVEL POR MONITORAR OS REGISTROS DO JOGO - PASTAS E ARQUIVOS)
        trhed = Thread(target=createWatchdog)
        trhed.start()

        #CRIA OS ARQUIVOS DE REGISTRO PARA ARMANEZAR AS ESPÉCIES ANALISADAS
        try:
            os.mkdir(f'{pathOrigin}')
            os.mkdir(f'{pathOrigin}/gallery')

            criarAqv = open(f'{pathOrigin}/registro.json', 'w')
            criarAqv.write('{"especiesCatalogadas": {}}')
            criarAqv.close()


        except FileExistsError:
            print("ARQUIVO JÁ CRIADO")

@mainthread
def gerarImagem():
    Window.size = (800, 600)
    try:
        layoutMain.add_widget(layoutImage)
    except kivy.uix.widget.WidgetException:
        print("Widget já adicionado")

    value_txtinputJournal = json.loads(txtInputJournal.text)

    #REQUISIÇÃO NOME DO SISTEMA PELO CODIGO DO JOURNAL (RETORNA UM JSON STRING)
    requisitionNameSystem = requests.get(
        f"https://www.edsm.net/typeahead/systems/query/{value_txtinputJournal['SystemAddress']}")
    resultRequisitionNameSystem = requisitionNameSystem.json()[0]["value"]

    #CAPTURA O MONITOR PRINCIPAL E SALVA COMO ARQUIVO "TEMPORARIO"
    imagePrint = pyscreenshot.grab()
    imagePrint.save(f'{pathOrigin}/gallery/imgTemp.png')

    imageEdit.source = 'gallery/imgTemp.png'
    imageEdit.reload()

    #PREENCHE IMAGEM COM AS INFORMAÇÕES
    printscreen = Image.open(f'{pathOrigin}/gallery/imgTemp.png')
    mold = Image.open('gallery/imagemMolde.png')
    mold_draw = ImageDraw.Draw(mold)
    mold_font = ImageFont.truetype('fonts/TechnoBoard.ttf', 26)
    mold_fontSmall = ImageFont.truetype('fonts/Glitch inside.otf', 12)
    mold_draw.text((258, 53),
                   f"{value_txtinputJournal['Species_Localised']}\n {value_txtinputJournal['Variant_Localised'].split('- ')[1]} ",
                   font=mold_font)
    mold_draw.text((360, 115), f"{resultRequisitionNameSystem}", font=mold_fontSmall)

    mold.save(f'{pathOrigin}/gallery/imagemMoldeEscrito.png')

    colarMolde(printscreen, mold, (0, 0))


def colarMolde(printscreen, mold, positions):
    printscreen.paste(mold, positions, mask=mold)
    printscreen.save(f'{pathOrigin}/gallery/imagemMesclada.png')

    imageEdit.source = f'{pathOrigin}/gallery/imagemMesclada.png'
    imageEdit.reload()


def atualizaPosicoes(tuple):
    #FUNÇÃO UTILITÁRIA PARA TRANSFORMAR EM INTEIRO (PARA O CLICK E PARA O CÁLCULO DE PROPORÇÃO)
    valX = int(tuple[0])
    valY = int(tuple[1])

    return (valX, valY)


class UpdatePos(BoxLayout):
    def __init__(self, **kwargs):
        super(UpdatePos, self).__init__(**kwargs)
        self.size = (0, 0)
        self.size_hint = (None, None)

    def on_touch_down(self, touch):
        root = tk.Tk()

        x = int(touch.pos[0])
        y = int(touch.pos[1])

        try:
            imgTemp = Image.open(f'{pathOrigin}/gallery/imgTemp.png')
            mold = Image.open(f'{pathOrigin}/gallery/imagemMoldeEscrito.png')

            if (x >= 50 and x <= 750) and (y >= 100 and y <= 450):
                resolX = root.winfo_screenwidth()
                resolY = root.winfo_screenheight()

                proporcaoX = (resolX * 1.18) / 800
                proporcaoY = (resolY * 1.6) / 600

                x = int(((x - 50) * proporcaoX) - 220)
                y = int(-((y - 450) * proporcaoY) - 185)

                txtInputCoord.text = f"{x, y}"
                colarMolde(imgTemp, mold, (x, y))

        except FileNotFoundError:
            print("Aguardando algum registro do journal")


class ButtonGerar(Button):

    def __init__(self):
        super(ButtonGerar, self).__init__()
        self.text = "GERAR IMAGEM"
        self.background_color = "#282828"
        self.size_hint = (None, None)
        self.width = 250

    def on_press(self):
        gerarImagem()


class ButtonSalvar(Button):

    def __init__(self):
        super(ButtonSalvar, self).__init__()
        self.size_hint = (None, None)
        self.height = 50
        self.background_color = "green"
        self.text = "SALVAR"

    def on_press(self):
        registrarDescoberta()


class ButtonReload(Button):
    def __init__(self):
        super(ButtonReload, self).__init__()
        self.size_hint = (None, None)
        self.height = 50
        self.background_color = "red"
        self.text = "RELOAD"

    def on_press(self):
        reloadWidgets()


def createWatchdog():
    observer = Observer()

    @mainthread
    def on_modified(event):
        print(event)
        testeComJournal(event.src_path)

    try:
        event_handler = FileSystemEventHandler()
        event_handler.on_modified = on_modified

        path = "C:/Users/davio/Desktop/fileMod"

        #observer.schedule(event_handler, pathED, recursive=True)
        observer.schedule(event_handler, path, recursive=True)
        observer.start()

        print("Monitorando")
        while not Window:
            time.sleep(1)
    except (FileNotFoundError, Exception):
        print("Pasta de monitoramento não encontrada")
        observer.stop()
    exit()


def testeComJournal(file_modified):
    dateNow = datetime.date.today()
    file_modified = file_modified.replace('\\', '/')

    if f"Journal.{dateNow}" in file_modified:

        archive = open(file_modified, "r", errors='replace')
        archiveRead = archive.readlines()
        arquivoJournalLog = json.loads(archiveRead[len(archiveRead) - 1])

        if arquivoJournalLog['event'] == 'ScanOrganic':
            txtInputJournal.text = json.dumps(arquivoJournalLog)
            playsound('fonts/system-notification-199277.mp3')


def registrarDescoberta():
    registryJournal = json.loads(txtInputJournal.text)
    specie = registryJournal['Variant_Localised']

    registryDaily = open(f'{pathOrigin}/registro.json', 'r')
    registryDailyJSON = json.loads(registryDaily.read())

    if specie not in registryDailyJSON['especiesCatalogadas']:
        registryDailyJSON['especiesCatalogadas'].__setitem__(specie, {"registro": registryJournal})
        registryDaily.close()

        registryDayly = open(f'{pathOrigin}/registro.json', 'w')
        registryDayly.write(json.dumps(registryDailyJSON))
        registryDayly.close()
        print("ESPÉCIE REGISTRADA COM SUCESSO!")
        reloadWidgets()

    else:
        print("ESPÉCIE JÁ REGISTRADA!")
        reloadWidgets()


def reloadWidgets():
    Window.size = (800, 200)
    layoutMain.remove_widget(layoutImage)
    txtInputJournal.text = ""



def createObserverKeyboard():

    def on_presskeyboard(key):
        if key == Key.f2:
            print("TESTEEEEEEE")
            gerarImagem()

    listener = Listener(on_press=on_presskeyboard)
    listener.start()



if __name__ == "__main__":
    myApp = MeuAplicativo()
    myApp.run()
