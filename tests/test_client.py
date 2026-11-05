
import json

import httpx
import pytest

from jas_si_community_python import JASSIClient, JASSIError


def make_client(handler, api_key="test-key"):
    transport = httpx.MockTransport(handler)

    client = JASSIClient(api_key=api_key)
    client._client.close()
    client._client = httpx.Client(
        base_url="https://api.example.test",
        headers={
            "X-API-Key": api_key,
            "Accept": "application/json",
        } if api_key else {"Accept": "application/json"},
        transport=transport,
    )
    return client


def close_client(client):
    client.close()


def test_health():
    def handler(request):
        assert request.method == "GET"
        assert request.url.path == "/health"

        return httpx.Response(
            200,
            json={
                "service": "JAS-SI API",
                "status": "ok",
                "api_enabled": True,
            },
        )

    client = make_client(handler)

    try:
        result = client.health()
        assert result["status"] == "ok"
        assert result["api_enabled"] is True
    finally:
        close_client(client)


def test_authorize_matches_api_contract():
    def handler(request):
        assert request.method == "POST"
        assert request.url.path == "/v1/authorize"
        assert request.headers["X-API-Key"] == "test-key"

        body = json.loads(request.read())

        assert body == {
            "action_id": "test-1",
            "action": "read_repository",
            "resource": "owner/repository",
        }

        return httpx.Response(
            200,
            json={
                "action_id": "test-1",
                "allowed": False,
                "reason": "denied",
                "grant_id": None,
                "executed": False,
            },
        )

    client = make_client(handler)

    try:
        result = client.authorize(
            action_id="test-1",
            action="read_repository",
            resource="owner/repository",
        )

        assert result["action_id"] == "test-1"
        assert result["allowed"] is False
        assert result["reason"] == "denied"
        assert result["grant_id"] is None
        assert result["executed"] is False
    finally:
        close_client(client)


def test_verify_matches_api_contract():
    def handler(request):
        assert request.method == "POST"
        assert request.url.path == "/v1/verify"
        assert request.headers["X-API-Key"] == "test-key"

        body = json.loads(request.read())

        assert body == {
            "action_id": "verify-1",
            "claimed_success": True,
            "observed_state": "completed",
            "evidence_ref": "evidence-1",
        }

        return httpx.Response(
            200,
            json={
                "action_id": "verify-1",
                "status": "INCONCLUSIVE",
                "reason": "Evidence is not independently collected.",
                "evidence_origin": "caller_submitted",
            },
        )

    client = make_client(handler)

    try:
        result = client.verify(
            action_id="verify-1",
            claimed_success=True,
            observed_state="completed",
            evidence_ref="evidence-1",
        )

        assert result["action_id"] == "verify-1"
        assert result["status"] == "INCONCLUSIVE"
        assert result["evidence_origin"] == "caller_submitted"
        assert isinstance(result["reason"], str)
    finally:
        close_client(client)


def test_verify_without_evidence():
    def handler(request):
        body = json.loads(request.read())

        assert body == {
            "action_id": "verify-2",
            "claimed_success": False,
        }

        return httpx.Response(
            200,
            json={
                "action_id": "verify-2",
                "status": "INCONCLUSIVE",
                "reason": "Evidence not provided.",
                "evidence_origin": "not_provided",
            },
        )

    client = make_client(handler)

    try:
        result = client.verify(
            action_id="verify-2",
            claimed_success=False,
        )

        assert result["evidence_origin"] == "not_provided"
    finally:
        close_client(client)


def test_github_evidence_matches_api_contract():
    def handler(request):
        assert request.method == "POST"
        assert request.url.path == "/v1/github/evidence"
        assert request.headers["X-API-Key"] == "test-key"

        body = json.loads(request.read())

        assert body == {
            "repository": "owner/repo",
            "commit_sha": "a" * 40,
            "paths": ["README.md"],
        }

        return httpx.Response(
            200,
            json={
                "service": "JAS-SI Verify",
                "status": "EVIDENCE_INTEGRITY_VERIFIED",
                "verification_scope": "github_commit_and_file_integrity",
                "repository": "owner/repo",
                "commit_sha": "a" * 40,
                "tree_sha": "b" * 40,
                "files_verified": 1,
                "files": [
                    {
                        "path": "README.md",
                        "blob_sha": "c" * 40,
                        "sha256": "d" * 64,
                        "size_bytes": 100,
                        "integrity": "VERIFIED",
                    }
                ],
                "read_only": True,
                "semantic_truth_verified": False,
            },
        )

    client = make_client(handler)

    try:
        result = client.verify_github_evidence(
            repository="owner/repo",
            commit_sha="a" * 40,
            paths=["README.md"],
        )

        assert result["status"] == "EVIDENCE_INTEGRITY_VERIFIED"
        assert result["files_verified"] == 1
        assert result["files"][0]["integrity"] == "VERIFIED"
        assert result["read_only"] is True
        assert result["semantic_truth_verified"] is False
    finally:
        close_client(client)


def test_api_error_preserves_status_code():
    def handler(request):
        return httpx.Response(
            401,
            json={"detail": "Missing or invalid API key"},
        )

    client = make_client(handler)

    try:
        with pytest.raises(JASSIError) as error:
            client.authorize(
                "test-1",
                "read_repository",
                "owner/repository",
            )

        assert error.value.status_code == 401
    finally:
        close_client(client)


def test_protected_endpoint_requires_api_key():
    client = JASSIClient(api_key=None)

    try:
        with pytest.raises(JASSIError):
            client.authorize("test-1", "read_repository", "repository")

        with pytest.raises(JASSIError):
            client.verify("test-1", True)

        with pytest.raises(JASSIError):
            client.verify_github_evidence(
                "owner/repo",
                "a" * 40,
                ["README.md"],
            )
    finally:
        close_client(client)


def test_https_required_for_remote_api():
    with pytest.raises(ValueError):
        JASSIClient(base_url="http://example.com")


def test_localhost_http_allowed():
    client = JASSIClient(base_url="http://localhost:8000")

    try:
        assert client is not None
    finally:
        client.close()


def test_invalid_timeout_rejected():
    with pytest.raises(ValueError):
        JASSIClient(timeout=0)


def test_invalid_success_response_rejected():
    def handler(request):
        return httpx.Response(200, text="not-json")

    client = make_client(handler)

    try:
        with pytest.raises(JASSIError):
            client.health()
    finally:
        close_client(client)


def test_verify_rejects_observed_state_without_evidence_ref():
    client = JASSIClient(api_key="test-key")

    try:
        with pytest.raises(
            ValueError,
            match="must be provided together",
        ):
            client.verify(
                action_id="verify-3",
                claimed_success=True,
                observed_state="completed",
            )
    finally:
        client.close()


def test_verify_rejects_evidence_ref_without_observed_state():
    client = JASSIClient(api_key="test-key")

    try:
        with pytest.raises(
            ValueError,
            match="must be provided together",
        ):
            client.verify(
                action_id="verify-4",
                claimed_success=True,
                evidence_ref="evidence-4",
            )
    finally:
        client.close()


@pytest.mark.parametrize(
    ("repository", "commit_sha", "paths"),
    [
        ("invalid-repo", "a" * 40, ["README.md"]),
        ("owner/repo", "A" * 40, ["README.md"]),
        ("owner/repo", "a" * 40, []),
        ("owner/repo", "a" * 40, ["README.md", "README.md"]),
        ("owner/repo", "a" * 40, ["../secret.txt"]),
        ("owner/repo", "a" * 40, ["/absolute/path"]),
        ("owner/repo", "a" * 40, ["folder\\file.txt"]),
    ],
)
def test_github_evidence_rejects_invalid_inputs(
    repository,
    commit_sha,
    paths,
):
    client = JASSIClient(api_key="test-key")

    try:
        with pytest.raises(ValueError):
            client.verify_github_evidence(
                repository,
                commit_sha,
                paths,
            )
    finally:
        client.close()

