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

Orquestrar o fluxo de execução entre os agentes do sistema.

O Coordinator deverá receber a solicitação do usuário, identificar o dataset e encaminhar a tarefa para os agentes responsáveis.

## Entrada

O Coordinator deverá receber:

```json
{
  "task_id": "string",
  "user_request": "string",
  "dataset_path": "string",
  "context": {}
}

---

# 5. Contrato do Quality Agent

## Responsabilidade

Analisar a qualidade estrutural e semântica do dataset recebido pelo sistema.

O Quality Agent deverá identificar problemas de qualidade de dados antes que o dataset seja encaminhado para análises posteriores.

## Entrada

O Quality Agent deverá receber:

```json
{
  "task_id": "string",
  "dataset_path": "string",
  "context": {}
}

---

# 6. Contrato do Analytics Agent

## Responsabilidade

Executar análises sobre os dados após a validação realizada pelo Quality Agent.

O Analytics Agent deverá utilizar os dados disponíveis e produzir métricas e insights relevantes para a tomada de decisão.

## Entrada

O Analytics Agent deverá receber:

```json
{
  "task_id": "string",
  "dataset_path": "string",
  "quality_report": {},
  "context": {}
}

---

# 7. Contrato do Reviewer Agent

## Responsabilidade

Revisar os resultados produzidos pelos agentes anteriores e verificar sua consistência, qualidade e conformidade com os contratos definidos.

O Reviewer Agent deverá identificar erros, inconsistências ou informações que necessitem de correção antes da entrega final.

## Entrada

O Reviewer Agent deverá receber:

```json
{
  "task_id": "string",
  "quality_report": {},
  "analytics_result": {},
  "context": {}
}