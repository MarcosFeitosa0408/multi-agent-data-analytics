# Data Dictionary — Sales Dataset

## 1. Objetivo

Este documento descreve a estrutura, o significado e as regras básicas do dataset utilizado pelo Multi-Agent Data Analytics System.

O documento deverá ser utilizado pelos agentes como fonte de contexto para interpretação e validação dos dados.

---

## 2. Dataset

Arquivo:

`sales.csv`

Domínio:

Vendas

Formato:

CSV

Periodicidade:

Diária

---

## 3. Campos

### order_id

Identificador único do pedido.

Tipo esperado:

Integer

Regra:

Cada pedido deve possuir um identificador único.

Não deve ser nulo.

---

### order_date

Data em que o pedido foi realizado.

Tipo esperado:

Date

Formato esperado:

YYYY-MM-DD

Regra:

Não deve ser nulo.

---

### store

Identificação da loja responsável pela venda.

Tipo esperado:

String

Valores esperados inicialmente:

- Loja A
- Loja B
- Loja C

Regra:

Não deve ser nulo.

---

### product

Nome do produto vendido.

Tipo esperado:

String

Regra:

Não deve ser nulo.

---

### category

Categoria do produto.

Tipo esperado:

String

Valores esperados inicialmente:

- Eletrônicos
- Periféricos
- Escritório

Regra:

Não deve ser nulo.

---

### quantity

Quantidade de unidades vendidas.

Tipo esperado:

Integer

Regra:

Deve ser maior que zero.

Não deve ser nulo.

---

### unit_price

Preço unitário do produto.

Tipo esperado:

Decimal

Regra:

Deve ser maior que zero.

Não deve ser nulo.

---

### total_sales

Valor total da venda.

Tipo esperado:

Decimal

Regra:

Deve ser maior ou igual a zero.

Idealmente:

`total_sales = quantity × unit_price`

Quando `quantity` estiver disponível.

---

### customer_state

Estado brasileiro do cliente.

Tipo esperado:

String

Regra:

Não deve ser nulo.

Deve representar uma UF válida.

---

### payment_method

Método utilizado para pagamento.

Tipo esperado:

String

Valores esperados inicialmente:

- PIX
- Cartão
- Boleto

Regra:

Não deve ser nulo.

---

# 4. Regras de Qualidade

O Quality Agent deverá utilizar estas regras durante a avaliação.

## Regra Q01 — Identificador

`order_id` deve ser único.

Se houver duplicidade:

`Q01 = FAILED`

---

## Regra Q02 — Valores ausentes

Campos obrigatórios não devem possuir valores ausentes.

Campos obrigatórios:

- order_id
- order_date
- store
- product
- category
- quantity
- unit_price
- total_sales
- customer_state
- payment_method

---

## Regra Q03 — Quantidade

`quantity` deve ser maior que zero.

Valores menores ou iguais a zero devem ser classificados como inválidos.

---

## Regra Q04 — Preço

`unit_price` deve ser maior que zero.

---

## Regra Q05 — Total da venda

`total_sales` deve ser maior ou igual a zero.

---

## Regra Q06 — Consistência matemática

Quando `quantity` e `unit_price` estiverem disponíveis:

`total_sales` deve corresponder a:

`quantity × unit_price`

Diferenças deverão ser registradas como inconsistências.

---

## Regra Q07 — Data

`order_date` deve possuir formato válido de data.

---

## Regra Q08 — Categoria

`category` deve pertencer ao conjunto de categorias conhecidas.

---

## Regra Q09 — Método de pagamento

`payment_method` deve pertencer ao conjunto de métodos conhecidos.

---

## Regra Q10 — Estado

`customer_state` deve representar uma UF válida.

---

# 5. Severidade

Os problemas encontrados deverão ser classificados em três níveis.

### CRITICAL

Problemas que impedem uma análise confiável.

Exemplos:

- dataset inexistente;
- estrutura inválida;
- ausência de colunas essenciais.

### HIGH

Problemas que podem comprometer significativamente a análise.

Exemplos:

- duplicidades;
- valores inválidos;
- grande quantidade de valores ausentes.

### MEDIUM

Problemas que precisam de atenção, mas não necessariamente impedem a análise.

Exemplos:

- inconsistências menores;
- valores fora do padrão esperado.

---

# 6. Regra de Preservação

O dataset original nunca deverá ser sobrescrito pelos agentes.

Qualquer transformação deverá gerar um novo arquivo.

Original:

`data/sales.csv`

Processado:

`data/processed_sales.csv`

---

# 7. Uso pelos Agentes

O Data Dictionary poderá ser utilizado por:

### Quality Agent

Para validação dos dados.

### Analytics Agent

Para interpretar corretamente as variáveis.

### Reviewer Agent

Para verificar se os resultados respeitam as regras definidas.

### Coordinator Agent

Para fornecer contexto ao fluxo de execução.

---

# 8. Fonte de Verdade

Quando houver conflito entre uma interpretação gerada por um agente e uma regra explicitamente definida neste documento, a regra documentada deverá prevalecer.

Os agentes não devem inventar regras de negócio.

Novas regras deverão ser adicionadas ao documento antes de serem utilizadas como critérios oficiais.
