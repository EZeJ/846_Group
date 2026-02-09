User: 
> “Write a docstring summary for `verify_reset_token` intended for a public authentication API.
> Rules:
>
> 1. If the function is security/auth related (token/auth/password/reset), the summary MUST include: (a) one key security property, (b) side effects if any, and (c) failure modes/raised exceptions.
> 2. Do not describe cryptographic internals, but do state externally observable behavior (one-time use, expiration).
>    Keep it 2–4 sentences.  All code in week5/resources/updated_guideline5/auth_reset.py

GitHub Copilot: """
Validates a password reset token and returns the corresponding user ID on success.
Tokens are one-time use: a successful verification marks the token as used (state change) and prevents reuse.
Raises InvalidTokenError for malformed/unknown/bad-signature/already-used tokens, and ExpiredTokenError when the token is past its expiry time.
"""