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


class Botaogerar(Button):

    def __init__(self):
        super(Botaogerar, self).__init__()
        self.text = "GERAR IMAGEM"
        self.background_color = "#282828"
        self.size_hint = (None, None)
        self.width = 250

    def on_press(self):
        gerar_imagem()


class Botaoregistrar(Button):

    def __init__(self):
        super(Botaoregistrar, self).__init__()
        self.size_hint = (None, None)
        self.height = 50
        self.background_color = "green"
        self.text = "SALVAR"

    def on_press(self):
        registrar_descoberta()


class Botaorecarregar(Button):
    def __init__(self):
        super(Botaorecarregar, self).__init__()
        self.size_hint = (None, None)
        self.height = 50
        self.background_color = "red"
        self.text = "LIMPAR"

    def on_press(self):
        recarregar_widgets()


class Botaosubstituir(Button):
    def __init__(self):
        super(Botaosubstituir, self).__init__()
        self.size_hint = (None, None)
        self.height = 50
        self.background_color = "yellow"
        self.text = "SUBSTITUIR"

    def on_press(self):
        registro_journal = json.loads(txt_entrada_journal.text)
        especie = registro_journal['Variant_Localised']

        imagem_com_borda_atual = Image.open(f'{caminho_fonte}/gallery/imagemCortadaComBorda.png')
        imagem_com_borda_atual.save(f'{caminho_fonte}/gallery/REGISTRO DE ESPECIES/{especie}.png')

        recarregar_widgets()
        layout_rodape.spacing = 400
        alterar_widgets(layout_rodape_botoes, botao_substituir, "r")


class Botaopequenocolorido(Button):

    def __init__(self, cor, txt):
        super(Botaopequenocolorido, self).__init__()
        self.size_hint = (None, None)
        self.height = 35
        self.width = 50
        self.background_color = cor
        self.text = txt
        self.disabled = True

    def on_press(self):

        try:
            img_temp = Image.open(f'{caminho_fonte}/gallery/imgTemp.png')

        except FileNotFoundError:
            print("AGUARDANDO REGISTRO DO JOURNAL")

        resetar_botoes_pequenos("t")
        self.disabled = True

        match self.text:

            case "R":
                molde_atual["cor"] = "R"
                colar_molde(img_temp, gerar_molde("R"), posicao_atual["pos"], molde_atual["cor"])
            case "G":
                molde_atual["cor"] = "G"
                colar_molde(img_temp, gerar_molde("G"), posicao_atual["pos"], molde_atual["cor"])
            case "B":
                molde_atual["cor"] = "B"
                colar_molde(img_temp, gerar_molde("B"), posicao_atual["pos"], molde_atual["cor"])
            case "Y":
                molde_atual["cor"] = "Y"
                colar_molde(img_temp, gerar_molde("Y"), posicao_atual["pos"], molde_atual["cor"])


class Botaopequenoalterarimagem(Button):

    def __init__(self, txt):
        super(Botaopequenoalterarimagem, self).__init__()
        self.size_hint = (None, None)
        self.height = 35
        self.width = 50
        self.background_color = "black"
        self.text = txt
        self.disabled = True

    def on_press(self):

        if "imagemMesclada" in editor_imagem.source:
            editor_imagem.source = f'{caminho_fonte}/gallery/imagemCortadaComBorda.png'
            editor_imagem.reload()
        else:
            editor_imagem.source = f'{caminho_fonte}/gallery/imagemMesclada.png'
            editor_imagem.reload()


class Botaopequenoalterarjournal(Button):

    def __init__(self, txt, modo):
        super(Botaopequenoalterarjournal, self).__init__()
        self.size_hint = (None, None)
        self.height = 50
        self.width = 35
        self.background_color = "black"
        self.text = txt
        self.modo = modo
        if modo == "D":
            self.disabled = True

    def on_press(self):
        registro_journais_temporarios = open(f'{caminho_fonte}/journaisTemporarios.json', 'r')
        registro_journais_temporarios_json = json.loads(registro_journais_temporarios.read())

        try:
            match self.modo:

                case "U":

                    botao_pequeno_alterar_jornal_d.disabled = False
                    contagem = contagem_atual_journal_temporario["contagem"] - 1

                    if contagem >= 0:
                        txt_entrada_journal.text = registro_journais_temporarios_json["journaisTemporarios"][contagem]
                        contagem_atual_journal_temporario["contagem"] = contagem

                    if contagem == 0:
                        botao_pequeno_alterar_jornal_u.disabled = True

                case "D":

                    botao_pequeno_alterar_jornal_u.disabled = False
                    contagem = contagem_atual_journal_temporario["contagem"] + 1

                    if contagem >= 2:
                        botao_pequeno_alterar_jornal_d.disabled = True

                    txt_entrada_journal.text = registro_journais_temporarios_json["journaisTemporarios"][contagem]
                    contagem_atual_journal_temporario["contagem"] = contagem

        except IndexError:
            print("INDEX NÃO ENCONTRADO")


# INSTANCIAÇÃO DOS ELEMENTOS GRÁFICOS

Window.clearcolor = "white"

layout_principal = BoxLayout()
layout_principal.orientation = "vertical"
layout_principal.padding = (50, 50, 50, 50)
layout_principal.minimum_height = 600

layout_formulario = BoxLayout()
layout_formulario.width = 700
layout_formulario.height = 100
layout_formulario.size_hint = (None, None)

txt_entrada_journal = TextInput()
botao_gerar = Botaogerar()

layout_botoes_pequenos_alterar_journal = BoxLayout()
layout_botoes_pequenos_alterar_journal.orientation = "vertical"
layout_botoes_pequenos_alterar_journal.size_hint = (None, None)
layout_botoes_pequenos_alterar_journal.height = 100
layout_botoes_pequenos_alterar_journal.width = 50

botao_pequeno_alterar_jornal_u = Botaopequenoalterarjournal("-", "U")  #UPPER (SUBIR)
botao_pequeno_alterar_jornal_d = Botaopequenoalterarjournal("+", "D")  #DOWN (DESCER)

layout_botoes_pequenos = BoxLayout()
layout_botoes_pequenos.size_hint = (None, None)
layout_botoes_pequenos.width = 700
layout_botoes_pequenos.height = 35
layout_botoes_pequenos.orientation = "horizontal"
layout_botoes_pequenos.spacing = 400

layout_botoes_pequenos_cor = BoxLayout()
layout_botoes_pequenos_cor.size_hint = (None, None)
layout_botoes_pequenos_cor.height = 35
layout_botoes_pequenos_cor.width = 200

botao_pequeno_red = Botaopequenocolorido("#ff4d42", "R")
botao_pequeno_red.disabled = True
botao_pequeno_green = Botaopequenocolorido("#2e9800", "G")
botao_pequeno_blue = Botaopequenocolorido("#4981ff", "B")
botao_pequeno_yellow = Botaopequenocolorido("#f8ff07", "Y")

layout_botoes_pequenos_alterar_imagem = BoxLayout()
layout_botoes_pequenos_alterar_imagem.size_hint = (None, None)
layout_botoes_pequenos_alterar_imagem.width = 100
layout_botoes_pequenos_alterar_imagem.height = 35

botao_pequeno_alterar_imagem_u = Botaopequenoalterarimagem("<")
botao_pequeno_alterar_imagem_r = Botaopequenoalterarimagem(">")

layout_imagem = BoxLayout()
layout_imagem.width = 700
layout_imagem.height = 400
layout_imagem.size_hint = (None, None)
layout_imagem.orientation = "vertical"

editor_imagem = AsyncImage()
editor_imagem.size_hint = (None, None)
editor_imagem.width = 700
editor_imagem.height = 350
editor_imagem.padding = (0, 0, 0, 0)
editor_imagem.fit_mode = "fill"

layout_rodape = BoxLayout()
layout_rodape.size_hint = (None, None)
layout_rodape.width = 700
layout_rodape.height = 50
layout_rodape.spacing = 400

txt_entrada_coord = TextInput()
txt_entrada_coord.disabled = True
txt_entrada_coord.size_hint = (0, 0)
txt_entrada_coord.width = 100
txt_entrada_coord.height = 50

layout_rodape_botoes = BoxLayout()
layout_rodape_botoes.size_hint = (None, None)

botao_recarregar = Botaorecarregar()
botao_registrar = Botaoregistrar()
botao_substituir = Botaosubstituir()

root = tk.Tk()

#RETORNA O DIRETORIO DO USUARIO E COMPLEMENTA COM A PASTA DE REGISTROS DO PROGRAMA
caminho_fonte = path.join(path.expanduser("~"), "Documents/image-generator-exobiology-ed").replace("\\", "/")

#RETORNA O DIRETORIO DO USUARIO E COMPLEMENTA COM A PASTA DE REGISTROS DOS JOURNAIS
caminho_ed_journais = path.join(path.expanduser("~"), "Saved Games/Frontier Developments/Elite Dangerous").replace("\\",
                                                                                                                   "/")

#VARIÁVEIS DE CONTROLE
todos_botoes_pequenos = []
todos_botoes_pequenos.append(
    [botao_pequeno_red, botao_pequeno_green, botao_pequeno_blue, botao_pequeno_yellow, botao_pequeno_alterar_imagem_u,
     botao_pequeno_alterar_imagem_r])
posicao_atual = {'pos': (0, 0)}  #UTILIZADA PARA MUDAR A COR DE FUNDO DO MOLDE NOS BOTÕES PEQUENOS
molde_atual = {'cor': 'R'}  #UTILIZADA PARA MUDAR A COR DE FUNDO DO MOLDE NOS BOTÕES PEQUENOS
contagem_atual_journal_temporario = {"contagem": 3}  # INICIADO COM 1 A MAIS POR QUESTÃO VISUAL


class Meuaplicativo(App):

    def build(self):
        self.title = "Gerador de Imagens para Exobiologia ED"

        #MONTAGEM DO LAYOUT PRINCIPAL DO PROGRAMA

        layout_botoes_pequenos_alterar_journal.add_widget(botao_pequeno_alterar_jornal_u)
        layout_botoes_pequenos_alterar_journal.add_widget(botao_pequeno_alterar_jornal_d)

        layout_botoes_pequenos_alterar_imagem.add_widget(botao_pequeno_alterar_imagem_u)
        layout_botoes_pequenos_alterar_imagem.add_widget(botao_pequeno_alterar_imagem_r)

        layout_rodape_botoes.add_widget(botao_recarregar)
        layout_rodape_botoes.add_widget(botao_registrar)

        layout_rodape.add_widget(txt_entrada_coord)
        layout_rodape.add_widget(layout_rodape_botoes)

        layout_imagem.add_widget(editor_imagem)
        layout_imagem.add_widget(layout_rodape)

        layout_formulario.add_widget(txt_entrada_journal)
        layout_formulario.add_widget(layout_botoes_pequenos_alterar_journal)
        layout_formulario.add_widget(botao_gerar)

        layout_botoes_pequenos_cor.add_widget(botao_pequeno_red)
        layout_botoes_pequenos_cor.add_widget(botao_pequeno_green)
        layout_botoes_pequenos_cor.add_widget(botao_pequeno_blue)
        layout_botoes_pequenos_cor.add_widget(botao_pequeno_yellow)

        layout_botoes_pequenos.add_widget(layout_botoes_pequenos_cor)
        layout_botoes_pequenos.add_widget(layout_botoes_pequenos_alterar_imagem)

        layout_principal.add_widget(layout_formulario)

        layout_principal.add_widget(Atualizacliques())  # BoxLayout adicionado para manter a posição do mouse atualizada

        return layout_principal

    def on_start(self):
        criar_observador_teclado()

        #INSTANCIA E INICIA O WATCHDOG EM OUTRA THREAD (RESPONSAVEL POR MONITORAR OS REGISTROS DO JOGO - PASTAS E ARQUIVOS)
        thread = Thread(target=cria_watchdog)
        thread.start()

        #CRIA OS ARQUIVOS DE REGISTRO PARA ARMANEZAR AS ESPÉCIES ANALISADAS E JOURNAIS
        try:
            os.mkdir(f'{caminho_fonte}')
            os.mkdir(f'{caminho_fonte}/gallery')
            os.mkdir(f'{caminho_fonte}/gallery/REGISTRO DE ESPECIES')

            arquivo_registros_especies = open(f'{caminho_fonte}/registro.json', 'w')
            arquivo_registros_especies.write('{"especiesCatalogadas": {}}')
            arquivo_registros_especies.close()

            arquivo_journais_temporarios = open(f'{caminho_fonte}/journaisTemp.json', 'w')
            arquivo_journais_temporarios.write('{"journaisTemporarios":["", "", ""]}')
            arquivo_journais_temporarios.close()

        except FileExistsError:
            print("ARQUIVO JÁ CRIADO")


@mainthread  #NOTAÇÃO UTILIZADA PARA INDICAR QUE A FUNÇÃO SERÁ EXECUTADA NA TRHEAD PRINCIPAL, NECESSÁRIO PARA MODIFICAR OS WIDGETS DO KIVY
def gerar_imagem():
    try:
        imagem_molde_escrito = gerar_molde()

        # CAPTURA O MONITOR PRINCIPAL E SALVA COMO ARQUIVO "TEMPORARIO"
        imagem_captura_tela = pyscreenshot.grab()
        imagem_captura_tela.save(f'{caminho_fonte}/gallery/imgTemp.png')

        #printscreen = Image.open(f'{caminho_fonte}/gallery/imgTemp.png')

        colar_molde(imagem_captura_tela, imagem_molde_escrito, (0, 0), molde_atual["cor"])
        posicao_atual["pos"] = (0, 0)
        resetar_botoes_pequenos("t")

    except json.decoder.JSONDecodeError as JSONDecodeError:
        notifica_alerta(JSONDecodeError.msg, "CÓDIGO DO JOURNAL INVÁLIDO", "fonts/error-5-199276.mp3", "ms")
        print("CÓDIGO DO JOURNAL INVÁLIDO")
        return None  #ENCERRA A FUNÇÃO

    try:
        Window.size = (800, 600)
        layout_principal.add_widget(layout_botoes_pequenos)
        layout_principal.add_widget(layout_imagem)


    except kivy.uix.widget.WidgetException:
        print("WIDGET JÁ ADICIONADO")
        return None  #ENCERRA A FUNÇÃO


def gerar_molde(cor="R"):
    registro_journal = json.loads(txt_entrada_journal.text)

    # REQUISIÇÃO NOME DO SISTEMA PELO CODIGO DO JOURNAL (RETORNA UM JSON STRING)
    realiza_requisicao_nome_sistema = requests.get(
        f"https://www.edsm.net/typeahead/systems/query/{registro_journal['SystemAddress']}")
    resultado_nome_sistema = realiza_requisicao_nome_sistema.json()[0]["value"]

    # PREENCHE IMAGEM COM AS INFORMAÇÕES
    molde = Image.open(f'resources/fundo_colorido_{cor}.png')
    estilo_molde = Image.open('resources/molde_dna.png')
    efeito_vidro = Image.open('resources/efeito_vidro.png')
    mascara_vidro = Image.open('resources/efeito_vidro_mask.png')
    molde_escrever = ImageDraw.Draw(molde)

    molde_fonte_especie = ImageFont.truetype('fonts/TechnoBoard.ttf', 29)
    molde_fonte_sistema = ImageFont.truetype('fonts/Glitch inside.otf', 14)

    #CASO EXCEDA O NÚMERO DE CARACTERES QUE CAIBA NA PLAQUINHA
    if len(registro_journal['Species_Localised']) > 19:
        molde_fonte_especie = ImageFont.truetype('fonts/TechnoBoard.ttf', 25)

    molde_escrever.text((18, 26),
                        f"{registro_journal['Species_Localised']}\n{registro_journal['Variant_Localised'].split('- ')[1]} ",
                        font=molde_fonte_especie)
    molde_escrever.text((80, 123), f"{resultado_nome_sistema}", font=molde_fonte_sistema)

    molde.paste(estilo_molde, (-1, -1), mask=estilo_molde)

    molde.paste(efeito_vidro, (0, 0), mask=mascara_vidro)

    molde.save(f'{caminho_fonte}/gallery/imagemMoldeEscrito.png')

    return Image.open(f'{caminho_fonte}/gallery/imagemMoldeEscrito.png')


def colar_molde(captura_tela, molde, posicoes, cor="R"):
    captura_tela.paste(molde, posicoes, mask=molde)
    captura_tela.save(f'{caminho_fonte}/gallery/imagemMesclada.png')

    gerar_miniatura(captura_tela, posicoes, cor)

    editor_imagem.source = f'{caminho_fonte}/gallery/imagemMesclada.png'
    editor_imagem.reload()


def gerar_miniatura(img, posicoes, cor="R"):
    pontaUmX = posicoes[0] - 534  # -100 da plaquinha
    pontaUmY = posicoes[1] - 50
    pontaDoisX = posicoes[0] + 435  # +100 da plaquinha
    pontaDoisY = posicoes[1] + 500

    if pontaUmX < 0:
        while pontaUmX <= 0:
            pontaUmX = pontaUmX + 25
            pontaDoisX = pontaDoisX + 25

    if pontaDoisX > img.size[0]:
        while pontaDoisX >= img.size[0]:
            pontaUmX = pontaUmX - 25
            pontaDoisX = pontaDoisX - 25

    if pontaUmY < 0:
        while pontaUmY <= 0:
            pontaUmY = pontaUmY + 25
            pontaDoisY = pontaDoisY + 25

    if pontaDoisY > img.size[1]:
        while pontaDoisY >= img.size[1]:
            pontaUmY = pontaUmY - 25
            pontaDoisY = pontaDoisY - 25

    imagem_cortada = img.crop((pontaUmX, pontaUmY, pontaDoisX, pontaDoisY))

    borda_molde = Image.open(f'resources/borda_miniatura_M.png')
    borda_molde_colorida = Image.open(f'resources/borda_miniatura_{cor}.png')

    borda_molde.paste(imagem_cortada, (70, 37))

    borda_molde.paste(borda_molde_colorida, (0, 0), borda_molde_colorida)

    #imagem_cortada.save(f'{caminho_fonte}/gallery/imagemCortada.png')
    borda_molde.save(f'{caminho_fonte}/gallery/imagemCortadaComBorda.png')


class Atualizacliques(BoxLayout):
    def __init__(self):
        super(Atualizacliques, self).__init__()
        self.size = (0, 0)
        self.size_hint = (None, None)

    def on_touch_down(self, touch):
        print(touch)

        x = int(touch.pos[0])
        y = int(touch.pos[1])

        try:
            imagem_captura_tela = Image.open(f'{caminho_fonte}/gallery/imgTemp.png')
            molde = Image.open(f'{caminho_fonte}/gallery/imagemMoldeEscrito.png')

            if (50 <= x <= 750) and (100 <= y <= 450) and (Window.size == (800, 600)):
                resol_monitor_x = root.winfo_screenwidth()
                resol_monitor_y = root.winfo_screenheight()

                proporcaoX = (resol_monitor_x * 1.138) / 800
                proporcaoY = (resol_monitor_y * 1.7) / 600

                x = int(((x - 50) * proporcaoX) - 43)
                y = int(-((y - 450) * proporcaoY) - 282)

                txt_entrada_coord.text = f"{x, y}"

                colar_molde(imagem_captura_tela, molde, (x, y), molde_atual["cor"])
                posicao_atual["pos"] = (x, y)

        except FileNotFoundError:
            print("AGUARDANDO REGISTRO DO JOURNAL")

def cria_watchdog():
    observer = Observer()

    @mainthread
    def on_modified(event):
        print(event)
        analisa_journal(event.src_path)

    try:
        event_handler = FileSystemEventHandler()
        event_handler.on_modified = on_modified

        observer.schedule(event_handler, caminho_ed_journais, recursive=True)
        #observer.schedule(event_handler, pathOrigin, recursive=True)
        observer.start()

        print("MONITORANDO")
        while not Window:
            time.sleep(1)
    except FileNotFoundError as excep:
        notifica_alerta(excep.msg, "PASTA DE MONITORAMENTO DOS JOURNAIS NÃO ENCONTRADA", "fonts/error-5-199276.mp3",
                        "ms")
        observer.stop()

    exit()


def analisa_journal(arquivo_modificado):

    data_hoje = datetime.datetime.now()
    data_ontem = (data_hoje - datetime.timedelta(days=1))
    arquivo_modificado = arquivo_modificado.replace('\\', '/')

    if f"Journal.{data_hoje.strftime("%Y-%m-%d")}" in arquivo_modificado or f"Journal.{data_ontem.strftime("%Y-%m-%d")}" in arquivo_modificado:

        journal_atualizado = open(arquivo_modificado, "r", errors='replace')
        journal_lido = journal_atualizado.readlines()
        log_journal = json.loads(journal_lido[len(journal_lido) - 1])
        journal_atualizado.close()

        if log_journal['event'] == 'ScanOrganic':
            arquivo_registros_especies = open(f'{caminho_fonte}/registro.json', 'r')
            arquivo_registros_especies_json = json.loads(arquivo_registros_especies.read())
            arquivo_registros_especies.close()

            if log_journal['Variant_Localised'] not in arquivo_registros_especies_json['especiesCatalogadas']:
                txt_entrada_journal.text = json.dumps(log_journal)
                notifica_alerta("", "", "fonts/system-notification-199277.mp3", "s")
                preenche_journais_temporarios(json.dumps(log_journal))


def registrar_descoberta():
    registro_journal = json.loads(txt_entrada_journal.text)
    especie = registro_journal['Variant_Localised']

    arquivo_registros_especies = open(f'{caminho_fonte}/registro.json', 'r')
    arquivo_registros_especies_json = json.loads(arquivo_registros_especies.read())

    if especie not in arquivo_registros_especies_json['especiesCatalogadas']:
        arquivo_registros_especies_json['especiesCatalogadas'].__setitem__(especie, {"registro": registro_journal})
        arquivo_registros_especies.close()

        arquivo_registros_especies = open(f'{caminho_fonte}/registro.json', 'w')
        arquivo_registros_especies.write(json.dumps(arquivo_registros_especies_json))
        arquivo_registros_especies.close()

        imagem_com_borda_atual = Image.open(f'{caminho_fonte}/gallery/imagemCortadaComBorda.png')
        imagem_com_borda_atual.save(f'{caminho_fonte}/gallery/REGISTRO DE ESPECIES/{especie}.png')

        notifica_alerta("ESPÉCIE REGISTRADA COM SUCESSO!", "REGISTRO CONCLUÍDO", "fonts/system-notification-199277.mp3",
                        "ms")

        recarregar_widgets()
        layout_rodape.spacing = 400
        alterar_widgets(layout_rodape_botoes, botao_substituir, "r")

    else:
        notifica_alerta("ESPÉCIE JÁ REGISTRADA! CASO QUEIRA SUBSTITUIR A MINIATURA ATUAL PRESSIONE 'SUBSTITUIR'", "FALHA NO REGISTRO", "fonts/error-5-199276.mp3", "ms")
        layout_rodape.spacing = 300
        alterar_widgets(layout_rodape_botoes, botao_substituir, "a")


def recarregar_widgets():
    Window.size = (800, 200)
    layout_principal.remove_widget(layout_imagem)
    layout_principal.remove_widget(layout_botoes_pequenos)
    txt_entrada_journal.text = ""
    alterar_widgets(layout_rodape_botoes, botao_substituir, "r")
    layout_rodape.spacing = 400
    resetar_botoes_pequenos("r")
    posicao_atual["pos"] = (0, 0)


def criar_observador_teclado():
    def on_presskeyboard(key):
        if key == Key.f2:
            gerar_imagem()

    listener = Listener(on_press=on_presskeyboard)
    listener.start()


def notifica_alerta(msg, titulo, som, modo):
    def tocarmusica():
        playsound(som)

    def mostrarAlerta():
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, msg, titulo, 0)

    if modo == "s":
        threadSound = Thread(target=tocarmusica)
        threadSound.start()
    if modo == "ms":
        threadSound = Thread(target=tocarmusica)
        trhedMessage = Thread(target=mostrarAlerta)
        threadSound.start()
        trhedMessage.start()


def alterar_widgets(widgetPai, widgetFilho, modo):
    try:
        if (modo == "r"):
            widgetPai.remove_widget(widgetFilho)
            print("REMOVENDO")
        elif (modo == "a"):
            widgetPai.add_widget(widgetFilho)
            print("ADICIONANDO")


    except Exception as excep:
        print(excep)


def resetar_botoes_pequenos(mode="t"):
    for botao in todos_botoes_pequenos[0]:

        if mode == "t":
            if botao.disabled == True:
                botao.disabled = False
            else:
                botao.disabled = False
        elif mode == "r":
            botao.disabled = True


def preenche_journais_temporarios(journal):
    registro_journais_temporarios = open(f'{caminho_fonte}/journaisTemporarios.json', 'r')
    registro_journais_temporarios_json = json.loads(registro_journais_temporarios.read())

    registro_journais_temporarios_json["journaisTemporarios"].pop(0)
    registro_journais_temporarios_json["journaisTemporarios"].append(journal)

    registro_journais_temporarios.close()

    registro_journais_temporarios = open(f'{caminho_fonte}/journaisTemporarios.json', 'w')
    registro_journais_temporarios.write(json.dumps(registro_journais_temporarios_json))
    registro_journais_temporarios.close()


if __name__ == "__main__":
    meu_aplicativo = Meuaplicativo()
    meu_aplicativo.run()
