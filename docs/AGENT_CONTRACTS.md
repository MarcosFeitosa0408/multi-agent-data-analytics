# Agent Contracts — Multi-Agent Data Analytics System

## 1. Objetivo

Este documento define os contratos de comunicação entre os agentes do sistema.

Um contrato determina:

- quem envia a informação;
- quem recebe;
- quais dados são obrigatórios;
- qual formato deve ser utilizado;
- quais estados podem ser retornados;
- quais condições determinam sucesso ou falha.

Os agentes deverão depender dos contratos e não da implementação interna de outros agentes.

---

# 2. Princípio de Comunicação

O sistema utilizará mensagens estruturadas.

Fluxo principal:

User
↓
Coordinator
↓
Quality
↓
Analytics
↓
Reviewer
↓
Final Result

Cada etapa deverá produzir uma saída que possa ser utilizada pela etapa seguinte.

---

# 3. Estados Padronizados

Os agentes poderão utilizar os seguintes estados:

### PENDING

A tarefa ainda não foi executada.

### RUNNING

A tarefa está em execução.

### COMPLETED

A tarefa foi executada com sucesso.

### APPROVED

A entrega foi validada e aprovada.

### REJECTED

A entrega foi rejeitada durante a revisão.

### ERROR

Ocorreu um erro durante a execução.

---

# 4. Contrato do Coordinator Agent

## Responsabilidade

Orquestrar o fluxo de execução.

## Entrada

O Coordinator deverá receber:

```json
{
  "task_id": "string",
  "user_request": "string",
  "dataset_path": "string",
  "context": {}
}
