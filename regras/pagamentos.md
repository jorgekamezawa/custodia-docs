---
status: ativo
atualizado: 2026-10-24
descricao: Regras de negócio vigentes de Pagamentos, sobre qual parcela pode ser paga, o valor, a data do pagamento, a multa e os juros de mora.
---
# Regras de Pagamentos

Pagamentos registra o pagamento de cada parcela e avisa o contrato por evento. Termos no [glossário](../glossario.md). Prefixo dos identificadores: PAG.

## Pagamento em dia

### PAG-01: Parcela mais antiga primeiro
Só a parcela não paga mais antiga pode ser paga; outra é recusada com "Pague antes a parcela N".
- **Exemplo:** com a parcela 1 em aberto, o pagamento da parcela 2 é recusado com "Pague antes a parcela 1".
- **Fonte:** regra fictícia da POC.
- **Origem:** [spec 0007](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0007-pagamento-em-dia/spec.md).

### PAG-02: Valor devido na data
O valor pago é o valor devido na data: o da parcela, mais a multa (PAG-05) e os juros de mora (PAG-06) quando há atraso.
- **Em dia:** valor diferente é recusado com "Valor deve ser igual ao da parcela: R$ X".
- **Com atraso:** valor diferente é recusado com "Valor deve ser igual ao da parcela com multa e juros de mora: R$ X".
- **Exemplo:** parcela de R$ 945,60 paga 14 dias depois do vencimento deve R$ 968,92.
- **Fonte:** regra fictícia da POC.
- **Origem:** [spec 0007](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0007-pagamento-em-dia/spec.md); alterada pela [spec 0008](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0008-multa-e-juros-de-mora/spec.md).

### PAG-03: Data do pagamento
A data do pagamento fica entre a [data de liberação](../glossario.md) (dia em que o banco entrega o valor financiado) e hoje; fora disso é recusada com "Data do pagamento deve ficar entre a liberação e hoje". Depois do vencimento, o pagamento é aceito com a multa e os juros de mora.
- **Exemplo:** contrato liberado em 10/09/2026 não aceita pagamento datado de 09/09/2026 nem de amanhã.
- **Fonte:** regra fictícia da POC.
- **Origem:** [spec 0007](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0007-pagamento-em-dia/spec.md); alterada pela [spec 0008](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0008-multa-e-juros-de-mora/spec.md).

### PAG-04: Cada parcela paga uma vez
Cada parcela é paga uma vez; um segundo pagamento é recusado com "Parcela já paga".
- **Exemplo:** depois de registrado o pagamento da parcela 1, outro pagamento da parcela 1 é recusado.
- **Fonte:** regra fictícia da POC.
- **Origem:** [spec 0007](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0007-pagamento-em-dia/spec.md).

## Atraso

### PAG-05: Multa de mora
Parcela paga depois do vencimento tem multa de mora de 2% do valor da parcela, cobrada uma vez e arredondada conforme a [GER-01](gerais.md).
- **Exemplo:** parcela de R$ 945,60 paga com qualquer atraso tem multa de R$ 18,91.
- **Fonte:** [CDC, art. 52, §1º](https://www.planalto.gov.br/ccivil_03/leis/l8078compilado.htm), que limita a multa a 2% do valor da prestação.
- **Origem:** [spec 0008](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0008-multa-e-juros-de-mora/spec.md).

### PAG-06: Juros de mora
Parcela paga depois do vencimento tem juros de mora de 1% ao mês, simples, proporcionais aos dias corridos de atraso: valor da parcela × 1% ÷ 30 × dias, arredondados conforme a [GER-01](gerais.md).
- **Exemplo:** parcela de R$ 945,60 com 14 dias de atraso tem R$ 4,41 de juros de mora; com 1 dia, R$ 0,32.
- **Fonte:** regra fictícia da POC.
- **Origem:** [spec 0008](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0008-multa-e-juros-de-mora/spec.md).
