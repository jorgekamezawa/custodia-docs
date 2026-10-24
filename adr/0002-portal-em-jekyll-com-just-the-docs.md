---
status: aceito
atualizado: 2026-10-24
descricao: O portal é gerado por Jekyll com o tema Just the Docs, publicado pelo GitHub Actions.
---
# ADR-0002: Portal em Jekyll com Just the Docs

**Decisão:** o portal é gerado pelo Jekyll (gerador nativo do GitHub Pages) com o tema Just the Docs, publicado por workflow do GitHub Actions, porque dá menu lateral e busca sem build próprio e com tema mantido.

## Contexto
O portal precisa de menu por pasta e busca, sem exigir campos de navegação dos autores. O Material for MkDocs entrou em modo de manutenção em novembro de 2025, com fim de vida previsto para 2027, e o sucessor dele, Zensical, ainda está em alpha.

## Alternativas descartadas
- **MkDocs com Material:** navegação e busca excelentes. Descartado por estar em fim de vida.
- **Docusaurus:** gerador em React, muito usado. Descartado por exigir build Node e configuração de menu para um portal só de Markdown.

## Consequências
- **Ganhos:** build com a mesma imagem do GitHub Pages, reproduzível localmente com Docker; menu montado pelo `_config.yml`.
- **Custos:** cada projeto novo exige uma linha de configuração de menu no `_config.yml`.
- **Passa a ser obrigatório:** valor com dois-pontos no frontmatter entre aspas, senão o Jekyll descarta a página.
