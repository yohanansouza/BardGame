from kivy.app import App
from kivy.uix.label import Label

from ui.screens.carousel_tabs import CarouselTabs
from ui.screens.attributes_tab import AttributesTab


class DemoApp(App):
    def build(self):
        carousel = CarouselTabs()
        # adicionar a aba de atributos
        attr_tab = AttributesTab()
        carousel.add_tab(attr_tab, title='Atributos')

        # adiciona uma tab de exemplo
        carousel.add_tab(Label(text='Outra Aba - Exemplo', halign='center'))

        return carousel


if __name__ == '__main__':
    DemoApp().run()
