# BardGame - Sistema de RPG Customizável

## Descrição

BardGame é um sistema de RPG completamente customizável que permite aos Game Masters (GMs) criar mundos únicos com suas próprias regras. Desenvolvido com Kivy para ser multiplataforma (Windows, Linux, macOS, Android, iOS).

## Características Principais

### Sistemas Implementados

1. **Atributos** - Sistema de atributos primários e secundários customizáveis
2. **Níveis** - Sistema de progressão com múltiplos tipos de escalamento (linear, exponencial, curva S)
3. **Raças** - Definição de raças com modificadores e habilidades
4. **Proficiências** - Sistema de proficiências para armas, armaduras e perícias
5. **Magia** - Sistemas de spell slots, mana e stamina
6. **Talentos** - Sistema de talentos com pesos e restrições
7. **Moedas** - Sistema econômico com conversão de moedas
8. **Condições** - Status effects e condições aplicáveis
9. **Elementos** - Sistema elemental com interações e resistências
10. **Classe de Armadura** - AC física e mágica
11. **Equipamentos** - Sistema completo de itens com tags e raridades
12. **Línguas** - Sistema de idiomas com criptografia baseada em proficiência

## Estrutura do Projeto

```
BardGame/
├── main.py                 # Aplicação principal
├── config.py              # Configurações gerais
├── requirements.txt       # Dependências
├── core/                  # Lógica central
│   └── world_manager.py   # Gerenciador de mundos
├── models/                # Modelos de dados (todos os sistemas)
│   ├── attributes.py
│   ├── level_system.py
│   ├── races.py
│   ├── proficiency.py
│   ├── magic_system.py
│   ├── talents.py
│   ├── currency.py
│   ├── conditions.py
│   ├── elements.py
│   ├── armor_class.py
│   ├── equipment.py
│   └── languages.py
├── network/               # Sistema de rede
│   ├── server.py         # Servidor WebSocket
│   └── client.py         # Cliente WebSocket
├── ui/                    # Interface do usuário
│   └── screens/          # Telas do aplicativo
├── data/                  # Dados salvos
│   ├── rules/            # Regras dos sistemas
│   ├── translations/     # Traduções (pt-BR)
│   ├── worlds/           # Mundos salvos
│   ├── profiles/         # Perfis de usuários
│   └── layouts/          # Layouts personalizados
└── utils/                 # Utilitários gerais
```

## Instalação

### Requisitos

- Python 3.8 ou superior
- pip

### Passos

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/BardGame.git
cd BardGame
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute o aplicativo:
```bash
python main.py
```

## Uso

### Criando um Novo Mundo

1. Execute o aplicativo
2. Clique em "Novo Mundo"
3. Preencha o nome do mundo e do GM
4. Configure os sistemas de jogo nas abas disponíveis
5. Salve o mundo

### Modo Multiplayer (Local/LAN)

#### Servidor (GM)

```python
from network.server import GameServer

server = GameServer(host='localhost', port=5000)
server.run()
```

#### Cliente (Jogador)

```python
from network.client import GameClient
import asyncio

async def connect():
    client = GameClient(host='localhost', port=5000)
    await client.connect()
    await client.register_as_player("Nome do Jogador")
    await client.receive_messages()

asyncio.run(connect())
```

## Arquitetura de Dados

Todos os sistemas são salvos em arquivos JSON separados por categoria:

- `attributes.json` - Configuração de atributos
- `levels.json` - Sistema de níveis
- `races.json` - Raças disponíveis
- `proficiencies.json` - Proficiências
- `magic.json` - Sistema de magia
- `talents.json` - Talentos
- `currency.json` - Moedas
- `conditions.json` - Condições
- `elements.json` - Elementos
- `armor_class.json` - Classe de armadura
- `equipment.json` - Equipamentos
- `languages.json` - Línguas

## Personalização

### Layout Customizado

O sistema permite que cada usuário personalize seu layout através de um sistema de grid. As posições são salvas localmente em `data/layouts/`.

### Tradução

Para adicionar uma nova língua:

1. Copie `data/translations/pt-BR.json`
2. Renomeie para o código da língua (ex: `en-US.json`)
3. Traduza os valores
4. Atualize a configuração em `config.py`

## Recursos Futuros

- [ ] Editor visual de atributos e sistemas
- [ ] Sistema de combate
- [ ] Gerador de personagens
- [ ] Sistema de inventário com drag-and-drop
- [ ] Mapas e tokens
- [ ] Sistema de chat integrado
- [ ] Rolagem de dados com animações
- [ ] Exportação/Importação de mundos
- [ ] Marketplace de conteúdo
- [ ] Suporte para módulos de terceiros

## Tecnologias Utilizadas

- **Kivy** - Framework de UI multiplataforma
- **WebSockets** - Comunicação em tempo real
- **JSON** - Armazenamento de dados
- **Python AsyncIO** - Operações assíncronas

## Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaFeature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/NovaFeature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## Autores

- Game Master Original - Desenvolvedor Principal

## Agradecimentos

- Comunidade Kivy
- Comunidade de RPG de mesa
- Todos os contribuidores

---

**BardGame** - Crie seus mundos, suas regras, suas aventuras! 🎲✨
