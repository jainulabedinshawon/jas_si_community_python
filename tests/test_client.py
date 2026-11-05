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
            "read",
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
            client.authorize("test-1", "read", "document")

        assert error.value.status_code == 401
    finally:
        client.close()


def test_protected_endpoint_requires_key():
    client = JASSIClient(api_key=None)

    try:
        with pytest.raises(JASSIError):
            client.authorize("test-1", "read", "document")
    finally:
        client.close()
