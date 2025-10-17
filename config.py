"""
Configurações gerais do BardGame
"""

# Configurações do servidor
SERVER_CONFIG = {
    'host': 'localhost',
    'port': 5000,
    'use_websocket': True,
    'local_only': True  # Mudar para False quando expandir para LAN
}

# Configurações de UI
UI_CONFIG = {
    'default_language': 'pt-BR',
    'theme': 'default',
    'grid_based_layout': True
}

# Paths de arquivos
PATHS = {
    'rules': 'data/rules/',
    'translations': 'data/translations/',
    'user_profiles': 'data/profiles/',
    'world_data': 'data/worlds/',
    'layouts': 'data/layouts/'
}
