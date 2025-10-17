# TODO Atual - Próximas Tarefas a Serem Realizadas

Este arquivo contém os TODOs que devemos estar atuando em breve. Foque em progresso imediato. Consulte `models_todo.md` para a estrutura e processos.

---

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

## Tarefa: Editor visual de atributos e sistemas

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

---

## Tarefa: Sistema de combate

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

---

## Tarefa: Gerador de personagens

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

---

## Tarefa: Sistema de inventário com drag-and-drop

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

---

## Próximos Passos e Adições

- Revise semanalmente para mover tarefas prontas para `todo_realizados.md`.
- Adicione novas tarefas aqui quando estiverem prontas para implementação imediata, vindas de `todo_escopo.md`.
