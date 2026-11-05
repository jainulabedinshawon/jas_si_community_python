Changelog

All notable changes to JAS-SI Community Python SDK are documented in this file.

This project follows "Semantic Versioning" (https://semver.org/).


[0.1.1] - 2026-11-06

Changed

- Updated the SDK package version to 0.1.1.
- Adopted modern PEP 639 license metadata using Apache-2.0.
- Aligned the runtime package version with project metadata.

Added

- Added automated package build validation for wheel and source distributions.
- Added wheel content and license metadata checks.
- Added isolated wheel installation and package smoke tests.
- Added automated validation of the built package version and Python compatibility metadata.

[0.1.0] - 2026-11-06

Added

- Initial public release of the independent JAS-SI Community Python SDK.
- "JASSIClient" for communicating with the JAS-SI REST API.
- "JASSIError" for structured API and connection error handling.
- API health-check support through "health()".
- Authorization evaluation through "authorize()".
- Outcome verification through "verify()".
- GitHub commit and file-integrity verification through "verify_github_evidence()".
- Context-manager support for automatic HTTP client cleanup.
- Configurable request timeout.
- Python 3.10+ support.
- Automated test suite using "pytest" and "httpx.MockTransport".
- GitHub Actions CI across Python 3.10, 3.11, 3.12, and 3.13.

Security

- Enforced HTTPS for non-local API connections.
- Required API keys for protected endpoints.
- Added client-side validation for paired verification evidence inputs.
- Added validation for GitHub repository identifiers, full commit SHAs, and evidence file paths.
- Rejected duplicate, absolute, and unsafe relative evidence paths.
- Added handling for request timeouts, connection failures, unsuccessful HTTP responses, and invalid JSON responses.

API Compatibility

- Aligned SDK request payloads and response expectations with the JAS-SI API contracts.
- Preserved the API's authorization and verification response fields.
- Documented that authorization evaluation does not execute external actions.
- Documented that caller-submitted evidence is not independently collected.
- Clarified that GitHub evidence verification establishes commit and file integrity, not semantic truth.

Scope and Limitations

- This SDK is an independent HTTP client; it does not contain or reimplement JAS-SI Core logic.
- The SDK does not execute external actions.
- Verification results depend on the evidence and capabilities provided by the JAS-SI API.
- The SDK does not independently establish the truth of caller-submitted claims.

---
