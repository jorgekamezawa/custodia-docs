---
status: ativo
atualizado: 2026-10-24
descricao: Como escrever, organizar e verificar os documentos da área e dos projetos.
---
# Padrão de documentação

Vale para todo documento lido por pessoas, no `custodia-docs` e nos repositórios dos projetos. `CLAUDE.md`, regras e skills do agente seguem o guia da Anthropic, não este padrão.

A documentação tem dois leitores: pessoas e agentes de IA. Por isso cada documento precisa ser fácil de achar e de ler pela metade: o agente decide pelo título e pela descrição se vale abrir.

## Regras de escrita
1. **Resposta primeiro.** As primeiras linhas trazem a conclusão, a decisão ou o propósito. O detalhe vem depois.
2. **Um propósito por documento.** Dois propósitos, dois documentos.
3. **Sem enchimento.** Seção que não se aplica é apagada, não marcada como `N/A`.
4. **Fonte única.** Linke a informação; nunca copie.
5. **Listas e tabelas antes de prosa.** Parágrafos com no máximo 3 frases.
6. **Teste de corte.** Se apagar a frase não perde informação, apague.
7. **Explique no primeiro uso.** Termo de domínio ou pouco comum ganha uma explicação curta na primeira vez, ou um link para o glossário.
8. **Um termo, um nome.** Use o termo do glossário; sinônimo faz pessoa e agente acharem que são coisas diferentes.
9. **Título que diz o conteúdo.** "Baixa de gravame após quitação", não "Regras 2".
10. **Orçamento de tamanho.** Cada tipo tem um tamanho de referência. A verificação aponta quando passar; passar é permitido com motivo registrado.
11. **Diagramas em Mermaid** (diagrama escrito em texto, que o GitHub e o portal desenham), só quando substituem texto.
12. **Documento só existe quando tem gatilho.** O template fica pronto; o documento nasce quando o gatilho acontece.
13. **Sem travessão nem meia-risca.** Use vírgula, dois-pontos, parênteses ou reescreva.

## Metadados
Todo documento começa com frontmatter (cabeçalho de metadados no topo do arquivo):
```yaml
---
status: rascunho | ativo | substituído | obsoleto
atualizado: AAAA-MM-DD
descricao: Uma frase que diz o que o documento responde.
---
```
- A `descricao` é o que o agente lê para decidir se abre o documento. Escreva o que ele responde, não o tipo dele ("Prazos e passos para dar baixa no gravame após a quitação", não "Documento de regras").
- Valor com dois-pontos seguido de espaço vai entre aspas; sem elas o cabeçalho fica inválido e o portal descarta a página.
- Spec, task, ADR e registro de decisões usam status próprio (ver a seção de cada tipo).
- O README não tem frontmatter: o GitHub o mostraria como tabela no topo.

## Ciclo de vida
- O documento nasce do template do seu tipo, em `templates/` do `custodia-docs`, quando o gatilho acontece.
- Só é commitado depois de aprovado. Rejeitado durante a escrita, é apagado sem passar pelo git.
- Seções do template são obrigatórias, exceto as marcadas "só quando houver".
- Documento `substituído` ou `obsoleto` não é apagado: ganha o link de quem o substituiu e sai do menu do portal.

## Catálogo
| Tipo | Para que serve | Gatilho | Onde mora | Dono | Tamanho ref. |
|---|---|---|---|---|---|
| Visão da área | Problema, público, objetivos e o que fica fora da custódia | Início da área | área | produto | 60 linhas |
| Glossário | Termos da área, com definição única e o nome no código | Termo usado em 2+ documentos | área | produto | sem limite |
| Regras de módulo | Regras de negócio **vigentes** de um módulo (contratos, pagamentos, garantias...) | Primeira feature do módulo | área | produto | 150 linhas |
| Área vizinha | O que outro time faz e o que ele entrega ou pede à custódia | Primeira integração com aquele time | área | produto | 60 linhas |
| ADR | Uma decisão técnica, alternativas e consequências | Decisão cara de reverter ou que afeta vários módulos | área, se vale para vários projetos; senão projeto | técnico | 40 linhas |
| Spec de feature | A mudança que uma feature traz: regras, critérios de aceite, contratos, dados e cenários de teste | História refinada pronta para virar código | projeto | produto e técnico | 150 linhas |
| Task de feature | Como uma parte da feature é implementada numa camada | Spec aprovada | projeto | técnico | sem limite |
| Runbook | Passo a passo de operação | Procedimento que alguém executaria sob pressão | projeto | técnico | 40 linhas |
| Spike | Experimento curto que responde uma pergunta técnica | Decisão que não se resolve lendo, só medindo | projeto | técnico | 40 linhas |
| Registro de decisões | Debate de uma entrega: opções, números da época, escolha e correções | Entrega com decisões que não cabem em ADR nem em runbook | projeto | técnico | sem limite |
| Padrão | Como fazer algo sempre do mesmo jeito em todos os projetos | Regra que vale para mais de um projeto | área | técnico | sem limite |
| README | O que é o repositório, como rodar e onde está a doc | Criação do repositório | ambos | técnico | 60 linhas |

- Tamanho conta linhas não vazias, sem metadados e sem blocos de código. Valores iniciais, revisados com o uso.
- Backlog e roadmap ficam no GitHub Projects e Issues.
- Convenções de código ficam em `.claude/rules/` de cada projeto, não em `docs/`.

## Spec e regras de módulo
A spec descreve a **mudança**; a página de regras do módulo guarda o **estado atual** das regras de negócio.
- A spec cita a regra vigente pelo identificador e escreve só o que muda.
- Quando a feature é entregue, a página de regras é atualizada no mesmo ciclo, com o link da spec que originou a mudança.
- Assim, quem quer saber "como funciona hoje" lê uma página só, sem somar specs antigas.
- Contratos de API e dados não têm página de estado atual: cada spec traz o retrato completo do que usa na época. Se o contrato mudar, a feature que trata a mudança traz a nova versão na sua spec.

## Estrutura de pastas
**`custodia-docs` (área)**
```
├── index.md
├── produto/visao.md
├── glossario.md
├── regras/          <modulo>.md
├── areas-vizinhas/  <area>.md
├── adr/             NNNN-titulo-curto.md
├── padroes/         documentacao.md
├── templates/
├── scripts/         check_docs.py
└── projetos/        gerado pelo portal a cada build; não editar
```

**`docs/` de cada projeto**
```
├── index.md
├── adr/        NNNN-titulo-curto.md
├── specs/      NNNN-titulo-curto/
│               ├── spec.md
│               └── tasks/  NN-camada-titulo-curto.md
├── runbooks/
├── spikes/     NNNN-pergunta-curta.md
└── decisoes/   NNNN-titulo-curto.md
```

## Spec de feature
Cada feature tem uma pasta `docs/specs/NNNN-titulo-curto/` com `spec.md` (o quê) e a pasta `tasks/` (como).

**Critério de divisão:** o que independe de linguagem e framework fica na spec; o que depende fica nas tasks.

### spec.md
- Status: `rascunho` | `aprovada` | `entregue` | `substituída`.
- **Parte de negócio** (dono: produto). Seções: problema e link da história; fora de escopo; regras em delta (adicionadas, alteradas, revogadas), citando o identificador da regra do módulo; critérios de aceite em Dado / Quando / Então; telas, com link do esboço (só quando houver).
- **Parte técnica** (dono: tech lead), só quando houver:
  - **Contratos de API**, nossas ou de outros times, que o sistema expõe ou consome: método, URL, headers, códigos de resposta e erros, e uma tabela por corpo com campo, tipo, obrigatório, restrições e exemplo.
  - **Dados:** tabelas criadas ou alteradas, com colunas, tipos, nulidade, chaves, índices e restrições.
  - **Eventos ou arquivos trocados**, no mesmo formato de tabela.
- **Cenários de teste:** tabela com identificador, critério de origem, camada (unitário, integração, componente, ponta a ponta), entrada e resultado esperado. Todo critério tem ao menos um cenário; casos de borda entram como cenários próprios.
- Só vira `aprovada` sem perguntas em aberto e com as duas partes aprovadas pelos donos.
- Mudança depois da aprovação passa por nova aprovação, com uma linha no histórico da spec.

### Tasks
Ficam em `docs/specs/NNNN-titulo-curto/tasks/`, um arquivo por task: `NN-camada-titulo-curto.md` (ex.: `01-back-registro-de-gravame.md`, `03-front-tela-de-garantias.md`, `05-qa-validacao.md`).

- Status: `rascunho` | `aprovada` (pelo tech lead) | `concluída`.
- **Uma camada por task:** `back`, `front` ou `infra`. Nunca duas camadas na mesma task.
- **Um PR por task.**
- Nascem da spec aprovada e são aprovadas pelo tech lead antes da implementação.
- A primeira task de cada camada abre com a **abordagem técnica**: bibliotecas e mecanismos (ex.: cliente HTTP, JPA ou JDBC) e o motivo curto. Decisão significativa vira ADR.
- Cada task diz:
  - **depende de:** tasks que precisam estar prontas antes;
  - **arquivos criados ou alterados**, com o caminho;
  - **para cada classe, interface ou componente:** a responsabilidade e o que implementa ou abstrai, sem código nem assinatura de método;
  - **testes da própria task**, seguindo a pirâmide da camada: no back, unitários de domínio, integração e testes de API; no front, testes de componente;
  - **cenários da spec que passam a ficar verdes.**
- O agente marca os itens ao concluir; o arquivo é revisado no PR junto com o código.

### Task de QA
Toda feature termina com uma task `qa`, sempre a última.
- Confere se o que foi entregue bate com a spec: cada critério de aceite e cada cenário.
- Confere as boas práticas do projeto (convenções e padrões).
- Sobe a aplicação inteira e testa como usuário: o que for automatizável vira teste ponta a ponta com Playwright; o resto é verificado à mão e registrado com evidência.
- Não repete testes unitários nem de integração: esses já vêm das tasks de cada camada.
- Termina com um relatório curto: o que passou, o que falhou e a evidência.

### Validação
- **Antes de aprovar a spec:** o PO pergunta o que falta.
- **Antes de aprovar as tasks:** o `revisor-docs` confere que todo critério tem cenário, todo cenário tem task e todo identificador de regra existe.
- **Antes de cada PR:** o `revisor-codigo` confere o código e os testes contra os cenários da task.

### Quando não precisa de spec
Correção que só faz o código cumprir uma regra que já existe, sem mudar contrato nem dados, vai com a issue e um teste que reproduz o erro.

## Regras de módulo
- Cada regra tem um **identificador estável** (ex.: `GAR-03`), citado pela spec e pelo nome do teste que a verifica. Assim se vai da regra ao teste e do teste à regra.
- Cada regra traz enunciado, exemplo com valores, fonte normativa quando houver e o link da spec que a criou ou alterou.
- Regra que deixa de valer fica marcada como revogada, com o link da spec. O identificador nunca é reaproveitado.

## ADR
- Status: `proposto` | `aceito` | `substituído`.
- **Só vira ADR o que é significativo** (afeta estrutura, uma qualidade importante ou é caro de reverter) **e tem vida própria** (muda sem derrubar outra decisão). Decisão que só existe por causa de outra fica junto dela.
- **Versão muda de rotina:** o ADR registra a política ("usar a versão de suporte mais recente"); o número vive no arquivo de build.
- Idealmente 3 opções que respondem à mesma pergunta. Alternativa descartada é explicada pelo que faz na prática, não pela categoria.
- O debate acontece antes, fora do ADR; ele registra o resultado e o motivo curto de cada descarte.
- **Consequência descreve efeito, não escolhe.** Se havia alternativa plausível para um item, ele é decisão nova e vira outro ADR.
- **Link só aponta para trás**, exceto na substituição: o antigo passa a `substituído` e recebe o link do novo.
- **ADR aceito não se edita.** Se o cenário mudar, um novo o substitui. A única exceção é corrigir erro factual, em PR próprio.
- Arquivo: `NNNN-titulo-curto.md`, numeração sequencial por repositório.

## Spike
- Experimento com prazo que responde **uma** pergunta. Pergunta, prazo e critério de pronto são escritos antes de começar.
- O código é descartado; o spike guarda a evidência (números, comportamento, armadilhas) e alimenta o ADR.

## Registro de decisões
- Status: `registrado`. Retrato datado de uma entrega; não se edita depois.
- Guarda o caminho até a decisão: opções, números da época e o que foi afirmado errado e corrigido. Decisão que virou ADR aparece só com o link.

## Verificação
- **Script `scripts/check_docs.py`** (no `custodia-docs`): roda ao salvar um documento e no CI dos dois repositórios.
  - Erro: metadados ausentes ou com status inválido, travessão, `N/A`, seção obrigatória do template ausente, link relativo quebrado ou que sai do repositório (o portal copia a doc do projeto para outra pasta; para o outro repositório, use a URL do GitHub).
  - Aviso: tamanho acima da referência.
- **Subagente `revisor-docs`:** contexto limpo, confere as regras de escrita 1 a 9 e as regras do tipo ao terminar um documento, antes de ele ir para aprovação humana. Aponta só violação deste padrão, não preferência de estilo.
