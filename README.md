⚡ JAS-SI Community Python SDK

A lightweight Python client for the JAS-SI Intelligence API

""Python" (https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)" (https://www.python.org/)
""CI" (https://github.com/jainulabedinshawon/jas_si_community_python/actions/workflows/ci.yml/badge.svg)" (https://github.com/jainulabedinshawon/jas_si_community_python/actions/workflows/ci.yml)
""API" (https://img.shields.io/badge/JAS--SI_API-v0.1.0-0A7A55)" (https://jas-si.vercel.app/docs)
""SDK" (https://img.shields.io/badge/SDK-0.1.0-6F42C1)" (https://github.com/jainulabedinshawon/jas_si_community_python)

JAS-SI Community Python SDK is an independent Python HTTP client for interacting with the JAS-SI API.

It provides a straightforward interface for authorization evaluation, outcome verification, and GitHub evidence integrity checks.

«Architecture: This SDK communicates with the JAS-SI API over HTTPS. It does not contain, redistribute, or expose the proprietary JAS-SI Core engine.»

---

✨ Features

- 🔐 Authorization evaluation
- ✅ Outcome verification
- 🐙 GitHub commit and file integrity checks
- 🔑 API key authentication
- 🔒 HTTPS enforcement for remote API connections
- ⏱️ Configurable request timeout
- 🧩 Context manager support
- 🧪 Automated compatibility tests for Python 3.10–3.13

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
        action="read_repository",
        resource="repository"
    )

    print(result)

Important: Authorization evaluation determines whether an action is permitted. It does not execute the action.

✅ Outcome Verification

Submit an outcome for verification.

from jas_si_community_python import JASSIClient

with JASSIClient(api_key="YOUR_API_KEY") as client:
    result = client.verify(
        action_id="task-001",
        claimed_success=True,
        observed_state="completed",
        evidence_ref="evidence-001"
    )

    print(result)

Verification note: The API evaluates the submitted outcome against available evidence. Caller-submitted evidence is not automatically independently collected. The result may be "INCONCLUSIVE" when the evidence is insufficient or its trust cannot be established.

🐙 GitHub Evidence Integrity

Check GitHub commit and file evidence.

from jas_si_community_python import JASSIClient

with JASSIClient(api_key="YOUR_API_KEY") as client:
    result = client.verify_github_evidence(
        repository="owner/repository",
        commit_sha="YOUR_40_CHARACTER_COMMIT_SHA",
        paths=["README.md"]
    )

    print(result)

This endpoint performs read-only GitHub evidence integrity checks.

Important: GitHub evidence integrity does not establish the semantic truth of a claim or prove that a reported outcome actually occurred.

⚙️ Configuration

Configure the client with your API key, API endpoint, and request timeout.

from jas_si_community_python import JASSIClient

client = JASSIClient(
    api_key="YOUR_API_KEY",
    base_url="https://jas-si.vercel.app",
    timeout=15.0
)

Parameter| Description
"api_key"| API authentication key
"base_url"| JAS-SI API endpoint
"timeout"| Request timeout in seconds

Use the context manager whenever possible to ensure the HTTP client is properly closed.

The API key is required for protected endpoints.

🛡️ Security Practices

- Use HTTPS for remote API connections.
- Store API keys in environment variables or a secrets manager.
- Never expose API keys in public repositories.
- Avoid hardcoding credentials in application source code.
- Apply appropriate access controls in production environments.

Example:

import os

api_key = os.environ["JAS_SI_API_KEY"]

⚠️ Scope and Limitations

The Community SDK is an API client, not the JAS-SI Core engine.

Please understand the following boundaries:

1. No action execution: The API evaluates authorization but does not execute external actions.
2. Evidence dependency: Outcome verification depends on evidence submitted to the API.
3. No automatic independent collection: Caller-submitted evidence must not be represented as independently collected evidence.
4. Integrity is not semantic truth: GitHub evidence checks establish integrity-related properties, not the truth of the underlying claim.
5. Service-controlled behavior: API availability, authentication policies, rate limits, and endpoint behavior are controlled by the API service.

These boundaries are important when integrating JAS-SI into applications, automation systems, or AI agents.

📚 API Documentation

- 🌐 Live API: https://jas-si.vercel.app
- 📖 Interactive API Documentation: https://jas-si.vercel.app/docs
- 📄 OpenAPI Specification: https://jas-si.vercel.app/openapi.json

🧪 Development

Clone the repository:

git clone https://github.com/jainulabedinshawon/jas_si_community_python.git

cd jas_si_community_python

Install development dependencies:

python -m pip install -e ".[dev]"

Run the test suite:

python -m pytest -v

The CI workflow tests the SDK against Python 3.10, 3.11, 3.12, and 3.13.

🏗️ Architecture

┌──────────────────────────────┐
│     Your Python Application  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│  JAS-SI Community Python SDK │
└──────────────┬───────────────┘
               │
               │ HTTPS
               ▼
┌──────────────────────────────┐
│          JAS-SI API          │
├──────────────────────────────┤
│ Authorization Evaluation     │
│ Outcome Verification         │
│ GitHub Evidence Integrity    │
└──────────────────────────────┘

The Community SDK is architecturally separate from the proprietary JAS-SI Core.

🤝 Contributing

Contributions, bug reports, and technical feedback are welcome.

Before proposing significant architectural changes, please open an issue to discuss the proposed approach.

All contributions remain subject to the repository's applicable licensing terms.

🏛️ Project

JAS-SI — JAS Intelligence

Developed by JAS Research.

Research direction:

- Reality-Based Intelligence
- Authorization-Gated Action
- Independent Verification
- Verified-Failure Learning
- Accountable Governance

---

Building intelligence that verifies reality — not just reports success.
