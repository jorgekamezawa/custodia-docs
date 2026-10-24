---
status: ativo
atualizado: 2026-10-24
descricao: Regras de negócio vigentes de Calculadoras, sobre cronograma Price e SAC, vencimentos, CET e limites de entrada.
---
# Regras de Calculadoras

Calculadoras gera o cronograma de parcelas que os outros módulos usam; não guarda nada. Termos no [glossário](../glossario.md). Prefixo dos identificadores: CAL.

## Cronograma Price

### CAL-01: Parcela, juros e amortização na tabela Price
A parcela é `valor financiado × taxa ÷ (1 − (1 + taxa)^−prazo)`, arredondada ao centavo ([GER-01](gerais.md)).
- **Juros remuneratórios:** saldo devedor anterior × taxa, arredondados.
- **Amortização:** parcela menos juros.
- **Última parcela:** amortiza todo o saldo restante, absorvendo a diferença de arredondamento.
- **Taxa zero:** parcela = valor financiado ÷ prazo.
- **Exemplo:** R$ 10.000,00 a 2% ao mês em 12 meses: parcelas 1 a 11 de R$ 945,60 (a primeira com juros de R$ 200,00 e amortização de R$ 745,60) e parcela 12 de R$ 945,55.
- **Origem:** [spec 0001](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0001-cronograma-price/spec.md).

### CAL-02: Vencimentos mensais
O primeiro vencimento é informado; os seguintes caem no mesmo dia dos meses seguintes. Mês sem esse dia usa o último dia do mês, e o mês seguinte volta ao dia original.
- **Exemplo:** primeiro vencimento em 31/01/2027: 31/01/2027, 28/02/2027 e 31/03/2027.
- **Origem:** [spec 0001](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0001-cronograma-price/spec.md).

## Cronograma SAC

### CAL-04: Amortização constante no SAC
A amortização de cada parcela é o valor financiado ÷ prazo, arredondada ao centavo ([GER-01](gerais.md)).
- **Juros remuneratórios:** saldo devedor anterior × taxa, arredondados.
- **Parcela:** amortização mais juros remuneratórios, decrescente.
- **Última parcela:** amortiza todo o saldo restante, absorvendo a diferença de arredondamento.
- **Exemplo:** R$ 10.000,00 a 2% ao mês em 12 meses: amortização de R$ 833,33 nas parcelas 1 a 11 e de R$ 833,37 na 12; parcela 1 de R$ 1.033,33 e parcela 12 de R$ 850,04.
- **Origem:** [spec 0002](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0002-cronograma-sac/spec.md).

## CET

### CAL-05: Custo efetivo total
O CET é a taxa anual que iguala o valor liberado (valor financiado menos os custos pagos antecipadamente) à soma das parcelas descontadas por `(1 + CET)^(dias entre a liberação e o vencimento ÷ 365)`.
- **Expressão:** percentual ao ano, com 2 casas, arredondado conforme a [GER-01](gerais.md).
- **Exemplo:** R$ 10.000,00 a 2% ao mês em 12 meses pelo Price, liberado em 10/01/2027 e com primeiro vencimento em 10/02/2027: CET de 26,95% ao ano; com R$ 300,00 de custos pagos antecipadamente, 34,65%.
- **Fonte:** [Resolução CMN 4.881/2020, art. 4º](https://www.bcb.gov.br/content/estabilidadefinanceira/especialnor/Resolu%C3%A7%C3%A3o4881.pdf).
- **Origem:** [spec 0003](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0003-custo-efetivo-total/spec.md).

## Limites

### CAL-03: Limites de valor, taxa e prazo
Valor financiado de R$ 1.000,00 a R$ 1.000.000,00; taxa de 0% a 10% ao mês, com até 4 casas decimais; prazo de 1 a 72 meses. Fora disso, o cálculo é recusado dizendo qual campo está fora.
- **Exemplo:** prazo de 73 meses é recusado com "Prazo deve estar entre 1 e 72 meses".
- **Fonte:** regra fictícia da POC.
- **Origem:** [spec 0001](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0001-cronograma-price/spec.md).

### CAL-06: Limites do CET
A data de liberação é anterior ao primeiro vencimento, e os custos pagos antecipadamente vão de R$ 0,00 até menos que o valor financiado. Fora disso, o cálculo é recusado dizendo qual campo está fora.
- **Exemplo:** liberação no próprio dia do primeiro vencimento é recusada com "Data de liberação deve ser anterior ao primeiro vencimento".
- **Fonte:** regra fictícia da POC.
- **Origem:** [spec 0003](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0003-custo-efetivo-total/spec.md).
