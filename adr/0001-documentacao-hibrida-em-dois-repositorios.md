---
status: aceito
atualizado: 2026-10-24
descricao: A doc da área fica no custodia-docs e a de cada projeto junto do código; um portal junta as duas.
---
# ADR-0001: Documentação híbrida em dois repositórios

**Decisão:** a documentação da área (visão, glossário, regras, áreas vizinhas, padrões) fica no `custodia-docs`, a de cada projeto (ADRs, specs, tasks, runbooks) fica em `docs/` junto do código, e o portal no GitHub Pages junta as duas, porque doc de engenharia muda no mesmo PR que o código e doc da área atravessa projetos.

## Contexto
A área tem vários sistemas que compartilham regras e termos. O cenário de referência tem um repositório próprio de documentação, e o agente precisa buscar contexto num repositório que não é o do código.

## Alternativas descartadas
- **Tudo no repositório de cada projeto:** simples, mas a doc da área seria duplicada ou ficaria num projeto escolhido ao acaso.
- **Tudo num repositório só de documentação:** a doc de engenharia se afasta do código e desatualiza, porque não muda no mesmo PR.

## Consequências
- **Ganhos:** fonte única para a área; doc de projeto revisada junto com o código; um portal só para ler tudo.
- **Custos:** uma feature pode exigir PR nos dois repositórios (código e regras de módulo); o portal só reflete o projeto no próximo build.
- **Passa a ser obrigatório:** o padrão, os templates e o script de verificação vivem no `custodia-docs`, e o CI de cada projeto os usa de lá.
