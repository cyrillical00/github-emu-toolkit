#!/usr/bin/env python3
"""
GitHub EMU Toolkit — CLI
Usage: python main.py --org <org> --token <token> --output-dir <dir>

Exports: inventory.csv, team_map.csv, risk_flags.txt, migration_runbook.md
"""

import argparse
import csv
import os
import time
import requests

BASE_URL = "https://api.github.com"


def headers(token):
    return {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}


def fetch_repos(org, token):
    repos, page = [], 1
    while True:
        r = requests.get(
            f"{BASE_URL}/orgs/{org}/repos",
            headers=headers(token),
            params={"per_page": 100, "page": page, "type": "all"},
        )
        r.raise_for_status()
        data = r.json()
        if not data:
            break
        repos.extend(data)
        page += 1
        time.sleep(0.1)
    return repos


def has_actions(org, repo, token):
    r = requests.get(
        f"{BASE_URL}/repos/{org}/{repo}/contents/.github/workflows",
        headers=headers(token),
    )
    return r.status_code == 200


def has_webhooks(org, repo, token):
    r = requests.get(
        f"{BASE_URL}/repos/{org}/{repo}/hooks",
        headers=headers(token),
    )
    return r.status_code == 200 and len(r.json()) > 0


def fetch_teams(org, token):
    teams, page = [], 1
    while True:
        r = requests.get(
            f"{BASE_URL}/orgs/{org}/teams",
            headers=headers(token),
            params={"per_page": 100, "page": page},
        )
        r.raise_for_status()
        data = r.json()
        if not data:
            break
        teams.extend(data)
        page += 1
        time.sleep(0.1)
    return teams


def main():
    parser = argparse.ArgumentParser(description="GitHub EMU Toolkit CLI")
    parser.add_argument("--org", required=True, help="GitHub organization name")
    parser.add_argument("--token", required=True, help="GitHub PAT (classic, repo + admin:org scopes)")
    parser.add_argument("--output-dir", default="./emu-output", help="Output directory")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    print(f"Connecting to org: {args.org}")

    r = requests.get(f"{BASE_URL}/orgs/{args.org}", headers=headers(args.token))
    r.raise_for_status()
    org_info = r.json()
    total_repos = (org_info.get("public_repos") or 0) + (org_info.get("total_private_repos") or 0)
    print(f"Connected: {org_info['login']} — {total_repos} repos")

    print("Fetching repositories...")
    raw_repos = fetch_repos(args.org, args.token)
    inventory = []
    for repo in raw_repos:
        name = repo["name"]
        print(f"  Checking {name}...")
        act = has_actions(args.org, name, args.token)
        wh = has_webhooks(args.org, name, args.token)
        inventory.append({
            "repo": name,
            "visibility": repo.get("visibility", ""),
            "default_branch": repo.get("default_branch", ""),
            "last_pushed": (repo.get("pushed_at") or "")[:10],
            "stars": repo.get("stargazers_count", 0),
            "has_actions": "yes" if act else "no",
            "has_webhooks": "yes" if wh else "no",
            "archived": "yes" if repo.get("archived") else "no",
        })
        time.sleep(0.05)

    if inventory:
        inv_path = os.path.join(args.output_dir, "inventory.csv")
        with open(inv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(inventory[0].keys()))
            writer.writeheader()
            writer.writerows(inventory)
        print(f"Saved: {inv_path}")

    print("Fetching teams...")
    teams = fetch_teams(args.org, args.token)
    team_rows = [
        {"team": t["name"], "members": t.get("members_count", 0), "repos": t.get("repos_count", 0)}
        for t in teams
    ]
    team_path = os.path.join(args.output_dir, "team_map.csv")
    with open(team_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["team", "members", "repos"])
        writer.writeheader()
        writer.writerows(team_rows)
    print(f"Saved: {team_path}")

    # Risk flags
    flags = []
    public_count = sum(1 for r in inventory if r["visibility"] == "public")
    wh_count = sum(1 for r in inventory if r["has_webhooks"] == "yes")
    act_count = sum(1 for r in inventory if r["has_actions"] == "yes")
    if public_count:
        flags.append(f"RED: {public_count} public repos detected")
    if wh_count:
        flags.append(f"AMBER: {wh_count} repos have webhooks")
    if act_count:
        flags.append(f"AMBER: {act_count} repos use GitHub Actions")

    try:
        oc = requests.get(
            f"{BASE_URL}/orgs/{args.org}/outside_collaborators",
            headers=headers(args.token),
        )
        if oc.status_code == 200 and oc.json():
            flags.append(f"RED: {len(oc.json())} outside collaborators detected")
    except Exception:
        pass

    flags_path = os.path.join(args.output_dir, "risk_flags.txt")
    with open(flags_path, "w", encoding="utf-8") as f:
        f.write("\n".join(flags) if flags else "No critical risk flags detected.")
    print(f"Saved: {flags_path}")

    # Runbook
    low_risk = [
        r["repo"] for r in inventory
        if r["has_actions"] == "no" and r["has_webhooks"] == "no" and r["archived"] == "no"
    ][:10]
    wh_repos = [r["repo"] for r in inventory if r["has_webhooks"] == "yes"]
    act_repos = [r["repo"] for r in inventory if r["has_actions"] == "yes"]

    runbook = (
        f"# GitHub EMU Migration Runbook\nOrganization: {args.org}\n\n"
        f"## Phase 1 — Pre-Flight\n"
        + ("\n".join(flags) if flags else "No critical flags.") + "\n\n"
        + "## Phase 2 — EMU Org Setup\n"
        + "Create EMU org, configure SAML and SCIM, test pilot users.\n\n"
        + "## Phase 3 — Repo Migration (Low-Risk First)\n"
        + ("\n".join(f"- {r}" for r in low_risk) if low_risk else "- N/A") + "\n\n"
        + "## Phase 4 — Team Migration\n"
        + "\n".join(f"- {t['team']} ({t['members']} members)" for t in team_rows) + "\n\n"
        + "## Phase 5 — Webhook Remediation\n"
        + ("\n".join(f"- {r}" for r in wh_repos) if wh_repos else "- None") + "\n\n"
        + "## Phase 6 — Actions Secrets\n"
        + ("\n".join(f"- {r}" for r in act_repos) if act_repos else "- None") + "\n\n"
        + "## Phase 7 — Outside Collaborator Resolution\n"
        + "Review and convert or remove outside collaborators.\n\n"
        + "## Phase 8 — Cutover & Validation\n"
        + "Verify all access, CI/CD pipelines, and SSO.\n\n"
        + "## Phase 9 — Decommission Source Org\n"
        + "Archive repos, notify teams, cancel plan after 30-day window.\n"
    )

    runbook_path = os.path.join(args.output_dir, "migration_runbook.md")
    with open(runbook_path, "w", encoding="utf-8") as f:
        f.write(runbook)
    print(f"Saved: {runbook_path}")
    print("Done.")


if __name__ == "__main__":
    main()
