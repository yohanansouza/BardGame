# TODO Atual - Próximas Tarefas a Serem Realizadas

Este arquivo contém os TODOs que devemos estar atuando em breve. Foque em progresso imediato. Consulte `models_todo.md` para a estrutura e processos.

---

## Tarefa: Editor visual de atributos e sistemas

- Descrição:
  - Criar um editor visual que permita editar atributos, níveis, raças e outras entidades via interface gráfica (arrastar/soltar, sliders, tabelas).
- Arquivos alterados / adicionados:
  - `ui/screens/editor_attributes.py` - nova tela planejada
- Status:
  - [ ] Criado
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

## Tarefa: Implementar aba principal (Dashboard)

- Descrição:
  - Criar a aba principal do app com overview de campanhas, personagens ativos e atalhos para funções principais.
- Arquivos alterados / adicionados:
  - `ui/tabs/dashboard.py` - nova aba
- Status:
  - [ ] Criado
  - [ ] Lint/Typecheck
  - [ ] Testes manuais
  - [ ] Correções/Pendências

---

## Tarefa: Implementar aba de Personagens

- Descrição:
  - Aba para visualizar e gerenciar personagens (jogadores e NPCs), com listagem e edição básica.
- Arquivos alterados / adicionados:
  - `ui/tabs/characters.py` - nova aba
- Status:
  - [ ] Criado
  - [ ] Lint/Typecheck
  - [ ] Testes manuais
  - [ ] Correções/Pendências

---

## Tarefa: Implementar aba de Mapa

- Descrição:
  - Aba para exibir mapas de campanha, com navegação básica e tokens posicionáveis.
- Arquivos alterados / adicionados:
  - `ui/tabs/map.py` - nova aba
- Status:
  - [ ] Criado
  - [ ] Lint/Typecheck
  - [ ] Testes manuais
  - [ ] Correções/Pendências

---

## Próximos Passos e Adições

- Revise semanalmente para mover tarefas prontas para `todo_realizados.md`.
- Adicione novas tarefas aqui quando estiverem prontas para implementação imediata, vindas de `todo_escopo.md`.
