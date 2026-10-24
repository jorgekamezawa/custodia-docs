# custodia-docs

Documentação da área de custódia (fictícia) e portal que junta a documentação dos projetos.

## Como rodar localmente
Gerar o portal como o GitHub Pages gera, com Docker:
`docker run --rm -v "$PWD":/src -w /src ghcr.io/actions/jekyll-build-pages:v1.0.13`
O site sai em `_site/`.

## Como rodar os testes
- Script de verificação: `python3 -m unittest discover -s scripts -p 'test_*.py'`.
- Documentos: `python3 scripts/check_docs.py --root .`.

## Documentação
- Portal: https://jorgekamezawa.github.io/custodia-docs/
- Padrão de documentação: [padroes/documentacao.md](padroes/documentacao.md)
