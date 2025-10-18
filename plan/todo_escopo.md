# TODO Escopo - Tarefas para Elaboração Futura

Este arquivo contém os escopos que iremos elaborar e preparar o terreno para aplicação futura. São TODOs modulados para longo prazo. Consulte `models_todo.md` para a estrutura e processos.

---

## Tarefa: Mapas e tokens

- Descrição:
  - Implementar sistema de mapas com tokens posicionáveis, camadas e possibilidade de salvar/exportar mapas.
- Arquivos alterados / adicionados:
  - `ui/screens/map_editor.py`
  - `data/maps/` (estrutura de armazenamento)
- Status:
  - [ ] Criado
  - [ ] Lint/Typecheck
  - [ ] Testes manuais
  - [ ] Correções/Pendências

---

## Tarefa: Sistema de chat integrado

- Descrição:
  - Chat para comunicação entre jogadores e GM, integrado com o servidor WebSocket do projeto.
- Arquivos alterados / adicionados:
  - `ui/screens/chat.py`
  - `network/chat_protocol.py`
- Status:
  - [ ] Criado
  - [ ] Lint/Typecheck
  - [ ] Testes manuais
  - [ ] Correções/Pendências

---

## Tarefa: Rolagem de dados com animações

- Descrição:
  - Implementar sistema de rolagem de dados com animações e resultados integrados ao chat e logs de combate.
- Arquivos alterados / adicionados:
  - `ui/widgets/dice_widget.py`
  - `models/dice.py`
- Status:
  - [ ] Criado
  - [ ] Lint/Typecheck
  - [ ] Testes manuais
  - [ ] Correções/Pendências

---

## Tarefa: Exportação/Importação de mundos

- Descrição:
  - Ferramenta para exportar mundos inteiros (JSON + assets) e importar pacotes compartilháveis.
- Arquivos alterados / adicionados:
  - `core/world_export.py`
  - `core/world_import.py`
- Status:
  - [ ] Criado
  - [ ] Lint/Typecheck
  - [ ] Testes manuais
  - [ ] Correções/Pendências

---

## Tarefa: Marketplace de conteúdo

- Descrição:
  - Plataforma para compartilhar conteúdo (módulos, mapas, personagens) entre usuários, com upload/download.
- Arquivos alterados / adicionos:
  - `network/marketplace.py`
  - `ui/screens/marketplace.py`
- Status:
  - [ ] Criado
  - [ ] Lint/Typecheck
  - [ ] Testes manuais
  - [ ] Correções/Pendências

---

## Tarefa: Suporte para módulos de terceiros

- Descrição:
  - API e sistema de plugin para que terceiros possam adicionar módulos ao jogo sem alterar o núcleo.
- Arquivos alterados / adicionados:
  - `core/plugin_system.py`
- Status:
  - [ ] Criado
  - [ ] Lint/Typecheck
  - [ ] Testes manuais
  - [ ] Correções/Pendências

---

## Tarefa: Sistema de combate

- Descrição:
  - Implementar sistema de combate (turn-based ou em tempo real configurável), com cálculo de danos, iniciativas e efeitos.
- Arquivos alterados / adicionados:
  - `models/combat.py` - nova lógica de combate
- Status:
  - [ ] Criado
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
  - [ ] Lint/Typecheck
  - [ ] Testes manuais
  - [ ] Correções/Pendências

---

- Refine descrições e divida em subtarefas conforme necessário.
- Quando um escopo estiver maduro e pronto para ação, mova para `todo_atual.md`.
- Adicione novos escopos de longo prazo aqui para planejamento avançado.
