# Security

Security matters for this project, especially because it handles webhook data and secrets.

If you find a security issue, please report it responsibly.

---

## Reporting a Security Issue

Please **do not open a public GitHub issue** for security vulnerabilities.

Instead:
- Use GitHub Security Advisories, or
- Contact the maintainer privately (if contact details are provided)

When reporting, include:
- what the issue is
- how it can be reproduced (if possible)
- what impact it might have

---

## Built-in Security Features

This project includes several basic security protections:

- Telegram webhook secret token verification
- Optional outbound HMAC signature (`X-Gateway-Signature`)
- Rate limiting per chat
- Maximum request body size limits
- Optional allowlist of authorized chat IDs
- Immediate `200 OK` response to Telegram to avoid abuse retries

---

## User Responsibilities

You are responsible for:
- Keeping `BOT_TOKEN` and secrets private
- Rotating secrets if they are exposed
- Verifying webhook signatures on your own backend
- Securing your deployed instance (firewalls, access control, etc.)

---

## Out of Scope

The following are not considered security issues for this project:
- Compromised Telegram accounts
- Security of third-party webhook receivers
- Misconfigured deployments
- Weak or reused secrets

---

## Supported Versions

Only the latest version on the main branch is supported.
Security fixes will be applied to the latest version.

---

Thanks for helping keep the project secure.