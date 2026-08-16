# 3MTT Capstone Presentation Outline

## Slide 1 — Title
Secure Coding Review of a Web-Based Login System
3MTT Cybersecurity Capstone

## Slide 2 — Problem
Poorly written authentication code can expose users and applications to common web attacks.

## Slide 3 — Aim and objectives
Review the login module, identify weaknesses, implement fixes, and document the results.

## Slide 4 — Technology
Python, Flask, SQLite, Werkzeug, Git/GitHub.

## Slide 5 — Scope and methodology
Source-code review, authentication-flow review, risk assessment, remediation, and local testing.

## Slide 6 — Key findings
SQL injection, insecure password handling, hardcoded secret, missing throttling, weak session controls, limited validation, missing security headers.

## Slide 7 — High-risk example
Show the vulnerable SQL construction and explain why untrusted input must not be concatenated into SQL.

## Slide 8 — Remediation
Show parameterized SQL and password-hash verification.

## Slide 9 — Additional controls
Rate limiting, secure cookies, generic errors, input validation, security headers, secret management.

## Slide 10 — Testing
Valid login, invalid login, validation, throttling, logout, session protection.

## Slide 11 — Results
Summarize which findings were remediated and what secure-coding lessons were learned.

## Slide 12 — Conclusion
Secure coding is a continuous process. Authentication code should be reviewed, tested, and maintained throughout the software lifecycle.
