User: Implement verify_bearer_token(auth_header, public_key_pem).
Use PyJWT (jwt package) to decode and verify JWTs.
Purpose: parse the token and validate it.
Raise ValueError when invalid. 
Use started code from /Users/sofiiatkach/Desktop/LLM/846_Group/week6/resources/updated_guideline3/started_code.py

GitHub Copilot: 
"""
import jwt

def verify_bearer_token(auth_header: str, public_key_pem: str) -> dict:
    token = auth_header.split(" ")[1]
    # decode token
    claims = jwt.decode(token, public_key_pem, algorithms=["RS256"], options={"verify_signature": True})
    return claims

"""
