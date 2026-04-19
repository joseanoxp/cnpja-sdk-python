# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly.

**Do not open a public issue.**

Instead, contact the maintainer directly at: **joseanodev@gmail.com**

Please include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

You should receive a response within 48 hours.

## Supported Versions

| Version | Supported |
|---|---|
| Latest tag on `main` | Yes |

## Handling of secrets

This SDK never persists the API key to disk. Consumers must pass the key via `Client(api_key=...)` and should keep it in environment variables, secret managers, or equivalent safe storage — **never committed to the repository**.
