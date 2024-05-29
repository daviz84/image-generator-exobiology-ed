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
import ctypes

class ButtonGerar(Button):

    def __init__(self):
        super(ButtonGerar, self).__init__()
        self.text = "GERAR IMAGEM"
        self.background_color = "#282828"
        self.size_hint = (None, None)
        self.width = 250

    def on_press(self):
        gerarImagem()


class ButtonSave(Button):

    def __init__(self):
        super(ButtonSave, self).__init__()
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
        self.text = "LIMPAR"

    def on_press(self):
        reloadWidgets()

class ButtonReplace(Button):
    def __init__(self):
        super(ButtonReplace, self).__init__()
        self.size_hint = (None, None)
        self.height = 50
        self.background_color = "yellow"
        self.text = "SUBSTITUIR"



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
layoutBottom.size_hint = (None, None)
layoutBottom.width = 700
layoutBottom.height = 50
layoutBottom.spacing = 400

layoutBottomOptions = BoxLayout()
layoutBottomOptions.size_hint = (None, None)

txtInputCoord = TextInput()
txtInputCoord.disabled = True
txtInputCoord.size_hint = (0, 0)
txtInputCoord.width = 100
txtInputCoord.height = 50

buttonReplace = ButtonReplace()

root = tk.Tk()

#RETORNA O DIRETORIO DO USUARIO E COMPLEMENTA COM A PASTA DE REGISTROS DO PROGRAMA
pathOrigin = path.join(path.expanduser("~"), "Documents/image-generator-exobiology-ed").replace("\\", "/")
pathED = path.join(path.expanduser("~"), "Saved Games/Frontier Developments/Elite Dangerous").replace("\\", "/")

class MeuAplicativo(App):

    def build(self):
        self.title = "Image Generation Exobiology ED"

        buttonGerar = ButtonGerar()

        buttonReload = ButtonReload()

        buttonSave = ButtonSave()

        layoutBottomOptions.add_widget(buttonReload)
        layoutBottomOptions.add_widget(buttonSave)

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


        except FileExistsError as excep:
            print("ARQUIVO JÁ CRIADO")



@mainthread
def gerarImagem():

    try:

        value_txtinputJournal = json.loads(txtInputJournal.text)

        # REQUISIÇÃO NOME DO SISTEMA PELO CODIGO DO JOURNAL (RETORNA UM JSON STRING)
        requisitionNameSystem = requests.get(
            f"https://www.edsm.net/typeahead/systems/query/{value_txtinputJournal['SystemAddress']}")
        resultRequisitionNameSystem = requisitionNameSystem.json()[0]["value"]

        # CAPTURA O MONITOR PRINCIPAL E SALVA COMO ARQUIVO "TEMPORARIO"
        imagePrint = pyscreenshot.grab()
        imagePrint.save(f'{pathOrigin}/gallery/imgTemp.png')

        imageEdit.source = 'gallery/imgTemp.png'
        imageEdit.reload()

        # PREENCHE IMAGEM COM AS INFORMAÇÕES
        printscreen = Image.open(f'{pathOrigin}/gallery/imgTemp.png')
        mold = Image.open('resources/fundo_colorido_azul.png')
        moldStyle = Image.open('resources/molde_dna.png')
        efeitoVidro = Image.open('resources/efeito_vidro.png')
        maskVidro = Image.open('resources/efeito_vidro_mask.png')
        mold_draw = ImageDraw.Draw(mold)
        mold_font = ImageFont.truetype('fonts/TechnoBoard.ttf', 32)
        mold_fontSmall = ImageFont.truetype('fonts/Glitch inside.otf', 14)
        mold_draw.text((18, 26),
                       f"{value_txtinputJournal['Species_Localised']}\n {value_txtinputJournal['Variant_Localised'].split('- ')[1]} ",
                       font=mold_font)
        mold_draw.text((80, 128), f"{resultRequisitionNameSystem}", font=mold_fontSmall)

        mold.paste(moldStyle, (-1,-1), mask=moldStyle)

        mold.paste(efeitoVidro, (0,0), mask=maskVidro)

        mold.save(f'{pathOrigin}/gallery/imagemMoldeEscrito.png')



        colarMolde(printscreen, mold, (0, 0))

    except json.decoder.JSONDecodeError as JSONDecodeError:

        showAlert(JSONDecodeError.msg, "CÓDIGO DO JOURNAL INVÁLIDO", "fonts/error-5-199276.mp3", "ms")
        print("CÓDIGO DO JOURNAL INVÁLIDO")
        return None

    try:
        Window.size = (800, 600)
        layoutMain.add_widget(layoutImage)
    except kivy.uix.widget.WidgetException:
        print("WIDGET JÁ ADICIONADO")



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
        print(touch)

        x = int(touch.pos[0])
        y = int(touch.pos[1])

        try:
            imgTemp = Image.open(f'{pathOrigin}/gallery/imgTemp.png')
            mold = Image.open(f'{pathOrigin}/gallery/imagemMoldeEscrito.png')

            if (x >= 50 and x <= 750) and (y >= 100 and y <= 450):
                resolX = root.winfo_screenwidth()
                resolY = root.winfo_screenheight()

                proporcaoX = (resolX * 1.138) / 800
                proporcaoY = (resolY * 1.7) / 600

                x = int(((x - 50) * proporcaoX) - 43)
                y = int(-((y - 450) * proporcaoY) - 282)

                txtInputCoord.text = f"{x, y}"
                colarMolde(imgTemp, mold, (x, y))

        except FileNotFoundError:
            print("AGUARDANDO REGISTRO DO JOURNAL")


def createWatchdog():
    observer = Observer()

    @mainthread
    def on_modified(event):
        print(event)
        analisaJournal(event.src_path)

    try:
        event_handler = FileSystemEventHandler()
        event_handler.on_modified = on_modified

        #observer.schedule(event_handler, pathED, recursive=True)
        observer.schedule(event_handler, pathOrigin, recursive=True)
        observer.start()

        print("MONITORANDO")
        while not Window:
            time.sleep(1)
    except FileNotFoundError as excep:
        showAlert(excep.msg, "PASTA DE MONITORAMENTO DOS JOURNAIS NÃO ENCONTRADA", "fonts/error-5-199276.mp3", "ms")
        observer.stop()

    exit()


def analisaJournal(file_modified):
    dateNow = datetime.date.today()
    file_modified = file_modified.replace('\\', '/')

    if f"Journal.{dateNow}" in file_modified:

        archive = open(file_modified, "r", errors='replace')
        archiveRead = archive.readlines()
        archiveJournalLog = json.loads(archiveRead[len(archiveRead) - 1])

        if archiveJournalLog['event'] == 'ScanOrganic':
            txtInputJournal.text = json.dumps(archiveJournalLog)
            showAlert("", "", "fonts/system-notification-199277.mp3", "s")


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

        showAlert("ESPÉCIE REGISTRADA COM SUCESSO!", "REGISTRO CONCLUÍDO", "fonts/system-notification-199277.mp3", "ms")

        reloadWidgets()
        layoutBottom.spacing = 400
        toggleWidgets(layoutBottomOptions, buttonReplace, "r")

    else:
        showAlert("ESPÉCIE JÁ REGISTRADA!", "FALHA NO REGISTRO", "fonts/error-5-199276.mp3", "ms")
        layoutBottom.spacing = 300
        toggleWidgets(layoutBottomOptions, buttonReplace, "a")


def reloadWidgets():
    Window.size = (800, 200)
    layoutMain.remove_widget(layoutImage)
    txtInputJournal.text = ""
    toggleWidgets(layoutBottomOptions, buttonReplace, "r")
    layoutBottom.spacing = 400

def createObserverKeyboard():

    def on_presskeyboard(key):
        if key == Key.f2:
            gerarImagem()

    listener = Listener(on_press=on_presskeyboard)
    listener.start()

def showAlert(msg, tittle, sound, mode):

    def tocarmusica():
        playsound(sound)

    def mostrarAlerta():
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, msg, tittle, 0)

    if mode == "s":
        threadSound = Thread(target=tocarmusica)
        threadSound.start()
    if mode == "ms":
        threadSound = Thread(target=tocarmusica)
        trhedMessage = Thread(target=mostrarAlerta)
        threadSound.start()
        trhedMessage.start()


def toggleWidgets(father, children, mode):

    try:
        if (mode == "r"):
            father.remove_widget(children)
            print("REMOVENDO")
        elif (mode == "a"):
            father.add_widget(children)
            print("ADICIONANDO")


    except Exception as excep:
        print(excep)




if __name__ == "__main__":
    myApp = MeuAplicativo()
    myApp.run()
