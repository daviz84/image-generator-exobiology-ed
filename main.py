# Importar o App, Builder (GUI)
# Criar o nosso aplicativo
# criar a função build
from kivy.clock import mainthread
from kivy.config import Config

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
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
from pydub.playback import play
from pydub import AudioSegment
from playsound import playsound

# INSTANCIAÇÃO DOS ELEMENTOS GRÁFICOS

Window.clearcolor = "white"

layoutMain = BoxLayout()
layoutMain.orientation = "vertical"
layoutMain.padding = (50, 50, 50, 50)

txtInputJournal = TextInput()
txtInputJournal.id = "idTxtInput"

buttonGerar = Button()

layoutForm = BoxLayout()
layoutForm.width = 700
layoutForm.height = 100
layoutForm.size_hint = (None, None)

layoutImage = BoxLayout()
layoutImage.width = 700
layoutImage.height = 350
layoutImage.size_hint = (None, None)

imageEdit = AsyncImage()
imageEdit.size_hint = (None, None)
imageEdit.width = 700
imageEdit.height = 350
imageEdit.padding = (0, 0, 0, 0)
imageEdit.source = 'bordaazul.png'
imageEdit.fit_mode = "fill"

layoutBottom = BoxLayout()
layoutBottom.spacing = 500
layoutBottom.size_hint = (None, None)
layoutBottom.width = 700
layoutBottom.height = 50

txtInputCoord = TextInput()
txtInputCoord.disabled = True
txtInputCoord.size_hint = (0, 0)
txtInputCoord.width = 100
txtInputCoord.height = 50

buttonGerar = None

class MeuAplicativo(App):

    def build(self):
        self.title = "Image Generation Exobiology ED"

        buttonGerar = ButtonGerar()

        buttonSalvar = ButtonSalvar()

        layoutImage.add_widget(imageEdit)

        layoutForm.add_widget(txtInputJournal)
        layoutForm.add_widget(buttonGerar)

        layoutBottom.add_widget(txtInputCoord)
        layoutBottom.add_widget(buttonSalvar)

        layoutMain.add_widget(layoutForm)
        layoutMain.add_widget(layoutImage)
        layoutMain.add_widget(layoutBottom)

        layoutMain.add_widget(UpdatePos())  # BoxLayout adicionado para manter a posição do mouse atualizada

        return layoutMain

    def on_start(self):
        print("START")
        trhed = Thread(target=createWatchdog)
        trhed.start()




def clicarBotao():
    value_txtinputJournal = json.loads(txtInputJournal.text)

    #REQUISIÇÃO NOME DO SISTEMA PELO CODIGO
    requisicaoNameSystem = requests.get(
        f"https://www.edsm.net/typeahead/systems/query/{value_txtinputJournal['SystemAddress']}")
    resultRequisicaoNameSystem = requisicaoNameSystem.json()[0]["value"]

    imagemPrint = pyscreenshot.grab()
    imagemPrint.save('gallery/imgTemp.png')

    imageEdit.source = 'gallery/imgTemp.png'
    imageEdit.reload()

    #PREENCHE IMAGEM COM AS INFORMAÇÕES
    captura = Image.open('gallery/imgTemp.png')
    molde = Image.open('gallery/imagemMolde.png')
    molde_draw = ImageDraw.Draw(molde)
    mold_font = ImageFont.truetype('fonts/TechnoBoard.ttf', 26)
    mold_fontSmall = ImageFont.truetype('fonts/Glitch inside.otf', 12)
    molde_draw.text((258, 53),
                    f"{value_txtinputJournal['Species_Localised']}\n {value_txtinputJournal['Variant_Localised'].split('- ')[1]} ",
                    font=mold_font)
    molde_draw.text((360, 115), f"{resultRequisicaoNameSystem}", font=mold_fontSmall)

    molde.save('gallery/imagemMoldeEscrito.png')

    confirmarPosicao(captura, molde, (0, 0))


def confirmarPosicao(captura, molde, positions):
    captura.paste(molde, (positions[0], positions[1]), mask=molde)
    captura.save('gallery/imagemMesclada.png')

    imageEdit.source = 'gallery/imagemMesclada.png'
    imageEdit.reload()


def atualizaPosicoes(tupla):
    valX = int(tupla[0])
    valY = int(tupla[1])

    return (valX, valY)


class UpdatePos(BoxLayout):
    def __init__(self, **kwargs):
        super(UpdatePos, self).__init__(**kwargs)
        self.size = (0, 0)
        self.size_hint = (None, None)

    def on_touch_down(self, touch):
        x = atualizaPosicoes((touch.pos[0], touch.pos[1]))[0]
        y = atualizaPosicoes((touch.pos[0], touch.pos[1]))[1]

        print(atualizaPosicoes(touch.pos))

        capturaEsc = Image.open('gallery/imgTemp.png')
        moldeEsc = Image.open('gallery/imagemMoldeEscrito.png')

        if ((int(touch.pos[0]) >= 50 and int(touch.pos[0]) <= 750) and (
                int(touch.pos[1]) >= 100 and int(touch.pos[1]) <= 450)):
            resolX = 1440
            resolY = 900
            proporcaoX = (resolX * 1.18) / 800
            proporcaoY = (resolY * 1.6) / 600

            x = ((x - 50) * proporcaoX) - 200
            y = -((y - 450) * proporcaoY) - 200

            txtInputCoord.text = f"{x, y}"
            confirmarPosicao(capturaEsc, moldeEsc, atualizaPosicoes((x, y)))


class ButtonGerar(Button):

    def __init__(self):
        super(ButtonGerar, self).__init__()
        self.text = "GERAR IMAGEM"
        self.background_color = "white"
        self.size_hint = (None, None)
        self.width = 250

    def on_press(self):
        clicarBotao()



class ButtonSalvar(Button):

    def __init__(self):
        super(ButtonSalvar, self).__init__()
        self.size_hint = (None, None)
        self.height = 50
        self.text = "SALVAR"

    def on_press(self):
        registrarDescoberta()


def createWatchdog():
    observer = Observer()

    @mainthread
    def on_modified(event):
        print(event)
        testeComJournal(event.src_path)


    event_handler = FileSystemEventHandler()
    event_handler.on_modified = on_modified

    path = "C:/Users/davio/Desktop/fileMod"

    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        print("Monitorando")
        while not Window:
            time.sleep(1)
    except Exception:
        print("Terminado")
        observer.stop()
    exit()


def registrarDescoberta():
    registroJournal = json.loads(txtInputJournal.text)
    especie = registroJournal['Variant_Localised']

    arquivo = open('C:/Users/davio/Desktop/fileMod/registro.json', 'r')
    jsonManipulavel = json.loads(arquivo.read())

    if especie not in jsonManipulavel['especiesCatalogadas']:
        jsonManipulavel['especiesCatalogadas'].__setitem__(especie, {"registro": registroJournal})
        arquivo.close()

        arquivo = open('C:/Users/davio/Desktop/fileMod/registro.json', 'w')
        arquivo.write(json.dumps(jsonManipulavel))
        arquivo.close()

    else:
        print("Espécie já registrada")

def testeComJournal(file_modified):

    dateNow = datetime.date.today()
    file_modified = file_modified.replace(r'\\', '/')

    if f"Journal.{dateNow}" in file_modified:
        print("YESSS")

        archive = open(file_modified, "r", errors='replace')
        archiveLido = archive.readlines()
        arquivoJournalLog = json.loads(archiveLido[len(archiveLido) - 1])

        if arquivoJournalLog['event'] == 'ScanOrganic':
            txtInputJournal.text = json.dumps(arquivoJournalLog)
            playsound('system-notification-199277.mp3')



if __name__ == "__main__":
    MeuAplicativo().run()
