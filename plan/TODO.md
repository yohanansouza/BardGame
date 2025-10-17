# TODO - Arquivo Central de Referência do Projeto BardGame (Agora Organizado por Categorias)

Este arquivo mantém o histórico original das tarefas e serve como referência para a estrutura. As tarefas foram reorganizadas em arquivos categorizados para melhor gestão:

- `models_todo.md`: Modelo e processos para criação de TODOs.
- `todo_atual.md`: Tarefas atuais para implementação imediata.
- `todo_escopo.md`: Escopos de longo prazo para elaboração futura.
- `todo_corrigir.md`: Tarefas que precisam de correção.
- `todo_realizados.md`: Tarefas concluídas.

Consulte `models_todo.md` para instruções atualizadas de uso e template.

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

Use os arquivos categorizados como fonte da verdade para priorização, QA e acompanhamento de pendências. Este arquivo é mantido para histórico.

---

## Tarefas Reorganizadas

As tarefas listadas anteriormente foram movidas para os arquivos categorizados:

- Tarefas atuais (próximas): Ver `todo_atual.md`
- Escopos de longo prazo: Ver `todo_escopo.md`
- Tarefas concluídas: Ver `todo_realizados.md`

Este arquivo mantém o histórico original para referência.

