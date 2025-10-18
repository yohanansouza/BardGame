# TODO Realizados - Tarefas Concluídas

Este arquivo registra os escopos já atuando, aplicados e feitos dentro dos conformes, ou seja, com TODOS os status marcados como [x]. Consulte `models_todo.md` para a estrutura padrão de TODOs.

---

## Tarefa: Detector de plataforma e configuração da janela

- Descrição:
  - Implementar utilitário de detecção de plataforma (`utils/platform.py`) e adaptar `main.py` para abrir em fullscreen no mobile e em janela resizável no desktop.
- Arquivos alterados / adicionados:
  - `utils/platform.py` - novo arquivo, detecta plataforma e retorna infos.
  - `main.py` - usa `detect_platform()` para configurar `Window.fullscreen` em mobile ou `Window.size` em desktop; adiciona popup de identificação.
- Status:
  - [x] Criado
  - [x] Lint/Typecheck
  - [x] Testes manuais
  - [x] Correções/Pendências
- Comandos úteis:
  - `python .\main.py`  # iniciar o app Kivy localmente
- Passos para testes manuais:
  1. Executar `python .\main.py` em desktop.
  2. Verificar se popup aparece com usuário e plataforma detectada.
  3. Redimensionar a janela e confirmar que conteúdos respondem ao novo tamanho.
  4. (Mobile) Build com Buildozer e confirmar fullscreen no dispositivo/emulador.

- Notas / Observações:
  - Detecção de iOS em Python é limitada; confiar em Kivy para builds iOS ou setar variável de ambiente durante a build.
  - Testes manuais efetuados e funcionando corretamente em desktop/Android. Testes em iOS não realizados devido à falta de setup do sistema para teste.

---

Quando uma tarefa for totalmente concluída (todos os status marcados com [x]), mova-a para este arquivo para registrar o progresso.
