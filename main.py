# Importar o App, Builder (GUI)
# Criar o nosso aplicativo
# criar a função build
from kivy.config import Config

Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '450')
Config.set('graphics', 'resizable', True)

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
import json

textInputUm = TextInput()
textInputCoord = TextInput()
buttonGerar = Button()
imageEdit = AsyncImage()
imageEdit.size_hint = (None,None)
imageEdit.width = 500
imageEdit.height = 200
imageEdit.padding = (0,0,0,0)


#PARTE CÓDIGO FUNCIONAL
class MeuAplicativo(App):

    def build(self):
        self.title = "APP DAVI"

        buttonGerar = ButtonGerar()

        textInputUm.text = ""
        textInputUm.id = "idTxtInput"

        textInputCoord.size_hint = (0, 0)
        textInputCoord.width = 100
        textInputCoord.height = 50

        layoutMain = BoxLayout()
        layoutMain.orientation = "vertical"
        layoutMain.padding = (50, 50, 50, 50)

        layoutForm = BoxLayout()
        layoutForm.width = 500
        layoutForm.size_hint = (None, None)

        layoutImage = BoxLayout()
        layoutImage.width = 500
        layoutImage.height = 200
        layoutImage.padding = (0,0,0,0)

        layoutImage.size_hint = (None,None)

        layoutImage.add_widget(imageEdit)


        layoutForm.add_widget(textInputUm)
        layoutForm.add_widget(buttonGerar)

        layoutMain.add_widget(UpdatePos())
        layoutMain.add_widget(layoutForm)
        layoutMain.add_widget(layoutImage)
        layoutMain.add_widget(textInputCoord)

        return layoutMain


def clicarBotao():
    value_txtinputJournal = json.loads(textInputUm.text)

    #REQUISIÇÃO NOME DO SYSTEMA PELO CODIGO
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
    captura.paste(molde, (positions[0], -positions[1]), mask=molde)
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

        capturaEsc = Image.open('gallery/imgTemp.png')
        moldeEsc = Image.open('gallery/imagemMoldeEscrito.png')

        if((int(touch.pos[0]) >= 140 and int(touch.pos[0]) <= 460) and (int(touch.pos[1]) >= 100 and int(touch.pos[1]) <= 300) ):
            x = ((x - 140) * 4.4) - 180
            y = ((y - 250) * 4.4) - 20
            textInputCoord.text = f"{x, y}"
            confirmarPosicao(capturaEsc, moldeEsc, atualizaPosicoes((x, y)))


class ButtonGerar(Button):

    def __init__(self, **kwargs):
        super(ButtonGerar, self).__init__(**kwargs)
        self.text = "ENVIAR"
        self.background_color = "green"

    def on_press(self):
        clicarBotao()


MeuAplicativo().run()
