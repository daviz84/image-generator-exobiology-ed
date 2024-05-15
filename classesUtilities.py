from kivy.uix.button import Button
from main import MeuAplicativo, clicarBotao

class ButtonGerar(Button):

    def __init__(self, **kwargs):
        super(ButtonGerar, self).__init__(**kwargs)
        self.text = "ENVIAR"
        self.background_color = "white"
        self.size_hint = (None, None)
        self.width = 250

    def on_press(self):
        clicarBotao()