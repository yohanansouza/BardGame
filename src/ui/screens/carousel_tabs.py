from kivy.uix.carousel import Carousel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


class CarouselTabs(BoxLayout):
    """Wrapper simples para um Carousel que conterá várias abas/screens.

    Uso:
        from ui.screens.carousel_tabs import CarouselTabs
        c = CarouselTabs()
        c.add_tab(widget, title='Atributos')
    """

    carousel = ObjectProperty(None)
    controls = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        # Controles superiores (setas)
        ctrl = BoxLayout(size_hint_y=None, height=40)
        btn_prev = Button(text='<', size_hint_x=None, width=40)
        btn_next = Button(text='>', size_hint_x=None, width=40)
        title = Label(text='Tabs Carousel', halign='center')
        btn_prev.bind(on_press=lambda *_: self.show_previous())
        btn_next.bind(on_press=lambda *_: self.show_next())
        ctrl.add_widget(btn_prev)
        ctrl.add_widget(title)
        ctrl.add_widget(btn_next)

        self.add_widget(ctrl)

        # Carousel
        self.carousel = Carousel(direction='right')
        self.add_widget(self.carousel)

    def add_tab(self, widget: Widget, title: str = ''):
        # Para simplicidade, adiciona o widget diretamente ao carousel
        self.carousel.add_widget(widget)

    def show_next(self):
        try:
            self.carousel.load_next(mode='next')
        except Exception:
            pass

    def show_previous(self):
        try:
            self.carousel.load_previous()
        except Exception:
            pass

