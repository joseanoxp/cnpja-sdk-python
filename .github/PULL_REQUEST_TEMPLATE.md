<!--
Título do PR deve seguir Conventional Commits (vira commit único em main via squash merge):
    <type>(<scope>): <descrição>

Exemplos: feat(office): adiciona filtro X | fix(pager): corrige iteração vazia
Adicione `!` no tipo para breaking changes (ex: `feat(office)!: remove campo X`).
-->

## Summary

<!-- O que esta mudança resolve e por quê. Linke a issue se aplicável. -->

## Test Plan

<!-- Como foi testado? Que cenários cobrem? -->

## Checklist

- [ ] Título e commits seguem [Conventional Commits](https://www.conventionalcommits.org/)
- [ ] `task qa` passa localmente (`uv lock --check`, lint, format, typecheck, tests, pre-commit)
- [ ] Testes novos ou atualizados cobrem as mudanças
- [ ] Para mudanças em DTOs: `schemas/openapi.json` e `src/cnpja/types/` permanecem sincronizados
- [ ] Documentação (README/CONTRIBUTING/CLAUDE) atualizada quando aplicável
