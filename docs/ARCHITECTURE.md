# Architecture — Multi-Agent Data Analytics System

## 1. Visão Geral

O Multi-Agent Data Analytics System utiliza uma arquitetura multiagente baseada em especialização de responsabilidades.

Cada agente possui uma função operacional específica, ferramentas controladas, entradas e saídas definidas e critérios próprios de execução.

Um agente coordenador será responsável por controlar o fluxo geral e garantir que as entregas sejam encaminhadas corretamente entre os especialistas.

---

## 2. Arquitetura Inicial

O fluxo principal será:

Usuário
↓
Coordinator Agent
↓
Quality Agent
↓
Analytics Agent
↓
Reviewer Agent
↓
Resultado Final

O Coordinator Agent será responsável pela orquestração do fluxo.

---

## 3. Componentes

### 3.1 Usuário

O usuário fornece:

- objetivo da análise;
- dataset;
- contexto adicional;
- regras de negócio, quando disponíveis.

O usuário também poderá participar de decisões críticas por meio do Human-in-the-Loop em versões futuras.

---

### 3.2 Coordinator Agent

O Coordinator Agent funciona como o orquestrador do sistema.

#### Responsabilidades

- receber a missão;
- interpretar o objetivo;
- identificar as etapas necessárias;
- acionar os agentes especializados;
- encaminhar informações entre agentes;
- verificar resultados;
- controlar erros;
- solicitar novas execuções;
- finalizar o processo.

#### Não deve

- concentrar todas as tarefas de análise;
- substituir os agentes especialistas;
- alterar diretamente os resultados sem justificativa;
- aprovar sozinho uma entrega que exige revisão.

---

### 3.3 Quality Agent

O Quality Agent é responsável pela avaliação da qualidade do dataset.

#### Responsabilidades

- carregar o dataset;
- verificar estrutura;
- verificar tipos de dados;
- identificar valores ausentes;
- identificar duplicidades;
- identificar inconsistências;
- executar regras de validação;
- calcular métricas de qualidade;
- gerar relatório estruturado.

#### Entrada

- dataset;
- data dictionary, quando disponível;
- regras de negócio, quando disponíveis.

#### Saída

Quality Report estruturado.

---

### 3.4 Analytics Agent

O Analytics Agent é responsável pela análise dos dados.

#### Responsabilidades

- realizar análise exploratória;
- calcular estatísticas;
- identificar tendências;
- identificar padrões;
- calcular métricas;
- analisar relações entre variáveis;
- produzir resultados analíticos.

#### Entrada

- dataset;
- Quality Report.

#### Saída

Analysis Report estruturado.

---

### 3.5 Reviewer Agent

O Reviewer Agent funciona como camada independente de validação.

#### Responsabilidades

- revisar resultados;
- verificar consistência;
- verificar critérios definidos;
- comparar resultados com os dados;
- identificar erros;
- identificar conclusões sem evidência;
- aprovar ou rejeitar a entrega.

#### Entrada

- Quality Report;
- Analysis Report;
- critérios de validação.

#### Saída

Review Report.

O resultado deverá possuir um status:

- APPROVED
- REJECTED

---

## 4. Fluxo de Comunicação

O fluxo inicial será sequencial.

### Etapa 1

O usuário envia a missão ao Coordinator Agent.

### Etapa 2

O Coordinator envia o dataset ao Quality Agent.

### Etapa 3

O Quality Agent executa a avaliação.

### Etapa 4

O Quality Agent devolve o Quality Report.

### Etapa 5

O Coordinator verifica o resultado.

### Etapa 6

Se os dados forem considerados adequados, o Coordinator encaminha o trabalho ao Analytics Agent.

### Etapa 7

O Analytics Agent executa a análise.

### Etapa 8

O Analytics Agent devolve o Analysis Report.

### Etapa 9

O Coordinator envia os resultados ao Reviewer Agent.

### Etapa 10

O Reviewer Agent valida a entrega.

### Etapa 11

Se aprovado, o processo continua para o resultado final.

### Etapa 12

Se rejeitado, o Coordinator identifica a etapa que precisa ser corrigida e solicita uma nova execução.

---

## 5. Fluxo de Aprovação

O processo seguirá o seguinte padrão:

Dataset
↓
Quality
↓
Quality Validation
↓
Analytics
↓
Review
↓
Approval
↓
Final Result

Caso a revisão seja rejeitada:

Review
↓
REJECTED
↓
Coordinator
↓
Correction
↓
New Review

O fluxo somente será finalizado após uma entrega considerada válida.

---

## 6. Contratos entre Agentes

Os agentes não devem depender da implementação interna uns dos outros.

A comunicação será realizada por meio de estruturas de dados padronizadas.

Exemplo:

```json
{
  "status": "APPROVED",
  "agent": "quality_agent",
  "dataset": "sales.csv",
  "metrics": {
    "rows": 1000,
    "columns": 12,
    "missing_values": 23,
    "duplicates": 4
  },
  "quality_score": 96.5
}
