---
status: ativo
atualizado: 2026-10-24
descricao: A custódia acompanha o contrato de financiamento de veículo depois de assinado, para o back-office do Banco Exemplo; cliente final e contratação ficam fora.
---
# Visão da área: Custódia de financiamentos

A custódia cuida de tudo o que acontece com o contrato de financiamento de veículo depois da assinatura: parcelas, pagamentos, antecipações, alterações, cancelamento e gravame (registro que prende o veículo ao banco até a quitação). Atende o back-office (equipe interna que opera os contratos) do Banco Exemplo (fictício) pelo portal da custódia.

## Problema
Depois de assinado, o contrato passa a ser acompanhado à mão, em planilha e sistemas soltos. O operador recalcula encargos e saldos manualmente e controla prazos de cabeça. O resultado é cobrança errada, quitação com retrabalho e gravame que fica ativo além do prazo depois da quitação.

## Público
- **Operador:** registra pagamentos, antecipações, alterações e cancelamentos, e consulta o contrato.
- **Supervisor:** faz o que o operador faz e aprova as operações que pedem segunda conferência.

## Objetivos e como medir
| Objetivo | Como medir |
|---|---|
| Baixa do gravame no prazo | Percentual de gravames baixados dentro do prazo após a quitação |
| Encargo cobrado sem erro | Número de cobranças de multa e juros corrigidas depois de lançadas |
| Quitação sem retrabalho | Número de quitações recalculadas depois de informadas ao cliente |

## Módulos
| Módulo | O que cobre | Regras |
|---|---|---|
| Calculadoras | Biblioteca de cálculo: SAC e Price (parcela decrescente e fixa), carência (prazo sem pagar), balão (parcela final maior) e CET (custo efetivo total) | Na primeira feature |
| Contratos | Cadastro e consulta do contrato e do cronograma de parcelas | Na primeira feature |
| Pagamentos | Pagamento de parcela, multa, juros de mora e juros remuneratórios | Na primeira feature |
| Antecipação | Amortização parcial (pagar parte do saldo antes) e quitação | Na primeira feature |
| Alteração de plano | Troca de vencimento e renegociação | Na primeira feature |
| Garantias | Registro e baixa do gravame e alertas de prazo | Na primeira feature |
| Cancelamento | Arrependimento e estorno | Na primeira feature |

## Fora do escopo
- Cliente final: não usa o portal nem recebe comunicação da custódia.
- Simulação e contratação: são de outro time; a custódia recebe o contrato já assinado.
- Financiamento de imóvel e empréstimo pessoal.
