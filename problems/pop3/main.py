from kivy.app import App
from kivy.uix.widget import Widget

class WordConstructorGame(Widget):
    pass


class WordConstructorApp(App):
    def build(self):
        return WordConstructorGame()


if __name__ == '__main__':
    WordConstructorApp().run()