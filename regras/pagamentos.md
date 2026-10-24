---
status: ativo
atualizado: 2026-10-24
descricao: Regras de negócio vigentes de Pagamentos, sobre qual parcela pode ser paga, o valor e a data do pagamento.
---
# Regras de Pagamentos

Pagamentos registra o pagamento de cada parcela e avisa o contrato por evento. Termos no [glossário](../glossario.md). Prefixo dos identificadores: PAG.

## Pagamento em dia

### PAG-01: Parcela mais antiga primeiro
Só a parcela não paga mais antiga pode ser paga; outra é recusada com "Pague antes a parcela N".
- **Exemplo:** com a parcela 1 em aberto, o pagamento da parcela 2 é recusado com "Pague antes a parcela 1".
- **Fonte:** regra fictícia da POC.
- **Origem:** [spec 0007](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0007-pagamento-em-dia/spec.md).

### PAG-02: Valor igual ao da parcela
O valor pago é igual ao valor da parcela; outro é recusado com "Valor deve ser igual ao da parcela: R$ X".
- **Exemplo:** R$ 945,59 na parcela de R$ 945,60 é recusado com "Valor deve ser igual ao da parcela: R$ 945,60".
- **Fonte:** regra fictícia da POC.
- **Origem:** [spec 0007](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0007-pagamento-em-dia/spec.md).

### PAG-03: Data do pagamento
A data do pagamento fica entre a [data de liberação](../glossario.md) (dia em que o banco entrega o valor financiado) e hoje e não passa do vencimento da parcela.
- **Fora do intervalo:** antes da liberação ou depois de hoje, recusada com "Data do pagamento deve ficar entre a liberação e hoje".
- **Depois do vencimento:** recusada com "Pagamento depois do vencimento ainda não pode ser registrado".
- **Exemplo:** parcela que vence em 10/11/2026 pode ser paga até 10/11/2026; em 11/11/2026 é recusada.
- **Fonte:** regra fictícia da POC.
- **Origem:** [spec 0007](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0007-pagamento-em-dia/spec.md).

### PAG-04: Cada parcela paga uma vez
Cada parcela é paga uma vez; um segundo pagamento é recusado com "Parcela já paga".
- **Exemplo:** depois de registrado o pagamento da parcela 1, outro pagamento da parcela 1 é recusado.
- **Fonte:** regra fictícia da POC.
- **Origem:** [spec 0007](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0007-pagamento-em-dia/spec.md).
