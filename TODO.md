# TODO - Lista de tarefas do projeto BardGame

Este arquivo centraliza as tarefas, o estado de desenvolvimento e os passos de verificação para cada item implementado no projeto.

Instruções de uso (como preencher cada TODO):

- Cada item deve conter um título curto e uma descrição sucinta do que será feito.
- Campos de status (marcar com [x] quando concluído):
  - [ ] Criado: Implementação básica concluída (código adicionado ao repositório).
  - [ ] Testes automáticos: Existe um teste automatizado que cobre a feature (ou um comando/script para executar testes).
  - [ ] Lint/Typecheck: O código passou nas verificações de lint e tipo (ex.: flake8, pylint, mypy).
  - [ ] Testes manuais: Passos manuais descrevendo como validar a feature em runtime (o que clicar, quais entradas usar).
  - [ ] Correções/Pendências: Caso algo funcione mas precise ajustes visuais/UX/posição, listar aqui com prioridade.

- Para cada item, inclua também: o(s) arquivo(s) modificados, comandos para executar testes (se aplicável), e notas de QA/observações.

Template de item (copie e preencha por tarefa):

## Tarefa: <Título curto da tarefa>

- Descrição:
  - <Descrição detalhada do que a tarefa implementa>
- Arquivos alterados / adicionados:
  - `path/to/file.py` - breve descrição
- Status:
  - [ ] Criado
  - [ ] Testes automáticos
  - [ ] Lint/Typecheck
  - [ ] Testes manuais
  - [ ] Correções/Pendências
- Comandos úteis (ex.: rodar testes, lint):
  - `python -m pytest tests/test_x.py`  # exemplo
  - `flake8 .`  # exemplo
- Passos para testes manuais:
  1. <Passo 1 - iniciar app>
  2. <Passo 2 - navegar até X>
  3. <Passo 3 - validar comportamento Y>

- Notas / Observações:
  - <Qualquer informação adicional>

---

Exemplo preenchido (detector de plataforma):

## Tarefa: Detector de plataforma e configuração da janela

- Descrição:
  - Implementar utilitário de detecção de plataforma (`utils/platform.py`) e adaptar `main.py` para abrir em fullscreen no mobile e em janela resizável no desktop.
- Arquivos alterados / adicionados:
  - `utils/platform.py` - novo arquivo, detecta plataforma e retorna infos.
  - `main.py` - usa `detect_platform()` para configurar `Window.fullscreen` em mobile ou `Window.size` em desktop; adiciona popup de identificação.
- Status:
  - [x] Criado
  - [ ] Testes automáticos
  - [x] Lint/Typecheck
  - [ ] Testes manuais
  - [ ] Correções/Pendências
- Comandos úteis:
  - `python .\main.py`  # iniciar o app Kivy localmente
  - (adicionar testes automatizados no futuro com pytest)
- Passos para testes manuais:
  1. Executar `python .\main.py` em desktop.
  2. Verificar se popup aparece com usuário e plataforma detectada.
  3. Redimensionar a janela e confirmar que conteúdos respondem ao novo tamanho.
  4. (Mobile) Build com Buildozer e confirmar fullscreen no dispositivo/emulador.

- Notas / Observações:
  - Detecção de iOS em Python é limitada; confiar em Kivy para builds iOS ou setar variável de ambiente durante a build.

---

Use este arquivo como fonte da verdade para priorização, QA e acompanhamento de pendências.

---

## Recursos Futuros (importados de `README_PROJETO.md`)

### Tarefa: Editor visual de atributos e sistemas

- Descrição:
  - Criar um editor visual que permita editar atributos, níveis, raças e outras entidades via interface gráfica (arrastar/soltar, sliders, tabelas).
- Arquivos alterados / adicionados:
  - `ui/screens/editor_attributes.py` - nova tela planejada
- Status:
  - [ ] Criado
  - [ ] Testes automáticos
  - [ ] Lint/Typecheck
  - [ ] Testes manuais
  - [ ] Correções/Pendências
- Comandos úteis:
  - `python .\main.py`  # iniciar app
- Passos para testes manuais:
  1. Abrir o app e navegar até Editor de Atributos
  2. Criar/editar um atributo e salvar
  3. Verificar JSON salvo em `data/rules/attributes.json`

### Tarefa: Sistema de combate

- Descrição:
  - Implementar sistema de combate (turn-based ou em tempo real configurável), com cálculo de danos, iniciativas e efeitos.
- Arquivos alterados / adicionados:
  - `models/combat.py` - nova lógica de combate
- Status:
  - [ ] Criado
  - [ ] Testes automáticos
  - [ ] Lint/Typecheck
  - [ ] Testes manuais
  - [ ] Correções/Pendências
- Passos para testes manuais:
  1. Criar dois personagens de teste
  2. Iniciar combate e validar ordem de turnos e resultados

### Tarefa: Gerador de personagens

- Descrição:
  - Ferramenta para gerar personagens (NPCs e jogadores) com seleção de raças, classes, atributos e equipamentos randômicos ou predefinidos.
- Arquivos alterados / adicionados:
  - `ui/screens/char_generator.py`
  - `models/character_generator.py`
- Status:
  - [ ] Criado
  - [ ] Testes automáticos
  - [ ] Lint/Typecheck
  - [ ] Testes manuais
  - [ ] Correções/Pendências

### Tarefa: Sistema de inventário com drag-and-drop

- Descrição:
  - Inventário visual com suporte a arrastar-e-soltar itens, empacotamento, limite de peso/volume e UI responsiva.
- Arquivos alterados / adicionados:
  - `ui/screens/inventory.py`
  - `models/inventory.py`
- Status: 
  - [ ] Criado
  - [ ] Testes automáticos
  - [ ] Lint/Typecheck
  - [ ] Testes manuais
  - [ ] Correções/Pendências

### Tarefa: Mapas e tokens

- Descrição:
  - Implementar sistema de mapas com tokens posicionáveis, camadas e possibilidade de salvar/exportar mapas.
- Arquivos alterados / adicionados:
  - `ui/screens/map_editor.py`
  - `data/maps/` (estrutura de armazenamento)
- Status:
  - [ ] Criado
  - [ ] Testes automáticos
  - [ ] Lint/Typecheck
  - [ ] Testes manuais
  - [ ] Correções/Pendências

### Tarefa: Sistema de chat integrado

- Descrição:
  - Chat para comunicação entre jogadores e GM, integrado com o servidor WebSocket do projeto.
- Arquivos alterados / adicionados:
  - `ui/screens/chat.py`
  - `network/chat_protocol.py`
- Status:
  - [ ] Criado
  - [ ] Testes automáticos
  - [ ] Lint/Typecheck
  - [ ] Testes manuais
  - [ ] Correções/Pendências

### Tarefa: Rolagem de dados com animações

- Descrição:
  - Implementar sistema de rolagem de dados com animações e resultados integrados ao chat e logs de combate.
- Arquivos alterados / adicionados:
  - `ui/widgets/dice_widget.py`
  - `models/dice.py`
- Status:
  - [ ] Criado
  - [ ] Testes automáticos
  - [ ] Lint/Typecheck
  - [ ] Testes manuais
  - [ ] Correções/Pendências

### Tarefa: Exportação/Importação de mundos

- Descrição:
  - Ferramenta para exportar mundos inteiros (JSON + assets) e importar pacotes compartilháveis.
- Arquivos alterados / adicionados:
  - `core/world_export.py`
  - `core/world_import.py`
- Status:
  - [ ] Criado
  - [ ] Testes automáticos
  - [ ] Lint/Typecheck
  - [ ] Testes manuais
  - [ ] Correções/Pendências

### Tarefa: Marketplace de conteúdo

- Descrição:
  - Plataforma para compartilhar conteúdo (módulos, mapas, personagens) entre usuários, com upload/download.
- Arquivos alterados / adicionos:
  - `network/marketplace.py`
  - `ui/screens/marketplace.py`
- Status:
  - [ ] Criado
  - [ ] Testes automáticos
  - [ ] Lint/Typecheck
  - [ ] Testes manuais
  - [ ] Correções/Pendências

### Tarefa: Suporte para módulos de terceiros

- Descrição:
  - API e sistema de plugin para que terceiros possam adicionar módulos ao jogo sem alterar o núcleo.
- Arquivos alterados / adicionados:
  - `core/plugin_system.py`
- Status:
  - [ ] Criado
  - [ ] Testes automáticos
  - [ ] Lint/Typecheck
  - [ ] Testes manuais
  - [ ] Correções/Pendências

