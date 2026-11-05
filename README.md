JAS-SI Community Python Client

An independent Python HTTP client for the JAS-SI REST API.

The client lets Python applications communicate with JAS-SI for authorization evaluation, outcome verification, and GitHub evidence-integrity checks.

This SDK does not contain or execute JAS-SI Core logic.

Features

- Check API health
- Request authorization evaluation
- Submit outcome reports for verification
- Verify GitHub commit and file integrity
- HTTPS enforcement for remote API connections
- Configurable request timeout
- API-key authentication
- Context-manager support
- Python 3.10–3.13 compatibility

Requirements

- Python 3.10 or newer
- Access to the JAS-SI API
- An API key for protected endpoints

Installation

Install directly from GitHub:

pip install git+https://github.com/jainulabedinshawon/jas_si_community_python.git

Or clone the repository and install locally:

git clone https://github.com/jainulabedinshawon/jas_si_community_python.git
cd jas_si_community_python
pip install .

Quick Start

from jas_si_community_python import JASSIClient

with JASSIClient(
    api_key="YOUR_API_KEY"
) as client:

    health = client.health()
    print(health)

Use an environment variable or a secure secret manager for API keys in real applications. Do not commit API keys to source control.

Authorization Evaluation

from jas_si_community_python import JASSIClient

with JASSIClient(api_key="YOUR_API_KEY") as client:
    result = client.authorize(
        action_id="action-001",
        action="read",
        resource="document",
    )

    print(result)

This endpoint evaluates authorization. It does not execute the requested action.

Outcome Verification

with JASSIClient(api_key="YOUR_API_KEY") as client:
    result = client.verify(
        action_id="action-001",
        claimed_success=True,
        observed_state="completed",
        evidence_ref="evidence-001",
    )

    print(result)

The verification endpoint evaluates submitted outcome information. Caller-submitted evidence is not automatically independent evidence.

GitHub Evidence Integrity

with JASSIClient(api_key="YOUR_API_KEY") as client:
    result = client.verify_github_evidence(
        repository="owner/repository",
        commit_sha="YOUR_40_CHARACTER_COMMIT_SHA",
        paths=["README.md"],
    )

    print(result)

This endpoint checks GitHub commit and file integrity. It does not establish the semantic truth of repository contents.

Error Handling

from jas_si_community_python import JASSIClient, JASSIError

try:
    with JASSIClient(api_key="YOUR_API_KEY") as client:
        result = client.authorize(
            "action-001",
            "read",
            "document",
        )

except JASSIError as error:
    print("JAS-SI request failed:", error)

    if error.status_code is not None:
        print("HTTP status:", error.status_code)

Configuration

client = JASSIClient(
    base_url="https://jas-si.vercel.app",
    api_key="YOUR_API_KEY",
    timeout=10.0,
)

Parameter| Description
"base_url"| JAS-SI API base URL
"api_key"| API key for protected endpoints
"timeout"| Request timeout in seconds

HTTPS is required for remote API URLs. HTTP is permitted only for local development addresses.

API Reference

Method| Endpoint| Authentication
"health()"| "GET /health"| Public
"authorize()"| "POST /v1/authorize"| API key
"verify()"| "POST /v1/verify"| API key
"verify_github_evidence()"| "POST /v1/github/evidence"| API key

API documentation: https://jas-si.vercel.app/docs

Important Limitations

- This SDK is an HTTP client, not the JAS-SI Core engine.
- Authorization evaluation does not execute external actions.
- Outcome verification depends on the evidence supplied to the API.
- GitHub evidence-integrity checks do not prove semantic truth.
- API availability, authentication, rate limits, and endpoint behavior are controlled by the API service.

Development

git clone https://github.com/jainulabedinshawon/jas_si_community_python.git
cd jas_si_community_python

pip install -e ".[dev]"
python -m pytest -v

Project

- GitHub: https://github.com/jainulabedinshawon/jas_si_community_python
- JAS-SI API: https://jas-si.vercel.app
- API Documentation: https://jas-si.vercel.app/docs

Maintained by JAS Research.

JAS-SI is designed around authorization evaluation, evidence-based verification, and accountable outcomes.
