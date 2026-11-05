import httpx
import pytest

from jas_si_community_python import JASSIClient, JASSIError


def make_client(handler):
    transport = httpx.MockTransport(handler)

    client = JASSIClient(api_key="test-key")
    client._client.close()
    client._client = httpx.Client(
        base_url="https://api.example.test",
        headers={"X-API-Key": "test-key"},
        transport=transport,
    )
    return client


def test_health():
    def handler(request):
        assert request.url.path == "/health"
        return httpx.Response(
            200,
            json={"status": "ok", "api_enabled": True},
        )

    client = make_client(handler)

    try:
        assert client.health()["status"] == "ok"
    finally:
        client.close()


def test_authorize():
    def handler(request):
        assert request.headers["X-API-Key"] == "test-key"
        assert request.url.path == "/v1/authorize"

        body = request.read().decode()
        assert '"action_id":"test-1"' in body

        return httpx.Response(
            200,
            json={
                "action_id": "test-1",
                "allowed": True,
                "executed": False,
            },
        )

    client = make_client(handler)

    try:
        result = client.authorize(
            "test-1",
            "read_repository",
            "document",
        )
        assert result["allowed"] is True
        assert result["executed"] is False
    finally:
        client.close()


def test_api_error():
    def handler(request):
        return httpx.Response(
            401,
            json={"detail": "Missing or invalid API key"},
        )

    client = make_client(handler)

    try:
        with pytest.raises(JASSIError) as error:
            client.authorize("test-1", "read_repository", "document")

        assert error.value.status_code == 401
    finally:
        client.close()


def test_protected_endpoint_requires_key():
    client = JASSIClient(api_key=None)

    try:
        with pytest.raises(JASSIError):
            client.authorize("test-1", "read_repository", "document")
    finally:
        client.close()


def test_verify():
    def handler(request):
        assert request.url.path == "/v1/verify"
        assert request.headers["X-API-Key"] == "test-key"

        import json
        body = json.loads(request.read())

        assert body["action_id"] == "verify-1"
        assert body["claimed_success"] is True
        assert body["observed_state"] == "completed"
        assert body["evidence_ref"] == "evidence-1"

        return httpx.Response(
            200,
            json={
                "action_id": "verify-1",
                "status": "INCONCLUSIVE",
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
        assert result["status"] == "INCONCLUSIVE"
    finally:
        client.close()


def test_github_evidence():
    def handler(request):
        import json
        body = json.loads(request.read())

        assert request.url.path == "/v1/github/evidence"
        assert body["repository"] == "owner/repo"
        assert body["commit_sha"] == "a" * 40
        assert body["paths"] == ["README.md"]

        return httpx.Response(
            200,
            json={
                "status": "EVIDENCE_INTEGRITY_VERIFIED",
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
        assert result["semantic_truth_verified"] is False
    finally:
        client.close()


def test_https_required_for_remote_api():
    with pytest.raises(ValueError):
        JASSIClient(base_url="http://example.com")


def test_invalid_timeout_rejected():
    with pytest.raises(ValueError):
        JASSIClient(timeout=0)


def test_verify_requires_api_key():
    client = JASSIClient(api_key=None)

    try:
        with pytest.raises(JASSIError):
            client.verify("verify-1", True)
    finally:
        client.close()
