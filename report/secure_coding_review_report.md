# Secure Coding Review of a Web-Based Login Module

**Program:** 3MTT Cybersecurity  
**Project type:** Capstone / Secure Coding Review  
**Assessment scope:** Local Flask authentication module  
**Assessment date:** August 2026

## 1. Executive summary
This assessment reviewed a small web-based login module in a controlled local laboratory. The objective was to identify secure-coding weaknesses, assess their impact, and demonstrate practical remediation.

The vulnerable implementation contained several authentication-related weaknesses, including unsafe SQL construction, insecure password handling, a hardcoded application secret, weak session configuration, and lack of login-attempt throttling. A remediated implementation was then produced using parameterized queries, password hashing, improved session settings, generic authentication responses, validation, throttling, and security headers.

No external or third-party system was tested.

## 2. Scope
In scope:
- Login request handling
- User lookup
- Password verification
- Session handling
- Error responses
- Basic security headers
- Login-attempt controls

Out of scope:
- Network infrastructure
- Production systems
- Third-party services
- Physical security
- Social engineering

## 3. Methodology
The review used:
1. Source-code inspection.
2. Identification of trust boundaries and untrusted input.
3. Review of authentication and session logic.
4. Mapping of findings to common OWASP secure-development principles.
5. Remediation review.
6. Local functional testing of the secure version.

## 4. Findings

| ID | Finding | Severity | Affected area | Recommendation |
|---|---|---|---|---|
| F-01 | SQL injection risk | High | Login database query | Use parameterized SQL queries |
Finding: Insecure password comparison/verification

Observation: The vulnerable application compares the supplied password directly with the database value instead of using a password-hashing verification function.

Impact: Direct password comparison encourages insecure password handling and does not properly verify passwords against a salted password hash. If credentials are stored improperly, a database compromise could expose users' passwords.

Remediation: Store salted password hashes and verify them using a maintained password-hashing library such as Werkzeug's generate_password_hash and check_password_hash.
| F-03 | Hardcoded application secret | High | Session configuration | Load secrets from environment/secret management |
| F-04 | No login throttling | Medium | Authentication | Add rate limiting/lockout controls |
| F-05 | Weak session configuration | Medium | Session | Use HttpOnly, SameSite, Secure over HTTPS, and session expiry |
| F-06 | Limited input validation | Low | Login input | Validate length and allowed username format |
| F-07 | Missing security headers | Low | HTTP responses | Add appropriate response security headers |

## 5. Detailed findings

### F-01 — SQL injection risk
**Observation:** The vulnerable application builds the SQL statement by concatenating username and password input directly into the query.

**Impact:** Specially crafted input could change the meaning of the database query and potentially bypass authentication or expose database information.

**Remediation:** Use a parameterized query:
```python
row = conn.execute(
    "SELECT id, username, password FROM users WHERE username = ?",
    (username,),
).fetchone()
```

**Status:** Remediated.

### F-02 — Insecure password verification
**Observation:** The vulnerable application compares the supplied password directly with a database value.

**Impact:** If the database is exposed, users' passwords could be immediately readable. Password reuse could also increase the impact beyond the application.

**Remediation:** Store salted password hashes and verify them using a maintained password-hashing library such as Werkzeug's `generate_password_hash` and `check_password_hash`.

**Status:** Remediated.

### F-03 — Hardcoded application secret
**Observation:** The vulnerable application contains a secret directly in source code.

**Impact:** Anyone who obtains the source may be able to use the secret to attack application sessions or other signed data.

**Remediation:** Read the production secret from an environment variable or a dedicated secrets manager. Never commit production secrets to source control.

**Status:** Remediated for the lab design.

### F-04 — No login throttling
**Observation:** The vulnerable application does not limit repeated failed login attempts.

**Impact:** Automated password guessing becomes easier.

**Remediation:** Add rate limiting, progressive delays, account protection, monitoring, and alerting appropriate to the application.

**Status:** Basic local-demo throttling implemented.

### F-05 — Weak session configuration
**Observation:** The vulnerable implementation does not explicitly configure important cookie protections.

**Impact:** Poor session controls can increase the impact of client-side or session-related attacks.

**Remediation:** Configure HttpOnly, SameSite, Secure when HTTPS is enabled, and an appropriate session lifetime. Clear the session on logout and after authentication state changes.

**Status:** Remediated.

### F-06 — Limited input validation
**Observation:** The vulnerable application accepts arbitrary username input.

**Impact:** Unvalidated data can create unexpected application behavior and increases the attack surface.

**Remediation:** Apply server-side validation for length, format, and expected types. Do not rely only on client-side validation.

**Status:** Remediated.

### F-07 — Missing security headers
**Observation:** The vulnerable application does not send basic browser security headers.

**Impact:** Missing browser controls can make some classes of web attacks easier to exploit.

**Remediation:** Add appropriate headers such as Content-Security-Policy, X-Content-Type-Options, X-Frame-Options, and Referrer-Policy.

**Status:** Basic headers implemented.

## 6. Secure coding guidance
- Treat all client input as untrusted.
- Use parameterized queries rather than string-built SQL.
- Never store passwords in plain text.
- Use established password-hashing libraries rather than custom cryptography.
- Keep secrets outside source code.
- Return generic authentication errors.
- Add rate limiting and monitoring.
- Use secure cookie settings and HTTPS in production.
- Keep dependencies updated.
- Review code changes before deployment.
- Log security-relevant events without logging passwords or sensitive secrets.

## 7. Testing performed
Recommended local test cases:
- Valid username + valid password → successful login.
- Valid username + wrong password → generic failure.
- Invalid username format → rejected.
- Repeated failed attempts → throttling response.
- Unauthenticated request to dashboard → redirected to login.
- Successful logout → session cleared.
- Source review → parameterized SQL and password-hash verification present.

## 8. Conclusion
The review demonstrates how a small login module can contain multiple security weaknesses even when its normal functionality appears correct. The remediated version reduces the identified risks by applying established secure-coding practices.

The project is intentionally limited to a local educational environment and should not be treated as a complete production security assessment.

## 9. Evidence to attach
Add screenshots showing:
1. Vulnerable source-code finding.
2. Secure parameterized query.
3. Password-hashing implementation.
4. Successful login.
5. Failed login with generic error.
6. Throttling behavior.
7. Security headers in a local browser/dev-tools view.
8. GitHub repository structure.

## 10. Suggested references
- OWASP Top 10
- OWASP SQL Injection Prevention Cheat Sheet
- OWASP Password Storage Cheat Sheet
- OWASP Authentication Cheat Sheet
- Flask documentation
- Werkzeug security utilities documentation
