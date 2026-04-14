import streamlit as st
import requests
import pandas as pd
import time as time_module

st.set_page_config(page_title="GitHub EMU Toolkit", page_icon="🐙", layout="wide")

st.sidebar.markdown("## 🐙 GitHub EMU Toolkit")
st.sidebar.markdown("Pre-flight inventory and runbook generator for GitHub → EMU migrations.")
st.sidebar.markdown("---")
st.sidebar.subheader("Connection")

org_input = st.sidebar.text_input("GitHub organization name")
token_input = st.sidebar.text_input("GitHub PAT", type="password")
connect = st.sidebar.button("Connect", type="primary")

BASE_URL = "https://api.github.com"


def gh_headers(token):
    return {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}


def validate_connection(org, token):
    r = requests.get(f"{BASE_URL}/orgs/{org}", headers=gh_headers(token), timeout=10)
    r.raise_for_status()
    return r.json()


def fetch_repos(org, token):
    repos, page = [], 1
    while True:
        r = requests.get(
            f"{BASE_URL}/orgs/{org}/repos",
            headers=gh_headers(token),
            params={"per_page": 100, "page": page, "type": "all"},
            timeout=15,
        )
        r.raise_for_status()
        data = r.json()
        if not data:
            break
        repos.extend(data)
        page += 1
        time_module.sleep(0.1)
    return repos


def has_actions(org, repo_name, token):
    r = requests.get(
        f"{BASE_URL}/repos/{org}/{repo_name}/contents/.github/workflows",
        headers=gh_headers(token),
        timeout=10,
    )
    return r.status_code == 200


def has_webhooks(org, repo_name, token):
    r = requests.get(
        f"{BASE_URL}/repos/{org}/{repo_name}/hooks",
        headers=gh_headers(token),
        timeout=10,
    )
    return r.status_code == 200 and len(r.json()) > 0


def fetch_teams(org, token):
    teams, page = [], 1
    while True:
        r = requests.get(
            f"{BASE_URL}/orgs/{org}/teams",
            headers=gh_headers(token),
            params={"per_page": 100, "page": page},
            timeout=15,
        )
        r.raise_for_status()
        data = r.json()
        if not data:
            break
        teams.extend(data)
        page += 1
        time_module.sleep(0.1)
    return teams


def fetch_outside_collaborators(org, token):
    r = requests.get(
        f"{BASE_URL}/orgs/{org}/outside_collaborators",
        headers=gh_headers(token),
        timeout=10,
    )
    return r.json() if r.status_code == 200 else []


def fetch_app_installations(org, token):
    r = requests.get(
        f"{BASE_URL}/orgs/{org}/installations",
        headers=gh_headers(token),
        timeout=10,
    )
    return r.json().get("total_count", 0) if r.status_code == 200 else 0


# Session state
for key in ("connected", "org_info", "org", "token", "repo_df", "team_df", "risk_flags"):
    if key not in st.session_state:
        st.session_state[key] = None
if st.session_state.connected is None:
    st.session_state.connected = False

if connect and org_input and token_input:
    with st.spinner("Connecting to GitHub..."):
        try:
            info = validate_connection(org_input, token_input)
            st.session_state.connected = True
            st.session_state.org_info = info
            st.session_state.org = org_input
            st.session_state.token = token_input
            st.sidebar.success(f"Connected: {info['login']}")
        except Exception as e:
            st.sidebar.error(f"Connection failed: {e}")
            st.session_state.connected = False

if st.session_state.connected:
    org = st.session_state.org
    token = st.session_state.token
    info = st.session_state.org_info

    total_repos = (info.get("public_repos") or 0) + (info.get("total_private_repos") or 0)
    st.sidebar.metric("Repos", total_repos)

    st.title(f"GitHub EMU Toolkit — {org}")

    # Section 2: Repository Inventory
    st.subheader("Repository Inventory")
    if st.button("Fetch Repository Inventory"):
        with st.spinner("Fetching repos — this may take a while for large orgs..."):
            try:
                raw_repos = fetch_repos(org, token)
                rows = []
                progress = st.progress(0)
                for i, repo in enumerate(raw_repos):
                    name = repo["name"]
                    actions = has_actions(org, name, token)
                    webhooks = has_webhooks(org, name, token)
                    rows.append({
                        "Repo": name,
                        "Visibility": repo.get("visibility", "unknown"),
                        "Default Branch": repo.get("default_branch", ""),
                        "Last Pushed": (repo.get("pushed_at") or "")[:10],
                        "Stars": repo.get("stargazers_count", 0),
                        "Has Actions": "Yes" if actions else "No",
                        "Has Webhooks": "Yes" if webhooks else "No",
                        "Archived": "Yes" if repo.get("archived") else "No",
                    })
                    progress.progress((i + 1) / len(raw_repos))
                    time_module.sleep(0.05)
                st.session_state.repo_df = pd.DataFrame(rows)
            except Exception as e:
                st.error(f"Error fetching repos: {e}")

    if st.session_state.repo_df is not None:
        df = st.session_state.repo_df
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Repos", len(df))
        c2.metric("Private", (df["Visibility"] == "private").sum())
        c3.metric("Has Actions", (df["Has Actions"] == "Yes").sum())
        c4.metric("Has Webhooks", (df["Has Webhooks"] == "Yes").sum())

        vis_filter = st.multiselect(
            "Visibility", ["public", "private", "internal"],
            default=["public", "private", "internal"],
        )
        actions_only = st.checkbox("Only repos with Actions")
        no_archived = st.checkbox("Exclude archived")

        filtered = df[df["Visibility"].isin(vis_filter)]
        if actions_only:
            filtered = filtered[filtered["Has Actions"] == "Yes"]
        if no_archived:
            filtered = filtered[filtered["Archived"] == "No"]

        st.dataframe(filtered, use_container_width=True, hide_index=True)
        st.download_button(
            "Download Inventory CSV",
            data=df.to_csv(index=False),
            file_name="repo_inventory.csv",
            mime="text/csv",
        )

    # Section 3: Team Mapping
    st.subheader("Team & Member Mapping")
    if st.button("Fetch Teams"):
        with st.spinner("Fetching teams..."):
            try:
                teams = fetch_teams(org, token)
                team_rows = [
                    {
                        "Team": t["name"],
                        "Members": t.get("members_count", 0),
                        "Repos": t.get("repos_count", 0),
                        "Privacy": t.get("privacy", ""),
                    }
                    for t in teams
                ]
                st.session_state.team_df = pd.DataFrame(team_rows)
            except Exception as e:
                st.error(f"Error fetching teams: {e}")

    if st.session_state.team_df is not None:
        tdf = st.session_state.team_df
        st.dataframe(tdf, use_container_width=True, hide_index=True)
        high_access = tdf[tdf["Repos"] > 10]
        if not high_access.empty:
            st.warning(
                f"{len(high_access)} team(s) have access to more than 10 repos — "
                "review before EMU migration."
            )
        st.download_button(
            "Export Team Map CSV",
            data=tdf.to_csv(index=False),
            file_name="team_map.csv",
            mime="text/csv",
        )

    # Section 4: Pre-Flight Risk Flags
    st.subheader("Pre-Flight Risk Flags")
    if st.session_state.repo_df is not None:
        df = st.session_state.repo_df
        flags = []
        public_count = (df["Visibility"] == "public").sum()
        wh_count = (df["Has Webhooks"] == "Yes").sum()
        act_count = (df["Has Actions"] == "Yes").sum()

        if public_count > 0:
            flags.append(("error", f"{public_count} public repo(s) detected — confirm before EMU "
                          "(repos become private or internal in EMU by default)"))
        if wh_count > 0:
            flags.append(("warning", f"{wh_count} repos have webhooks — audit external service "
                          "dependencies before migration"))
        if act_count > 0:
            flags.append(("warning", f"{act_count} repos use GitHub Actions — verify Actions secrets "
                          "and environment variables are documented"))

        try:
            outside = fetch_outside_collaborators(org, token)
            if outside:
                flags.append(("error", f"{len(outside)} outside collaborator(s) detected — "
                              "cannot migrate to EMU; must convert to org members or remove"))
        except Exception:
            pass

        try:
            app_count = fetch_app_installations(org, token)
            if app_count > 0:
                flags.append(("warning", f"{app_count} GitHub App(s) installed — verify EMU "
                              "org compatibility for each app"))
        except Exception:
            pass

        if not flags:
            st.success("No critical risk flags detected.")
        for severity, msg in flags:
            if severity == "error":
                st.error(msg)
            else:
                st.warning(msg)
        st.session_state.risk_flags = flags

    # Section 5: Runbook Generator
    st.subheader("Migration Runbook Generator")
    if st.button("Generate Migration Runbook"):
        if st.session_state.repo_df is None:
            st.warning("Fetch the repository inventory first.")
        else:
            df = st.session_state.repo_df
            flags = st.session_state.risk_flags or []
            tdf = st.session_state.team_df

            low_risk = df[
                (df["Has Actions"] == "No") & (df["Has Webhooks"] == "No") & (df["Archived"] == "No")
            ]["Repo"].head(10).tolist()
            wh_repos = df[df["Has Webhooks"] == "Yes"]["Repo"].tolist()
            act_repos = df[df["Has Actions"] == "Yes"]["Repo"].tolist()

            flag_lines = "\n".join([f"- {msg}" for _, msg in flags]) if flags else "- No critical flags detected"
            team_lines = (
                "\n".join([f"- {r['Team']} ({r['Members']} members, {r['Repos']} repos)"
                           for _, r in tdf.iterrows()])
                if tdf is not None and not tdf.empty
                else "- No team data fetched"
            )

            runbook = (
                f"# GitHub EMU Migration Runbook\n"
                f"**Organization:** {org}\n\n---\n\n"
                f"## Phase 1 — Pre-Flight\n**Owner:** IT Ops\n\n{flag_lines}\n\n"
                f"## Phase 2 — EMU Org Setup\n"
                f"- Create new EMU GitHub organization\n"
                f"- Configure SAML SSO (connect to Okta or IdP)\n"
                f"- Configure SCIM provisioning\n"
                f"- Test with 1–2 pilot users end-to-end\n"
                f"- Validate group sync from IdP\n\n"
                f"## Phase 3 — Repository Migration\n"
                f"Migrate lowest-risk repos first (no Actions, no webhooks):\n"
                + ("\n".join([f"- {r}" for r in low_risk]) if low_risk else "- N/A")
                + f"\n\nBatch remaining repos by team ownership using GitHub Enterprise Importer (GEI).\n\n"
                f"## Phase 4 — Team & Access Migration\n{team_lines}\n\n"
                f"## Phase 5 — Webhook Remediation\n"
                + ("\n".join([f"- {r}" for r in wh_repos]) if wh_repos else "- None")
                + f"\n\n## Phase 6 — Actions Secrets Migration\n"
                + ("\n".join([f"- {r}" for r in act_repos]) if act_repos else "- None")
                + f"\n\n## Phase 7 — Outside Collaborator Resolution\n"
                f"- Convert to org member (invite to EMU org via SCIM)\n"
                f"- Remove if no longer needed\n"
                f"- Create external collaboration policy in EMU org\n\n"
                f"## Phase 8 — Cutover & Validation\n"
                f"- Verify all repos migrated and accessible\n"
                f"- Validate CI/CD pipelines running\n"
                f"- Confirm SSO login for all users\n"
                f"- Test webhook endpoints\n"
                f"- Check Actions secrets in new org\n\n"
                f"## Phase 9 — Decommission Source Org\n"
                f"- Archive all repos in source org\n"
                f"- Notify all teams of new org URL\n"
                f"- Update internal documentation\n"
                f"- Cancel or downgrade source org plan after 30-day retention window\n"
            )

            st.text_area("Migration Runbook (Markdown)", runbook, height=400)
            st.download_button(
                "Download Runbook as Markdown",
                data=runbook,
                file_name="emu_migration_runbook.md",
                mime="text/markdown",
            )

else:
    st.title("GitHub EMU Toolkit")
    st.info("Enter your GitHub organization and PAT in the sidebar, then click Connect.")

st.sidebar.markdown("---")
st.sidebar.markdown("Built by [Oleg Strutsovski](https://linkedin.com/in/olegst)")
