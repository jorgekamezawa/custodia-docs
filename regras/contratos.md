---
status: ativo
atualizado: 2026-10-24
descricao: Regras de negócio vigentes de Contratos, sobre o cadastro do contrato assinado, seus dados obrigatórios, o cronograma guardado, a situação das parcelas e o saldo devedor.
---
# Regras de Contratos

Contratos guarda o contrato de financiamento de veículo assinado, com o cronograma e o CET calculados no cadastro. Termos no [glossário](../glossario.md). Prefixo dos identificadores: CON.

## Cadastro

### CON-01: Número do contrato único
O número do contrato é único na custódia; um segundo cadastro com o mesmo número é recusado com "Número do contrato já cadastrado".
- **Exemplo:** com o CTR-0001 cadastrado, um novo cadastro com o número CTR-0001 é recusado.
- **Fonte:** regra fictícia da POC.
- **Origem:** [spec 0005](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0005-cadastro-de-contrato/spec.md).

### CON-02: Dados obrigatórios do cadastro
Cada campo fora da regra é recusado com a mensagem dele.
- **Número do contrato:** 1 a 30 letras, números ou hífen.
- **Nome do cliente e descrição do veículo:** 1 a 120 caracteres.
- **CPF:** 11 dígitos com dígitos verificadores válidos.
- **Chassi:** 17 letras e números, sem I, O e Q.
- **Exemplo:** o CPF 123.456.789-00 é recusado com "CPF inválido"; o 123.456.789-09 é aceito.
- **Fonte:** formato do chassi pelo padrão VIN (ISO 3779); o resto, regra fictícia da POC.
- **Origem:** [spec 0005](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0005-cadastro-de-contrato/spec.md).

### CON-03: Cronograma e CET guardados no cadastro
O cronograma e o CET são calculados no cadastro, pela [CAL-01 a CAL-06](calculadoras.md), e guardados com o contrato, que nasce ativo.
- **Exemplo:** R$ 10.000,00 a 2% ao mês em 12 meses pelo Price: contrato ativo com 12 parcelas (a última de R$ 945,55) e CET de 26,95% ao ano.
- **Fonte:** regra fictícia da POC.
- **Origem:** [spec 0005](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0005-cadastro-de-contrato/spec.md).

### CON-04: Quem cadastrou e quando
O cadastro guarda o usuário que cadastrou e o instante do cadastro.
- **Exemplo:** cadastro feito pelo `operador` às 10h00 de 10/01/2027 guarda os dois.
- **Fonte:** regra fictícia da POC.
- **Origem:** [spec 0005](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0005-cadastro-de-contrato/spec.md).

## Consulta

### CON-05: Situação da parcela não paga
Parcela não paga está "Em aberto" até o dia do vencimento e "Vencida" a partir do dia seguinte. O dia de hoje é a data no horário de Brasília.
- **Exemplo:** em 24/10/2026, a parcela de 10/10/2026 está vencida e as de 24/10/2026 e 10/11/2026 estão em aberto.
- **Fonte:** regra fictícia da POC.
- **Origem:** [spec 0006](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0006-consulta-de-contrato/spec.md).

### CON-06: Saldo devedor
O saldo devedor do contrato é o saldo depois da última parcela paga; sem parcela paga, é o valor financiado.
- **Exemplo:** contrato de R$ 10.000,00 sem parcela paga tem saldo devedor de R$ 10.000,00.
- **Fonte:** regra fictícia da POC.
- **Origem:** [spec 0006](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0006-consulta-de-contrato/spec.md).
