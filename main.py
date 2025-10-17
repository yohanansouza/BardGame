"""
BardGame - Sistema de RPG Customizável
Aplicação principal usando Kivy
"""
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window
import json
import os

from core.world_manager import WorldManager
from config import PATHS

# Plataforma
from utils.platform import detect_platform
from ui.screens.carousel_tabs import CarouselTabs
from ui.screens.attributes_tab import AttributesTab


class MainMenuScreen(Screen):
    """Tela do menu principal"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Título
        title = Label(
            text='BardGame\nSistema de RPG Customizável',
            size_hint=(1, 0.3),
            font_size='24sp'
        )
        layout.add_widget(title)
        
        # Botões do menu
        btn_new_world = Button(text='Novo Mundo', size_hint=(1, 0.15))
        btn_new_world.bind(on_press=self.new_world)
        layout.add_widget(btn_new_world)
        
        btn_load_world = Button(text='Carregar Mundo', size_hint=(1, 0.15))
        btn_load_world.bind(on_press=self.load_world)
        layout.add_widget(btn_load_world)
        
        btn_settings = Button(text='Configurações', size_hint=(1, 0.15))
        btn_settings.bind(on_press=self.settings)
        layout.add_widget(btn_settings)
        
        btn_exit = Button(text='Sair', size_hint=(1, 0.15))
        btn_exit.bind(on_press=self.exit_app)
        layout.add_widget(btn_exit)
        
        self.add_widget(layout)
    
    def new_world(self, instance):
        self.manager.current = 'world_creation'
    
    def load_world(self, instance):
        # TODO: Implementar seleção de mundo
        pass
    
    def settings(self, instance):
        # TODO: Implementar tela de configurações
        pass
    
    def exit_app(self, instance):
        App.get_running_app().stop()


class WorldCreationScreen(Screen):
    """Tela de criação de mundo"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Título
        title = Label(text='Criar Novo Mundo', size_hint=(1, 0.2), font_size='20sp')
        layout.add_widget(title)
        
        # Nome do mundo
        layout.add_widget(Label(text='Nome do Mundo:', size_hint=(1, 0.1)))
        self.world_name_input = TextInput(multiline=False, size_hint=(1, 0.1))
        layout.add_widget(self.world_name_input)
        
        # Nome do GM
        layout.add_widget(Label(text='Nome do Mestre (GM):', size_hint=(1, 0.1)))
        self.gm_name_input = TextInput(multiline=False, size_hint=(1, 0.1))
        layout.add_widget(self.gm_name_input)
        
        # Descrição
        layout.add_widget(Label(text='Descrição:', size_hint=(1, 0.1)))
        self.description_input = TextInput(multiline=True, size_hint=(1, 0.2))
        layout.add_widget(self.description_input)
        
        # Botões
        btn_layout = BoxLayout(size_hint=(1, 0.15), spacing=10)
        
        btn_create = Button(text='Criar')
        btn_create.bind(on_press=self.create_world)
        btn_layout.add_widget(btn_create)
        
        btn_cancel = Button(text='Cancelar')
        btn_cancel.bind(on_press=self.cancel)
        btn_layout.add_widget(btn_cancel)
        
        layout.add_widget(btn_layout)
        self.add_widget(layout)
    
    def create_world(self, instance):
        world_name = self.world_name_input.text or "Novo Mundo"
        gm_name = self.gm_name_input.text or "Game Master"
        description = self.description_input.text
        
        # Criar mundo
        world = WorldManager(world_name, gm_name)
        world.metadata.description = description
        
        # Salvar mundo
        world_path = world.save_world(PATHS['world_data'])
        
        # Armazenar no app
        app = App.get_running_app()
        app.current_world = world
        
        # Ir para tela de edição
        self.manager.current = 'world_editor'
    
    def cancel(self, instance):
        self.manager.current = 'main_menu'


class WorldEditorScreen(Screen):
    """Tela de edição do mundo"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Barra superior
        top_bar = BoxLayout(size_hint=(1, 0.1), spacing=10)
        
        btn_save = Button(text='Salvar')
        btn_save.bind(on_press=self.save_world)
        top_bar.add_widget(btn_save)
        
        btn_back = Button(text='Voltar')
        btn_back.bind(on_press=self.back_to_menu)
        top_bar.add_widget(btn_back)
        
        layout.add_widget(top_bar)
        
        # Área de conteúdo: usar CarouselTabs com abas por sistema
        self.carousel_tabs = CarouselTabs()
        layout.add_widget(self.carousel_tabs)

        # preparar abas (será populado quando a tela for mostrada)
        self._tabs_populated = False

        self.add_widget(layout)
    
    def save_world(self, instance):
        app = App.get_running_app()
        if hasattr(app, 'current_world'):
            app.current_world.save_world(PATHS['world_data'])
            
            popup = Popup(
                title='Sucesso',
                content=Label(text='Mundo salvo com sucesso!'),
                size_hint=(0.6, 0.3)
            )
            popup.open()
    
    def back_to_menu(self, instance):
        self.manager.current = 'main_menu'

    def on_pre_enter(self):
        # Popula as abas na primeira vez que a tela for exibida
        if not getattr(self, '_tabs_populated', False):
            self.populate_tabs()
            self._tabs_populated = True

    def populate_tabs(self):
        """Adiciona as abas para cada setor do sistema ao CarouselTabs.

        Atualmente adiciona:
        - Atributos (usando AttributesTab)
        - Abas placeholder para os outros setores
        """
        # Tentar limpar abas existentes (se houver)
        try:
            # Carousel do Kivy armazena slides em .slides
            slides = getattr(self.carousel_tabs.carousel, 'slides', None)
            if slides:
                for child in list(slides):
                    try:
                        self.carousel_tabs.carousel.remove_widget(child)
                    except Exception:
                        pass
        except Exception:
            pass

        # Aba de Atributos (funcional)
        attr_tab = AttributesTab()
        self.carousel_tabs.add_tab(attr_tab, title='Atributos')

        # Abas placeholder para outros setores
        other_sectors = [
            'Níveis', 'Raças', 'Proficiências', 'Magia', 'Talentos',
            'Moedas', 'Condições', 'Elementos', 'Classe de Armadura',
            'Equipamentos', 'Línguas'
        ]

        for name in other_sectors:
            self.carousel_tabs.add_tab(Label(text=f'{name} - Em desenvolvimento', halign='center'))


class BardGameApp(App):
    """Aplicação principal"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_world: WorldManager = None
    
    def build(self):
        # Detectar plataforma e configurar janela de acordo
        plat_info = detect_platform()
        is_mobile = plat_info.get('is_mobile', False)

        Window.clearcolor = (0.1, 0.1, 0.15, 1)

        if is_mobile:
            # Em mobile abrimos em fullscreen
            try:
                Window.fullscreen = True
            except Exception:
                # fallback para plataforma onde fullscreen não existe
                pass
        else:
            # Desktop: janela padrão resizável
            Window.size = (1024, 768)
            # Kivy permite redimensionamento por padrão em desktop
            try:
                Window.minimum_width = 600
                Window.minimum_height = 400
            except Exception:
                pass
        
        # Criar gerenciador de telas
        sm = ScreenManager()
        
        # Adicionar telas
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(WorldCreationScreen(name='world_creation'))
        sm.add_widget(WorldEditorScreen(name='world_editor'))
        
        return sm

    def on_start(self):
        # Mostrar popup informando a identificação do usuário/plataforma
        try:
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label
            info = detect_platform()
            user = info.get('user', 'desconhecido')
            platform_name = info.get('platform', 'unknown')
            is_mobile = info.get('is_mobile', False)
            text = f"Executando como: {user}\nPlataforma: {platform_name} ({'mobile' if is_mobile else 'desktop'})"
            popup = Popup(title='Identificação', content=Label(text=text), size_hint=(0.6, 0.3))
            popup.open()
        except Exception:
            pass


if __name__ == '__main__':
    BardGameApp().run()
