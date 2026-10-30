# Production Security Checklist

## Required before public launch

- [ ] Replace development JWT and database credentials with unique secrets from a secret manager.
- [ ] Set `APP_ENV=production` and configure the exact `ALLOWED_HOSTS` values.
- [ ] Terminate TLS at a maintained reverse proxy/load balancer; redirect HTTP to HTTPS.
- [ ] Restrict database and API network access to trusted application networks.
- [ ] Configure request rate limits at the ingress and API layers.
- [ ] Add email verification, password reset, token revocation/rotation, and account recovery.
- [ ] Review password policy, account lockout/abuse handling, and login telemetry.
- [ ] Add CSRF protection if browser authentication later uses cookies.
- [ ] Review CORS, CSP, HSTS, cookie, and proxy settings for the final domain and frontend assets.
- [ ] Configure secrets scanning and dependency vulnerability scanning in CI.
- [ ] Avoid logging passwords, tokens, precise location, or private trip details.
- [ ] Define retention and deletion policies for user and location data.
- [ ] Review LLM provider data handling and prompt-injection defenses.
- [ ] Restrict tourism-document ingestion to authorized administrators.
- [ ] Add authorization tests for every user-owned resource.
- [ ] Verify backup encryption, restore procedures, and recovery objectives.
- [ ] Conduct a security review and staging penetration test.

## Known implementation limitations

This starter uses signed JWT access tokens but does not yet implement refresh-token rotation, revocation, email verification, password reset, or an admin role. CORS is configured through environment variables. Nginx is a simple HTTP reverse proxy and does not terminate TLS. Configure the deployment platform's edge proxy and security policy before public release.
