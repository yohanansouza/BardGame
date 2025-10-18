# Modelos de TODO - Estrutura e Processos

Este arquivo define os modelos e processos para a organização dos TODOs no projeto BardGame. Cada categoria de arquivo TODO tem um propósito específico e deve ser respeitado para manter a consistência e o crescimento progressivo do projeto.

## Estrutura Geral de um TODO

Cada item TODO deve seguir o template abaixo:

### Tarefa: <Título curto da tarefa>

- **Descrição**:
  - <Descrição detalhada do que a tarefa implementa>
- **Arquivos alterados / adicionados**:
  - `path/to/file.py` - breve descrição
- **Status**:
  - [ ] Criado: Implementação básica concluída (código adicionado ao repositório).
  - [ ] Lint/Typecheck: O código passou nas verificações de lint e tipo (ex.: flake8, pylint, mypy). Foca em qualidade de código e detecção de erros estáticos.
  - [ ] Testes manuais: Passos manuais descrevendo como validar a feature em runtime (o que clicar, quais entradas usar).
  - [ ] Correções/Pendências: Caso algo funcione mas precise ajustes visuais/UX/posição, listar aqui com prioridade.
- **Comandos úteis** (ex.: rodar testes, lint):
  - `python -m pytest tests/test_x.py`  # exemplo
  - `flake8 .`  # exemplo
- **Passos para testes manuais**:
  1. <Passo 1 - iniciar app>
  2. <Passo 2 - navegar até X>
  3. <Passo 3 - validar comportamento Y>
- **Notas / Observações**:
  - <Qualquer informação adicional>

---

## Processos por Arquivo TODO

### models_todo.md
- **Propósito**: Este arquivo é o modelo central. Define a estrutura padrão para todos os TODOs e explica como cada categoria de arquivo deve operar. Deve ser consultado sempre que um novo TODO for criado ou movido entre categorias.
- **Como atuar**: Mantenha atualizado com melhorias nos processos. Adicione seções para novos tipos de categorias se necessário. Este arquivo não contém tarefas específicas, apenas definições.

### todo_atual.md
- **Propósito**: Contém os TODOs que devemos estar atuando em breve. São as próximas tarefas a serem realizadas, priorizando o progresso imediato do projeto.
- **Como atuar**: Foque em tarefas curtas a médias prazo (próximas semanas/meses). Mova tarefas aqui quando estiverem prontas para implementação. Atualize status regularmente. Quando concluída, mova para `todo_realizados.md`. Se uma tarefa evoluir para algo mais complexo, mova para `todo_escopo.md` para elaboração.

### todo_escopo.md
- **Propósito**: Contém os escopos que iremos elaborar e preparar o terreno para aplicação futura. São TODOs modulados e elaborados, mas ainda não prontos para execução imediata.
- **Como atuar**: Inclua tarefas de longo prazo ou que precisam de planejamento detalhado antes de implementação. Refine descrições, divida em subtarefas se necessário. Quando o escopo estiver maduro e pronto para ação, mova para `todo_atual.md`. Permite adequar processos sem remendos entre eles.

### todo_corrigir.md
- **Propósito**: Trata dos TODOs que foram quebrados, alterados sem necessidade, ou que têm pendências críticas que impedem o progresso.
- **Como atuar**: Liste aqui tarefas que precisam de correção urgente. Priorize correções sobre novas implementações. Quando corrigido, mova de volta para a categoria apropriada (`todo_atual.md` ou `todo_escopo.md`) ou para `todo_realizados.md` se aplicável.

### todo_realizados.md
- **Propósito**: Contém os escopos já atuando, aplicados e feitos dentro dos conformes. Registra o histórico de conquistas.
- **Como atuar**: Adicione tarefas concluídas aqui. Use como referência para QA e validação. Mantenha atualizado para acompanhar o progresso geral. Não edite tarefas aqui, apenas adicione novas concluídas.

## Crescimento Progressivo

Para manter o sistema crescendo:
- **Adicionar Novos TODOs**: Sempre comece adicionando em `todo_escopo.md` para elaboração inicial, depois mova para `todo_atual.md` quando pronto.
- **Revisão Periódica**: Semanalmente, revise todos os arquivos para mover tarefas entre categorias conforme o progresso.
- **Expansão de Categorias**: Se surgirem novas necessidades, adicione seções neste arquivo e crie novos arquivos TODO conforme necessário.
- **Integração**: Assegure que tarefas em `todo_atual.md` sejam compatíveis com escopos em `todo_escopo.md` para evitar conflitos.

Este modelo garante que o projeto evolua de forma organizada, evitando retrabalho e mantendo foco no progresso incremental.
