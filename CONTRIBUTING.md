# Contributing

Obrigado por contribuir com este projeto! Este documento descreve o fluxo de trabalho recomendado, convenções de código e templates para issues / pull requests.

**Resumo rápido**
- Fork → branch feature → commit pequeno e descritivo → abrir PR → passar CI/tests → merge

## 1. Guia rápido
1. Fork do repositório
2. Clone seu fork:

```bash
git clone https://github.com/<seu-usuario>/mlops-boston-project.git
cd mlops-boston-project
```

3. Crie branch de trabalho:

```bash
git checkout -b feature/<curta-descricao>
```

4. Desenvolva, rode testes e linters localmente.
5. Faça commits pequenos e claros.
6. Abra um Pull Request apontando para `main` no repositório original.

## 2. Branches e commits
- Branches: `feature/`, `fix/`, `chore/`, `docs/` (ex.: `feature/add-ci`)
- Mensagens de commit: verbo no imperativo, curto. Ex.: `Add API docs for /predict`
- Rebase preferível a merge para manter histórico limpo.

## 3. Testes e qualidade de código
- Execute antes de abrir PR:

```bash
# ativar venv (Windows)
.venv\Scripts\activate
# instalar deps (se necessário)
pip install -r requirements.txt

# rodar testes
pytest -q

# lint / format
black src/ tests/
ruff check src/ --fix
```

- Adicione testes para mudanças lógicas significativas (preferência por `pytest`).
- Evite mudanças massivas em vários tópicos em um único PR.

## 4. Regras de revisão
- PRs devem conter descrição do problema, solução, e como testar.
- Inclua screenshots ou logs quando aplicável.
- Mantenedores podem solicitar mudanças — responda de forma clara e rápida.

## 5. Atualizando a configuração de features
Se você alterar o conjunto de `top_features` (ordem ou nomes técnicos), siga estas etapas:
1. Atualize `src/train.py` para garantir que o pipeline gere a nova lista corretamente.
2. Rode `python src/train.py` para gerar um novo `top_features.json` e treinar o modelo final.
3. Inclua o novo `top_features.json` no PR e detalhe o motivo no corpo do PR.
4. Atualize também `FEATURES.md`, `API_DOCUMENTATION.md` e `README.md` quando necessário.

> IMPORTANTE: mudanças no contrato de features quebram clientes; coordene mudanças maiores com os mantenedores.

## 6. Template de Pull Request
Use este template ao abrir PRs:

```
Title: <tipo>: Breve descrição

Descrição:
- O que foi mudado?
- Porque essa mudança é necessária?
- Como testar (comandos / passos)?

Checklist:
- [ ] Testes adicionados / atualizados
- [ ] Linter (`black`, `ruff`) rodado
- [ ] `top_features.json` atualizado quando aplicável
- [ ] Documentação atualizada (`FEATURES.md`, `API_DOCUMENTATION.md`)
```

## 7. Template de Issue
Ao abrir uma issue, forneça:
- Descrição breve e reproduzível
- Passos para reproduzir
- Logs / stack trace (se houver)
- Ambiente: OS, Python version, venv/poetry

## 8. Política de revisão de código
- PRs pequenos e atômicos são aprovados mais rápido.
- Revisores devem focar em:
  - Correção funcional
  - Testes adequados
  - Legibilidade / manutenção
  - Segurança e validação de entradas

## 9. Segurança e divulgação responsável
- Se descobrir vulnerabilidade, não abra issue pública. Envie um e-mail ao mantenedor/autor com detalhes.

## 10. Contato e suporte
- Para dúvidas rápidas, abra uma issue com a tag `question`.
- Para contribuições maiores, abra uma issue com o rascunho de design antes de enviar um PR.

---

Obrigado por ajudar a melhorar este projeto! Se quiser, crio `CODE_OF_CONDUCT.md` e templates `.github/PULL_REQUEST_TEMPLATE.md` e `.github/ISSUE_TEMPLATE/bug.md` automaticamente.