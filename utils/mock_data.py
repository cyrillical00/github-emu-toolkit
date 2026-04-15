"""
Mock dataset representing an enterprise-scale GitHub org (~2,300 repos, 600 members).
Used in demo mode — no PAT required.
"""

MOCK_ORG = {
    "login": "acme-corp-demo",
    "name": "Acme Corp (Demo)",
    "public_repos": 12,
    "total_private_repos": 38,
    "description": "Demo org — representative sample of a 600-user, 2,300-repo EMU migration",
}

MOCK_REPOS = [
    {"name": "ios-app", "visibility": "private", "default_branch": "main", "pushed_at": "2026-04-11T18:22:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": True, "archived": False},
    {"name": "android-app", "visibility": "private", "default_branch": "main", "pushed_at": "2026-04-10T14:05:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": True, "archived": False},
    {"name": "backend-api", "visibility": "private", "default_branch": "main", "pushed_at": "2026-04-12T09:33:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": True, "archived": False},
    {"name": "data-platform", "visibility": "private", "default_branch": "main", "pushed_at": "2026-04-09T20:11:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": False, "archived": False},
    {"name": "infra-terraform", "visibility": "private", "default_branch": "main", "pushed_at": "2026-04-08T11:45:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": False, "archived": False},
    {"name": "design-system", "visibility": "internal", "default_branch": "main", "pushed_at": "2026-04-07T16:20:00Z", "stargazers_count": 3, "has_actions": True, "has_webhooks": False, "archived": False},
    {"name": "web-dashboard", "visibility": "private", "default_branch": "main", "pushed_at": "2026-04-06T08:55:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": True, "archived": False},
    {"name": "location-service", "visibility": "private", "default_branch": "main", "pushed_at": "2026-04-05T13:30:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": False, "archived": False},
    {"name": "notification-service", "visibility": "private", "default_branch": "main", "pushed_at": "2026-04-04T17:00:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": True, "archived": False},
    {"name": "auth-service", "visibility": "private", "default_branch": "main", "pushed_at": "2026-04-03T10:15:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": True, "archived": False},
    {"name": "billing-service", "visibility": "private", "default_branch": "main", "pushed_at": "2026-04-02T12:00:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": True, "archived": False},
    {"name": "analytics-pipeline", "visibility": "private", "default_branch": "main", "pushed_at": "2026-04-01T09:00:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": False, "archived": False},
    {"name": "ml-models", "visibility": "private", "default_branch": "main", "pushed_at": "2026-03-28T14:30:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": False, "archived": False},
    {"name": "safety-check-api", "visibility": "private", "default_branch": "main", "pushed_at": "2026-03-25T11:00:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": True, "archived": False},
    {"name": "public-docs", "visibility": "public", "default_branch": "main", "pushed_at": "2026-03-20T10:00:00Z", "stargazers_count": 47, "has_actions": False, "has_webhooks": False, "archived": False},
    {"name": "developer-sdk-ios", "visibility": "public", "default_branch": "main", "pushed_at": "2026-03-15T09:00:00Z", "stargazers_count": 112, "has_actions": True, "has_webhooks": False, "archived": False},
    {"name": "developer-sdk-android", "visibility": "public", "default_branch": "main", "pushed_at": "2026-03-10T09:00:00Z", "stargazers_count": 88, "has_actions": True, "has_webhooks": False, "archived": False},
    {"name": "shared-libs", "visibility": "internal", "default_branch": "main", "pushed_at": "2026-03-05T14:00:00Z", "stargazers_count": 0, "has_actions": False, "has_webhooks": False, "archived": False},
    {"name": "devops-scripts", "visibility": "internal", "default_branch": "main", "pushed_at": "2026-02-28T11:00:00Z", "stargazers_count": 0, "has_actions": False, "has_webhooks": False, "archived": False},
    {"name": "compliance-tooling", "visibility": "private", "default_branch": "main", "pushed_at": "2026-02-20T10:00:00Z", "stargazers_count": 0, "has_actions": False, "has_webhooks": False, "archived": False},
    {"name": "old-monolith", "visibility": "private", "default_branch": "master", "pushed_at": "2025-06-01T08:00:00Z", "stargazers_count": 0, "has_actions": False, "has_webhooks": False, "archived": True},
    {"name": "legacy-auth", "visibility": "private", "default_branch": "master", "pushed_at": "2024-11-15T08:00:00Z", "stargazers_count": 0, "has_actions": False, "has_webhooks": False, "archived": True},
    {"name": "deprecated-v1-api", "visibility": "private", "default_branch": "master", "pushed_at": "2024-03-01T08:00:00Z", "stargazers_count": 0, "has_actions": False, "has_webhooks": False, "archived": True},
    {"name": "growth-experiments", "visibility": "private", "default_branch": "main", "pushed_at": "2026-04-11T15:00:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": False, "archived": False},
    {"name": "feature-flags", "visibility": "internal", "default_branch": "main", "pushed_at": "2026-04-10T12:00:00Z", "stargazers_count": 0, "has_actions": False, "has_webhooks": True, "archived": False},
    {"name": "crisis-alerts", "visibility": "private", "default_branch": "main", "pushed_at": "2026-04-09T10:00:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": True, "archived": False},
    {"name": "partner-integrations", "visibility": "private", "default_branch": "main", "pushed_at": "2026-04-08T09:00:00Z", "stargazers_count": 0, "has_actions": False, "has_webhooks": True, "archived": False},
    {"name": "runbooks", "visibility": "internal", "default_branch": "main", "pushed_at": "2026-04-07T14:00:00Z", "stargazers_count": 0, "has_actions": False, "has_webhooks": False, "archived": False},
    {"name": "security-scanning", "visibility": "private", "default_branch": "main", "pushed_at": "2026-04-06T11:00:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": False, "archived": False},
    {"name": "load-testing", "visibility": "internal", "default_branch": "main", "pushed_at": "2026-03-30T10:00:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": False, "archived": False},
    {"name": "incident-response", "visibility": "private", "default_branch": "main", "pushed_at": "2026-03-22T09:00:00Z", "stargazers_count": 0, "has_actions": False, "has_webhooks": True, "archived": False},
    {"name": "customer-support-tools", "visibility": "private", "default_branch": "main", "pushed_at": "2026-03-18T08:00:00Z", "stargazers_count": 0, "has_actions": False, "has_webhooks": False, "archived": False},
    {"name": "internal-admin-portal", "visibility": "private", "default_branch": "main", "pushed_at": "2026-03-12T10:00:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": False, "archived": False},
    {"name": "helm-charts", "visibility": "internal", "default_branch": "main", "pushed_at": "2026-04-05T16:00:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": False, "archived": False},
    {"name": "chaos-engineering", "visibility": "private", "default_branch": "main", "pushed_at": "2026-03-08T11:00:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": False, "archived": False},
    {"name": "reporting-service", "visibility": "private", "default_branch": "main", "pushed_at": "2026-02-14T09:00:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": True, "archived": False},
    {"name": "user-segmentation", "visibility": "private", "default_branch": "main", "pushed_at": "2026-01-30T10:00:00Z", "stargazers_count": 0, "has_actions": False, "has_webhooks": False, "archived": False},
    {"name": "content-delivery", "visibility": "private", "default_branch": "main", "pushed_at": "2026-01-15T08:00:00Z", "stargazers_count": 0, "has_actions": False, "has_webhooks": True, "archived": False},
    {"name": "marketplace-integrations", "visibility": "private", "default_branch": "main", "pushed_at": "2025-12-20T10:00:00Z", "stargazers_count": 0, "has_actions": False, "has_webhooks": False, "archived": False},
    {"name": "prototype-ai-features", "visibility": "private", "default_branch": "main", "pushed_at": "2026-04-12T17:00:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": False, "archived": False},
    {"name": "config-management", "visibility": "internal", "default_branch": "main", "pushed_at": "2026-04-11T12:00:00Z", "stargazers_count": 0, "has_actions": False, "has_webhooks": False, "archived": False},
    {"name": "event-bus", "visibility": "private", "default_branch": "main", "pushed_at": "2026-04-10T08:00:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": True, "archived": False},
    {"name": "cache-service", "visibility": "private", "default_branch": "main", "pushed_at": "2026-04-09T16:00:00Z", "stargazers_count": 0, "has_actions": False, "has_webhooks": False, "archived": False},
    {"name": "search-service", "visibility": "private", "default_branch": "main", "pushed_at": "2026-04-08T13:00:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": False, "archived": False},
    {"name": "media-processing", "visibility": "private", "default_branch": "main", "pushed_at": "2026-04-07T10:00:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": True, "archived": False},
    {"name": "geofencing-engine", "visibility": "private", "default_branch": "main", "pushed_at": "2026-04-06T14:00:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": False, "archived": False},
    {"name": "test-automation", "visibility": "internal", "default_branch": "main", "pushed_at": "2026-04-05T09:00:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": False, "archived": False},
    {"name": "docs-site", "visibility": "public", "default_branch": "main", "pushed_at": "2026-04-04T11:00:00Z", "stargazers_count": 23, "has_actions": True, "has_webhooks": False, "archived": False},
    {"name": "release-tooling", "visibility": "internal", "default_branch": "main", "pushed_at": "2026-04-03T15:00:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": True, "archived": False},
    {"name": "customer-data-platform", "visibility": "private", "default_branch": "main", "pushed_at": "2026-04-02T10:00:00Z", "stargazers_count": 0, "has_actions": True, "has_webhooks": False, "archived": False},
]

MOCK_TEAMS = [
    {"name": "ios-team", "members_count": 18, "repos_count": 4, "privacy": "closed"},
    {"name": "android-team", "members_count": 15, "repos_count": 4, "privacy": "closed"},
    {"name": "backend-platform", "members_count": 32, "repos_count": 18, "privacy": "closed"},
    {"name": "data-engineering", "members_count": 12, "repos_count": 8, "privacy": "closed"},
    {"name": "devops-sre", "members_count": 8, "repos_count": 22, "privacy": "closed"},
    {"name": "security", "members_count": 5, "repos_count": 12, "privacy": "secret"},
    {"name": "ml-team", "members_count": 9, "repos_count": 5, "privacy": "closed"},
    {"name": "growth-eng", "members_count": 14, "repos_count": 7, "privacy": "closed"},
    {"name": "web-frontend", "members_count": 11, "repos_count": 6, "privacy": "closed"},
    {"name": "qa-automation", "members_count": 7, "repos_count": 9, "privacy": "closed"},
    {"name": "all-engineers", "members_count": 131, "repos_count": 50, "privacy": "closed"},
    {"name": "contractors", "members_count": 6, "repos_count": 3, "privacy": "secret"},
]

MOCK_OUTSIDE_COLLABORATORS = [
    {"login": "vendor-contractor-1", "type": "User"},
    {"login": "agency-dev-bot", "type": "User"},
    {"login": "security-audit-external", "type": "User"},
]

MOCK_APP_COUNT = 4  # GitHub Apps installed: Datadog, Snyk, Dependabot, CodeClimate
