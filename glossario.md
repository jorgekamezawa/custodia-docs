---
status: ativo
atualizado: 2026-10-24
descricao: Termos da custódia de financiamentos, com definição única e o nome usado no código.
---
# Glossário

| Termo | Nome no código | Definição | Módulo |
|---|---|---|---|
| Amortização parcial | `PartialPrepayment` | Pagamento antecipado de parte do saldo devedor, que reduz o valor ou o número das parcelas restantes. | Antecipação |
| Arrependimento | `Withdrawal` | Desistência do contrato pelo cliente logo após a assinatura, que desfaz o financiamento. | Cancelamento |
| Baixa do gravame | `LienRelease` | Retirada do gravame do veículo depois da quitação, que libera o veículo para o dono. | Garantias |
| Balão | `BalloonPayment` | Parcela final maior que as demais, combinada no contrato. | Calculadoras |
| Carência | `GracePeriod` | Prazo no início do contrato em que o cliente não paga parcela. | Calculadoras |
| CET | `TotalEffectiveCost` | Custo efetivo total: taxa que soma juros, tarifas e impostos do contrato, ao ano. | Calculadoras |
| Chassi | `chassisNumber` | Número de identificação único do veículo; é a chave do gravame. | Garantias |
| Contrato | `Contract` | Financiamento de veículo já assinado que a custódia acompanha até o fim. | Contratos |
| Custos pagos antecipadamente | `upfrontCosts` | Tarifas, tributos e seguros pagos na contratação, fora das parcelas; reduzem o valor liberado no cálculo do CET. | Calculadoras |
| Cronograma | `InstallmentSchedule` | Lista das parcelas do contrato, com vencimento e valores de cada uma. | Contratos |
| Data de liberação | `releaseDate` | Dia em que o banco entrega o valor financiado ao cliente; marco inicial do CET e limite mais antigo de um pagamento. | Contratos |
| Estorno | `Refund` | Devolução ao cliente de valor já pago. | Cancelamento |
| Gravame | `Lien` | Registro que prende o veículo ao banco como garantia até a quitação. | Garantias |
| Juros de mora | `DefaultInterest` | Juros cobrados por dia de atraso de uma parcela. | Pagamentos |
| Juros remuneratórios | `RemunerativeInterest` | Juros do financiamento, previstos no contrato, que remuneram o banco pelo empréstimo. | Pagamentos |
| Multa | `LateFee` | Valor único cobrado sobre a parcela paga depois do vencimento. | Pagamentos |
| Operador | `OPERATOR` | Perfil do back-office que registra operações e consulta contratos no portal. | Todos |
| Parcela | `Installment` | Cada pagamento previsto no cronograma, formado por amortização e juros. | Contratos |
| Price | `AmortizationSystem.PRICE` | Sistema de amortização em que todas as parcelas têm o mesmo valor. | Calculadoras |
| Quitação | `Payoff` | Pagamento de todo o saldo devedor, que encerra o contrato. | Antecipação |
| Renegociação | `Renegotiation` | Mudança de prazo, taxa ou valor das parcelas restantes de um contrato. | Alteração de plano |
| SAC | `AmortizationSystem.SAC` | Sistema de amortização constante: a amortização é igual em todas as parcelas e a parcela diminui com o tempo. | Calculadoras |
| Saldo devedor | `OutstandingBalance` | Quanto do valor financiado ainda falta pagar, sem os juros futuros. | Contratos |
| SNG | `LienRegistry` | Sistema Nacional de Gravames, onde o gravame é registrado e baixado; na POC é simulado. | Garantias |
| Supervisor | `SUPERVISOR` | Perfil do back-office que faz o que o operador faz e aprova operações que pedem segunda conferência. | Todos |
| Valor liberado | `releasedAmount` | Valor financiado menos os custos pagos antecipadamente: o que o cliente efetivamente recebe. | Calculadoras |
| Troca de vencimento | `DueDateChange` | Mudança do dia de vencimento das parcelas restantes. | Alteração de plano |
