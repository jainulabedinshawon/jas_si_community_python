"""HTTP client for the JAS-SI REST API."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlsplit

import httpx


class JASSIError(Exception):
    """Error returned by the JAS-SI API."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code


class JASSIClient:
    """Independent HTTP client; does not implement JAS-SI Core logic."""

    def __init__(
        self,
        base_url: str = "https://jas-si.vercel.app",
        api_key: str | None = None,
        timeout: float = 10.0,
    ) -> None:
        parsed = urlsplit(base_url)

        if parsed.scheme not in {"https", "http"} or not parsed.netloc:
            raise ValueError("A valid API base URL is required.")

        if parsed.scheme != "https" and parsed.hostname not in {
            "localhost",
            "127.0.0.1",
            "::1",
        }:
            raise ValueError("HTTPS is required for non-local API URLs.")

        if timeout <= 0:
            raise ValueError("timeout must be greater than zero.")

        headers = {"Accept": "application/json"}

        if api_key:
            headers["X-API-Key"] = api_key

        self._client = httpx.Client(
            base_url=base_url.rstrip("/"),
            headers=headers,
            timeout=timeout,
        )

        self._has_api_key = bool(api_key)

    def _require_api_key(self) -> None:
        if not self._has_api_key:
            raise JASSIError(
                "An API key is required for this endpoint."
            )

    def _request(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        try:
            response = self._client.request(
                method,
                path,
                json=payload,
            )
        except httpx.TimeoutException as exc:
            raise JASSIError("JAS-SI API request timed out.") from exc
        except httpx.RequestError as exc:
            raise JASSIError("Unable to connect to JAS-SI API.") from exc

        try:
            data = response.json()
        except ValueError:
            data = None

        if not response.is_success:
            detail = (
                data.get("detail", "JAS-SI API request failed.")
                if isinstance(data, dict)
                else "JAS-SI API request failed."
            )
            raise JASSIError(str(detail), response.status_code)

        if not isinstance(data, dict):
            raise JASSIError(
                "Invalid or empty JSON response from JAS-SI API.",
                response.status_code,
            )

        return data

    def health(self) -> dict[str, Any]:
        """Check public API health."""
        return self._request("GET", "/health")

    def authorize(
        self,
        action_id: str,
        action: str,
        resource: str,
    ) -> dict[str, Any]:
        """Request an authorization evaluation. Does not execute actions."""
        self._require_api_key()

        return self._request(
            "POST",
            "/v1/authorize",
            {
                "action_id": action_id,
                "action": action,
                "resource": resource,
            },
        )

    def verify(
        self,
        action_id: str,
        claimed_success: bool,
        observed_state: str | None = None,
        evidence_ref: str | None = None,
    ) -> dict[str, Any]:
        """Submit an outcome report for verification."""
        self._require_api_key()

        if (observed_state is None) != (evidence_ref is None):
            raise ValueError(
                "observed_state and evidence_ref must be "
                "provided together."
            )

        payload: dict[str, Any] = {
            "action_id": action_id,
            "claimed_success": claimed_success,
        }

        if observed_state is not None and evidence_ref is not None:
            payload["observed_state"] = observed_state
            payload["evidence_ref"] = evidence_ref

        return self._request("POST", "/v1/verify", payload)

    def verify_github_evidence(
        self,
        repository: str,
        commit_sha: str,
        paths: list[str],
    ) -> dict[str, Any]:
        """Verify GitHub commit and file integrity."""
        self._require_api_key()

        if not isinstance(repository, str) or not (
            3 <= len(repository) <= 200
        ):
            raise ValueError("Invalid GitHub repository format.")

        if not re.fullmatch(
            r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+",
            repository,
        ):
            raise ValueError("Invalid GitHub repository format.")

        if not isinstance(commit_sha, str) or not re.fullmatch(
            r"[0-9a-f]{40}",
            commit_sha,
        ):
            raise ValueError(
                "A full 40-character lowercase commit SHA is required."
            )

        if not isinstance(paths, list) or not 1 <= len(paths) <= 10:
            raise ValueError(
                "Between 1 and 10 evidence files are required."
            )

        if len(set(paths)) != len(paths):
            raise ValueError("Duplicate evidence paths are not allowed.")

        for path in paths:
            if (
                not isinstance(path, str)
                or not path
                or len(path) > 500
                or path.startswith("/")
                or "\\" in path
                or "\x00" in path
                or any(part in ("", ".", "..") for part in path.split("/"))
            ):
                raise ValueError("Invalid repository file path.")

        return self._request(
            "POST",
            "/v1/github/evidence",
            {
                "repository": repository,
                "commit_sha": commit_sha,
                "paths": paths,
            },
        )

    def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        self._client.close()

    def __enter__(self) -> "JASSIClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
