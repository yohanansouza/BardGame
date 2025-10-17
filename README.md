# BardGame - Kivy Demo

Este pequeno projeto demonstra uma interface simples usando Kivy.

Requisitos

- Python 3.8+ (recomendado 3.10 ou 3.11)

Instalação (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Se você estiver em Windows e tiver problemas com dependências gráficas, instale os pacotes `kivy_deps.sdl2` e `kivy_deps.glew` (já listados no `requirements.txt`).

Executar

```powershell
python main.py
```

Ferramentas úteis

- Se o app não abrir, verifique drivers de vídeo e mesa OpenGL. Em sistemas Windows, instale os drivers da GPU mais recentes.

