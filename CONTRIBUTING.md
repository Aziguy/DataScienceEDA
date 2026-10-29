# Guide de contribution

Merci de votre intérêt pour Playstore Insights. Ce guide décrit comment proposer une modification.

## Avant de commencer

- Cherchez dans les [issues](https://github.com/Aziguy/DataScienceEDA/issues) si le sujet existe déjà.
- Pour une évolution importante, ouvrez d'abord une issue pour en discuter.
- Respectez le [code de conduite](CODE_OF_CONDUCT.md).

## Environnement

```bash
python -m venv .venv && source .venv/bin/activate
```

```bash
make install
```

Node.js 18+ est nécessaire pour exécuter les tests de parité du runtime JavaScript.

## Flux de travail

1. Créez une branche depuis `master` : `feat/...`, `fix/...`, `docs/...`, `refactor/...`.
2. Écrivez le code et les tests associés.
3. Lancez `make lint test` : tout doit passer.
4. Si vous modifiez `web/`, vérifiez le rendu avec `make serve` en thème clair et sombre, sur mobile et sur desktop.
5. Ouvrez une pull request en remplissant le modèle.

## Conventions

**Python.** Ruff gère le lint et le format (ligne de 100 caractères). Typage des signatures publiques, docstrings courtes, pas de commentaires redondants.

**JavaScript.** Modules ES sans build. `web/assets/js/lib/` contient le code réutilisable, `web/assets/js/pages/` un fichier par page. Les libellés issus des données passent par `textContent`, jamais `innerHTML`.

**CSS.** Toute couleur passe par les variables de `:root`, définies pour les deux thèmes.

**Modèles.** Toute modification de `features.py` doit être répercutée dans `web/assets/js/lib/features.js`. Le test `tests/test_js_parity.py` le vérifie.

**Commits.** Messages courts à l'impératif, en anglais : `Add sentiment confusion matrix`, `Fix size parsing for gigabytes`.

## Structure

| Dossier | Rôle |
|---|---|
| `src/playstore_insights/` | Package Python (nettoyage, analyses, modèles, site) |
| `web/` | Sources du site statique |
| `app/` | Application Streamlit |
| `tests/` | Tests pytest et script de parité Node.js |

## Signaler un bug

Utilisez le [formulaire de bug](https://github.com/Aziguy/DataScienceEDA/issues/new?template=bug_report.yml) avec les étapes de reproduction, le comportement attendu et votre environnement.
