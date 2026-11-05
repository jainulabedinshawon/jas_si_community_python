⚡ JAS-SI Community Python SDK

A lightweight Python client for JAS-SI Intelligence API

""Python" (https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)" (https://www.python.org/)
""CI" (https://github.com/jainulabedinshawon/jas_si_community_python/actions/workflows/ci.yml/badge.svg)" (https://github.com/jainulabedinshan/jas_si_community_python/actions/workflows/ci.yml)
""API" (https://img.shields.io/badge/JAS--SI_API-v0.1.0-0A7A55)" (https://jas-si.vercel.app/docs)
""SDK" (https://img.shields.io/badge/SDK-0.1.0-6F42C1)" (https://github.com/jainulabedinshawon/jas_si_community_python)

JAS-SI Community Python SDK is an independent Python HTTP client for interacting with the JAS-SI API.

It provides a simple interface for authorization evaluation, outcome verification, and GitHub evidence integrity checks.

«The SDK communicates with the JAS-SI API. It does not contain or expose the proprietary JAS-SI Core engine.»

---

✨ Features

- 🔐 Authorization evaluation
- ✅ Outcome verification
- 🐙 GitHub evidence integrity checks
- 🔑 API key authentication
- 🔒 HTTPS enforcement for remote API connections
- ⏱️ Configurable request timeout
- 🧩 Context manager support
- 🧪 Automated tests across Python 3.10–3.13

🚀 Installation

Install directly from GitHub:

pip install git+https://github.com/jainulabedinshawon/jas_si_community_python.git

⚡ Quick Start

from jas_si_community_python import JASSIClient

with JASSIClient(
    api_key="YOUR_API_KEY",
    base_url="https://jas-si.vercel.app"
) as client:

    health = client.health()
    print(health)

Keep your API key private. Never commit credentials to source control.

🔐 Authorization Evaluation

Evaluate whether an action is authorized.

from jas_si_community_python import JASSIClient

with JASSIClient(api_key="YOUR_API_KEY") as client:
    result = client.authorize(
        action_id="task-001",
        action="read",
        resource="repository"
    )

    print(result)

✅ Outcome Verification

Submit an outcome for verification.

with JASSIClient(api_key="YOUR_API_KEY") as client:
    result = client.verify(
        action_id="task-001",
        claimed_success=True,
        observed_state={"status": "completed"},
        evidence_ref="evidence-001"
    )

    print(result)

🐙 GitHub Evidence Integrity

Check GitHub commit and file evidence.

with JASSIClient(api_key="YOUR_API_KEY") as client:
    result = client.verify_github_evidence(
        repository="owner/repository",
        commit_sha="YOUR_40_CHARACTER_COMMIT_SHA",
        paths=["README.md"]
    )

    print(result)

Important: GitHub evidence integrity checks do not establish the semantic truth of a claim or prove that a reported outcome is correct.

⚙️ Configuration

client = JASSIClient(
    api_key="YOUR_API_KEY",
    base_url="https://jas-si.vercel.app",
    timeout=15.0
)

Parameter| Description
"api_key"| API authentication key
"base_url"| JAS-SI API endpoint
"timeout"| Request timeout in seconds

The API key is required for protected endpoints.

🛡️ Security Notes

- Use HTTPS for remote API connections.
- Keep API keys in environment variables or a secrets manager.
- Do not expose API keys in public repositories.
- Use appropriate access controls for production systems.

Example:

import os

api_key = os.environ["JAS_SI_API_KEY"]

⚠️ Scope and Limitations

This project is an API client, not the JAS-SI Core engine.

- The API evaluates authorization; it does not execute external actions.
- Outcome verification depends on evidence submitted to the API.
- Caller-submitted evidence should not automatically be described as independently collected evidence.
- GitHub evidence checks establish integrity-related properties, not semantic truth.
- API availability, authentication policies, rate limits, and endpoint behavior are controlled by the API service.

📚 API Documentation

- Live API: https://jas-si.vercel.app
- Interactive API Docs: https://jas-si.vercel.app/docs
- OpenAPI Specification: https://jas-si.vercel.app/openapi.json

🧪 Development

Clone the repository:

git clone https://github.com/jainulabedinshawon/jas_si_community_python.git

cd jas_si_community_python

Install development dependencies:

python -m pip install -e ".[dev]"

Run tests:

python -m pytest -v

🏗️ Architecture

Your Python Application
          |
          v
JAS-SI Community Python SDK
          |
          | HTTPS
          v
     JAS-SI API
          |
          v
Authorization Evaluation
Outcome Verification
GitHub Evidence Integrity

The Community SDK remains architecturally separate from the proprietary JAS-SI Core.

🤝 Contributing

Contributions, bug reports, and technical feedback are welcome.

Please open an issue before proposing significant architectural changes.

🏛️ Project

JAS-SI — JAS Intelligence

Developed by JAS Research.

Research direction: Reality-Based Intelligence, Authorization-Gated Action, Independent Verification, and Accountable Governance.

---

Building intelligence that verifies reality — not just reports success.
