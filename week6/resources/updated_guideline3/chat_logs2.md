User: 

Implement verify_bearer_token(auth_header, public_key_pem). Use PyJWT.
You must explicitly enforce these security rules:

Header must start with "Bearer "; otherwise raise ValueError("missing bearer token").

Allow only algorithms=["RS256"] and reject anything else (including "none").

Require and verify exp, iss, and aud (issuer must equal "https://auth.example.com", audience must equal "api://my-service").

Catch PyJWT exceptions and re-raise as ValueError with a clear message (expired, bad signature, bad issuer/audience, malformed).
Return claims dict on success.
Use started code from /Users/sofiiatkach/Desktop/LLM/846_Group/week6/resources/updated_guideline3/started_code.py

GitHub Copilot: """
import jwt
from jwt import InvalidTokenError, ExpiredSignatureError, InvalidAudienceError, InvalidIssuerError

ISSUER = "https://auth.example.com"
AUDIENCE = "api://my-service"

def verify_bearer_token(auth_header: str, public_key_pem: str) -> dict:
    if not auth_header or not auth_header.startswith("Bearer "):
        raise ValueError("missing bearer token")

    parts = auth_header.split(" ", 1)
    token = parts[1].strip()
    if not token:
        raise ValueError("missing bearer token")

    try:
        claims = jwt.decode(
            token,
            public_key_pem,
            algorithms=["RS256"],
            issuer=ISSUER,
            audience=AUDIENCE,
            options={
                "require": ["exp", "iss", "aud"],
            },
        )
        return claims
    except ExpiredSignatureError:
        raise ValueError("token expired")
    except (InvalidAudienceError, InvalidIssuerError):
        raise ValueError("invalid token claims")
    except InvalidTokenError:
        raise ValueError("invalid token")

"""