# GitHub EMU Toolkit

Pre-flight inventory and runbook generator for GitHub.com → GitHub Enterprise Managed Users (EMU) migrations. Surfaces repo-level secrets, CI/CD dependencies, team mappings, and webhook configurations. Generates a sequenced migration runbook.

Demonstrates 600-user, 2,300-repo EMU migration expertise.

![Screenshot placeholder](screenshot.png)

## Features

- Connect to any GitHub org with a PAT
- Full paginated repo inventory (visibility, Actions, webhooks, archive status)
- Team & member mapping with high-access warnings
- Pre-flight risk flags (public repos, outside collaborators, installed apps)
- One-click migration runbook generator (9-phase)
- CSV export for inventory and team map

## Streamlit UI

```bash
git clone https://github.com/cyrillical00/github-emu-toolkit
cd github-emu-toolkit
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
streamlit run app.py
```

## CLI

```bash
python main.py --org my-org --token ghp_xxx --output-dir ./emu-output
```

Outputs: `inventory.csv`, `team_map.csv`, `risk_flags.txt`, `migration_runbook.md`

## Token Scopes Required

Classic PAT with: `repo`, `admin:org`, `read:org`

## Deploy to Streamlit Cloud

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/cloud)

Add your GitHub PAT in the Streamlit Cloud secrets panel.

---

Built by [Oleg Strutsovski](https://linkedin.com/in/olegst)
