# BardGame - Kivy Demo

Este pequeno projeto demonstra uma interface simples usando Kivy.

Requisitos

- Python 3.8+ (recomendado 3.10 ou 3.11)

Instalação (Windows PowerShell)

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

Se você estiver em Windows e tiver problemas com dependências gráficas, instale os pacotes `kivy_deps.sdl2` e `kivy_deps.glew` (já listados no `requirements.txt`).

## Estrutura do Projeto

```
BardGame/
├── src/                    # Código-fonte principal
│   ├── core/               # Lógica central do sistema
│   ├── data/               # Dados e configurações
│   ├── models/             # Modelos de dados
│   ├── network/            # Componentes de rede
│   ├── plan/               # Documentação e planejamento
│   │   └── TODO.md         # Lista de tarefas e planejamento
│   ├── ui/                 # Interface do usuário
│   └── utils/              # Utilitários diversos
├── .gitignore
├── README.md               # Este arquivo
├── main.py                 # Ponto de entrada principal
└── requirements.txt        # Dependências do projeto
```

## Executar

```powershell
python main.py
```

Ferramentas úteis

- Se o app não abrir, verifique drivers de vídeo e mesa OpenGL. Em sistemas Windows, instale os drivers da GPU mais recentes.

