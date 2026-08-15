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
```
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
```
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
```
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
```
---

# 8. Contrato do Final Result

## Responsabilidade

Consolidar os resultados produzidos pelos agentes do sistema e apresentar uma resposta final ao usuário.

O Final Result deverá utilizar os resultados validados pelo Reviewer Agent para produzir uma resposta estruturada, clara e rastreável.

## Entrada

O Final Result deverá receber:

```json
{
  "task_id": "string",
  "quality_report": {},
  "analytics_result": {},
  "review_result": {}
}
```
---

# 9. Regras Gerais dos Contratos

Todos os agentes deverão seguir as regras gerais definidas neste documento.

## Comunicação

Os agentes deverão utilizar mensagens estruturadas para comunicação entre as etapas do sistema.

Cada mensagem deverá possuir os campos necessários para que o próximo agente possa executar sua responsabilidade sem depender da implementação interna do agente anterior.

## Identificação da execução

Toda execução deverá possuir um `task_id` único.

O `task_id` deverá ser preservado durante todo o fluxo de processamento.

## Estados

Os agentes deverão utilizar somente os estados definidos neste contrato:

- `PENDING`
- `RUNNING`
- `COMPLETED`
- `APPROVED`
- `REJECTED`
- `ERROR`

## Tratamento de erros

Os erros deverão ser retornados de forma estruturada.

Sempre que possível, o erro deverá informar:

- tipo do erro;
- mensagem do erro;
- agente responsável;
- `task_id` da execução.

## Independência entre agentes

Os agentes deverão depender dos contratos definidos neste documento e não da implementação interna de outros agentes.

Um agente não deverá acessar diretamente funções, variáveis ou estruturas internas de outro agente.

## Rastreabilidade

Cada etapa deverá preservar informações suficientes para permitir o rastreamento da execução.

O fluxo deverá manter o seguinte identificador:

`task_id`

Esse identificador deverá acompanhar a execução desde o Coordinator até o Final Result.

## Compatibilidade

Alterações nos contratos deverão preservar a compatibilidade com os agentes existentes sempre que possível.

Alterações incompatíveis deverão ser documentadas e acompanhadas das respectivas alterações nos testes.

## Persistência de artefatos

Arquivos gerados automaticamente durante a execução deverão ser tratados como artefatos de execução.

Exemplos:

- `outputs/quality_report.json`
- `outputs/analytics_report.json`

Esses arquivos não deverão ser versionados no Git quando estiverem configurados como arquivos gerados automaticamente.

## Validação

Toda alteração relevante nos contratos deverá ser acompanhada por testes que verifiquem:

1. Estrutura das mensagens.
2. Campos obrigatórios.
3. Estados permitidos.
4. Tratamento de erros.
5. Compatibilidade entre os agentes.

---

# 10. Rastreabilidade da Execução

## Objetivo

Garantir que cada execução do sistema possa ser identificada e acompanhada desde a solicitação inicial do usuário até o resultado final.

## Identificador da execução

Cada execução deverá possuir um `task_id` único.

Exemplo:

```text
task_001
```
---

# 11. Versionamento dos Contratos

## Objetivo

Garantir que alterações nos contratos de comunicação entre os agentes sejam controladas, documentadas e rastreáveis.

## Princípio

Os contratos fazem parte da arquitetura do sistema e qualquer alteração relevante deverá ser registrada no controle de versão.

## Alterações compatíveis

Alterações compatíveis são aquelas que não quebram os agentes existentes.

Exemplos:

- adicionar um campo opcional;
- adicionar uma nova regra de validação;
- adicionar novos tipos de insight;
- adicionar informações complementares ao resultado.

Alterações compatíveis poderão ser realizadas mantendo a versão atual do contrato.

## Alterações incompatíveis

Alterações incompatíveis são aquelas que podem impedir o funcionamento dos agentes existentes.

Exemplos:

- remover um campo obrigatório;
- alterar o nome de um campo obrigatório;
- alterar o tipo de um campo existente;
- alterar a estrutura principal de uma mensagem;
- alterar um estado utilizado pelo sistema.

Alterações incompatíveis deverão ser avaliadas antes de serem implementadas.

## Registro das alterações

Toda alteração relevante deverá ser registrada no Git por meio de um commit descritivo.

Exemplo:

```text
docs: update analytics agent contract
```
---

# 12. Compatibilidade entre Agentes

## Objetivo

Definir regras para garantir que os agentes consigam consumir corretamente as mensagens produzidas pelas etapas anteriores do sistema.

## Contratos como interface

Cada contrato deverá ser tratado como uma interface de comunicação entre os agentes.

O agente consumidor não deverá depender da implementação interna do agente produtor.

A comunicação deverá ocorrer exclusivamente por meio dos dados definidos no contrato.

## Compatibilidade de entrada

Antes de executar uma tarefa, o agente deverá verificar se os campos obrigatórios da mensagem de entrada estão disponíveis.

Caso algum campo obrigatório esteja ausente, o agente deverá retornar um erro estruturado.

Exemplo:

```json
{
  "agent": "quality_agent",
  "status": "ERROR",
  "task_id": "string",
  "dataset": "string",
  "error": {
    "type": "INVALID_INPUT",
    "message": "Campo obrigatório ausente."
  }
}
```
---

# 13. Fluxo de Execução Completo

## Objetivo

Definir o fluxo completo de processamento do sistema Multi-Agent Data Analytics, desde a solicitação do usuário até a geração do resultado final.

## Etapa 1 — User

O usuário deverá fornecer uma solicitação contendo a tarefa que deseja executar e, quando aplicável, o dataset que deverá ser analisado.

## Etapa 2 — Coordinator Agent

O Coordinator Agent deverá:

1. Receber a solicitação do usuário.
2. Criar o `task_id`.
3. Identificar o dataset.
4. Preparar o contexto da execução.
5. Encaminhar a tarefa para o Quality Agent.

## Etapa 3 — Quality Agent

O Quality Agent deverá:

1. Receber o dataset.
2. Executar as regras de qualidade.
3. Calcular o `quality_score`.
4. Registrar os problemas encontrados.
5. Produzir o `quality_report`.
6. Encaminhar o resultado para o Analytics Agent.

## Etapa 4 — Analytics Agent

O Analytics Agent deverá:

1. Receber o dataset.
2. Receber o resultado do Quality Agent.
3. Executar as análises.
4. Calcular as métricas.
5. Identificar padrões e tendências.
6. Produzir os insights.
7. Encaminhar os resultados para o Reviewer Agent.

## Etapa 5 — Reviewer Agent

O Reviewer Agent deverá:

1. Receber os resultados do Quality Agent e Analytics Agent.
2. Validar a consistência dos resultados.
3. Identificar possíveis inconsistências.
4. Aprovar ou rejeitar a entrega.
5. Retornar `APPROVED`, `REJECTED` ou `ERROR`.

## Etapa 6 — Final Result

O Final Result deverá:

1. Receber os resultados validados.
2. Verificar o status do Reviewer Agent.
3. Consolidar os resultados.
4. Produzir a resposta final.
5. Preservar o `task_id`.

## Fluxo principal

```text
User
  ↓
Coordinator Agent
  ↓
Quality Agent
  ↓
Analytics Agent
  ↓
Reviewer Agent
  ↓
Final Result
```
---

# 14. Contrato de Contexto

## Objetivo

Definir como informações de contexto deverão ser transportadas entre os agentes durante uma execução.

O contexto deverá permitir que os agentes compartilhem informações necessárias para executar suas responsabilidades sem depender diretamente da implementação interna de outros agentes.

## Estrutura

O campo `context` poderá conter informações adicionais relacionadas à execução.

Exemplo:

```json
{
  "task_id": "task_001",
  "context": {
    "source": "user",
    "environment": "development"
  }
}
```
---

# 15. Contrato de Persistência de Resultados

## Objetivo

Definir como os resultados produzidos pelos agentes poderão ser persistidos como artefatos de execução.

A persistência deverá permitir que os resultados sejam reutilizados, auditados e analisados posteriormente.

## Diretório de saída

Os artefatos gerados durante as execuções deverão ser armazenados no diretório:

`outputs/`

## Quality Report

O resultado produzido pelo Quality Agent poderá ser armazenado em:

`outputs/quality_report.json`

Estrutura esperada:

```json
{
  "agent": "quality_agent",
  "status": "COMPLETED",
  "task_id": "string",
  "dataset": "string",
  "rows": 0,
  "columns": 0,
  "quality_score": 0.0,
  "issues": []
}
```
---

