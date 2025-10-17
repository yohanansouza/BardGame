from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.properties import NumericProperty, StringProperty


class AttributesTab(BoxLayout):
    """Aba simples para editar atributos. Exemplo mínimo com Agilidade."""

    agility = NumericProperty(10)
    agility_bonus = StringProperty('0')

    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        title = Label(text='Atributos', size_hint_y=None, height=40, font_size='18sp')
        self.add_widget(title)

        # Agilidade
        box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
        box.add_widget(Label(text='Agilidade', size_hint_x=0.4))
        self.agility_input = TextInput(text=str(self.agility), multiline=False, size_hint_x=0.3)
        self.agility_input.bind(text=self.on_agility_text)
        box.add_widget(self.agility_input)
        self.bonus_label = Label(text=f'Bônus: {self.agility_bonus}', size_hint_x=0.3)
        box.add_widget(self.bonus_label)

        self.add_widget(box)

        btn_update = Button(text='Atualizar', size_hint_y=None, height=40)
        btn_update.bind(on_press=lambda *_: self.update_bonus())
        self.add_widget(btn_update)

        # Inicial calcula
        self.update_bonus()

    def on_agility_text(self, instance, value):
        try:
            self.agility = int(value)
        except Exception:
            # manter valor anterior se inválido
            pass

    def calculate_agility_bonus(self, value: int) -> int:
        """Regra inicial de mapeamento valor -> bônus de agilidade.

        Regras padrão (configurável futuramente):
        - <=8 -> -1
        - 9-11 -> 0
        - >=12 -> +1
        """
        if value <= 8:
            return -1
        if 9 <= value <= 11:
            return 0
        if value >= 12:
            # Escala simples: cada +2 acima de 12 aumenta +1 (opcional)
            return 1 + max(0, (value - 12) // 2)

        return 0

    def update_bonus(self):
        bonus = self.calculate_agility_bonus(self.agility)
        self.agility_bonus = f'{bonus:+d}'
        self.bonus_label.text = f'Bônus: {self.agility_bonus}'

