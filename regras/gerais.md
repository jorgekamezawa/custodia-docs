---
status: ativo
atualizado: 2026-10-24
descricao: Regras de negócio vigentes que valem para todos os módulos da custódia, sobre arredondamento de valores, unicidade do gravame por chassi e acesso ao portal.
---
# Regras gerais

Regras que valem para qualquer módulo da custódia; a regra de um módulo só, mesmo que pareça geral, mora na página do módulo. Termos como gravame, baixa do gravame e chassi estão no [glossário](../glossario.md). Prefixo dos identificadores: GER.

## Valores em dinheiro

### GER-01: Arredondamento de valores em reais
Todo valor em reais é guardado e exibido com 2 casas decimais. Resultado de cálculo com mais casas é arredondado pelo método do banqueiro (meio para o par): o 5 exato vai para o dígito par mais próximo.
- **Exemplo:** juros calculados de R$ 10,125 viram R$ 10,12; de R$ 10,135 viram R$ 10,14; de R$ 10,1251 viram R$ 10,13.
- **Fonte:** regra fictícia da POC.
- **Origem:** discovery da área, sem spec.

## Gravame

### GER-02: Um gravame ativo por chassi
Um chassi não pode ter dois gravames ativos ao mesmo tempo. Um novo gravame para o mesmo chassi só é aceito depois da baixa do anterior.
- **Exemplo:** o chassi 9BWZZZ377VT004251 tem gravame ativo do contrato 1001; o registro de gravame do contrato 1002 para o mesmo chassi é recusado até a baixa do gravame do contrato 1001.
- **Fonte:** regra fictícia da POC.
- **Origem:** discovery da área, sem spec.

## Acesso ao portal

### GER-03: Nada sem login
Sem login, nenhuma tela do portal abre e nenhuma chamada à API é atendida.
- **Exemplo:** abrir o Início sem ter entrado leva à tela de entrada; a API responde 401.
- **Fonte:** regra fictícia da POC.
- **Origem:** [spec 0004](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0004-entrar-no-portal/spec.md).

### GER-04: Supervisor faz o que o operador faz
O supervisor pode fazer tudo o que o operador faz, além do que for só dele.
- **Exemplo:** o usuário `supervisor` tem os perfis operador e supervisor.
- **Fonte:** regra fictícia da POC.
- **Origem:** [spec 0004](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0004-entrar-no-portal/spec.md).

### GER-05: Sessão de 30 minutos sem uso
A sessão termina depois de 30 minutos sem uso; a próxima ação pede login de novo.
- **Exemplo:** quem entrou às 10h00 e não usou o portal até 10h31 é levado à tela de entrada na próxima ação.
- **Fonte:** regra fictícia da POC.
- **Origem:** [spec 0004](https://github.com/jorgekamezawa/poc-custodia-ia/blob/main/docs/specs/0004-entrar-no-portal/spec.md).
