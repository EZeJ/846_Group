User:
```
Review the authenticate_user() function in auth.py.

The docstring makes these claims about the implementation:
  1. Passwords are stored as SHA-256 hashes
  2. Hash comparison is constant-time to prevent timing attacks
  3. Returns True on success, False otherwise

Do not take these claims at face value — verify each one against the actual code.

For claim 2: find the exact line where hashes are compared and check whether
it is actually constant-time in CPython. If not, explain how an attacker could
exploit this and suggest the correct fix.

Also check any database queries in the function — if user input is being
inserted directly into a query string, flag it as SQL injection even if the
docstring doesn't mention it.

If the code doesn't deliver on a security claim made in the docstring, treat
that as BUG FIX / P1. A false security claim in documentation is dangerous
on its own because it makes reviewers trust code they shouldn't.

Format each finding as: [Category | Priority] Location → What → Why → Fix
```

GitHub Copilot:

Read [] file:///Users/sofiiatkach/Desktop/LLM/846_Group/week10/src/problem_B/auth.py

> **Review of `authenticate_user()`**
>
> ---
>
> **Verifying docstring claims against implementation:**
>
> **Finding 1** — `[BUG FIX | P1 — block merge]`
> **Location:** `auth.py:authenticate_user`, line 48
> **What:** SQL injection via f-string interpolation.
> **Why:** The query `f"SELECT password_hash FROM users WHERE username = '{username}'"` inserts the user-supplied `username` directly into the SQL string. An attacker can supply `' OR '1'='1' --` as the username to bypass authentication entirely, or `'; DROP TABLE users; --` to destroy data. This is a direct, unauthenticated exploit.
> **Fix:** Use a parameterised query:
> ```python
> cursor.execute(
>     "SELECT password_hash FROM users WHERE username = ?",
>     (username,)
> )
> ```
>
> **Finding 2** — `[BUG FIX | P1 — block merge]`
> **Location:** `auth.py:authenticate_user`, line 54
> **What:** Docstring claims constant-time comparison; implementation uses `==`, which is not constant-time.
> **Why:** Python's `==` on strings short-circuits on the first differing byte. An attacker who can measure response-time differences (e.g., via repeated login requests) can infer how many leading bytes of their guessed hash match the stored hash, and incrementally reconstruct it. The docstring's false claim means every reviewer who read it — human or LLM — would have accepted this line as correct. The misleading documentation is itself a security risk.
> **Fix:**
> ```python
> import hmac
> return hmac.compare_digest(stored_hash, password_hash)
> ```
> `hmac.compare_digest` is guaranteed constant-time in CPython regardless of string content.
>
> **Finding 3** — `[BUG FIX | P2]`
> **Location:** `auth.py:authenticate_user`, lines 43–44 and `get_user_posts`, line 73
> **What:** SHA-256 is not a password hashing function. The same f-string SQL injection pattern also appears in `get_user_posts`.
> **Why:** SHA-256 has no salt and is designed for speed, making it trivially brute-forced with GPU rigs. `get_user_posts` repeats the injection pattern from Finding 1.
> **Fix:** Replace SHA-256 with `bcrypt` or `argon2-cffi` for password storage. Apply parameterised queries to `get_user_posts` identically to Finding 1.
>
> **Finding 4** — `[ENHANCEMENT | P2]`
> **Location:** `auth.py:generate_reset_token`, line 62
> **What:** `random.choices` is not cryptographically secure.
> **Why:** Python's `random` module uses a Mersenne Twister PRNG, which is not suitable for security tokens. An attacker who observes enough tokens can predict future ones.
> **Fix:** Replace with `secrets.token_urlsafe(8)`.
>
> **Finding 5** — `[DOCUMENTATION | P1]`
> **Location:** `auth.py:authenticate_user` docstring
> **What:** Docstring falsely asserts constant-time comparison.
> **Why:** A false security claim in a docstring actively misleads reviewers into approving unsafe code with higher confidence than if there were no claim at all. It must be corrected before merge to prevent future reviewers from repeating this error.
> **Fix:** Replace the false claim with an accurate description after implementing `hmac.compare_digest`.
>
> ---
>
> **Verdict: Reject.**
> Three P1 findings must be resolved before this PR can merge:
> SQL injection in `authenticate_user` (Finding 1), non-constant-time
> hash comparison (Finding 2), and the actively misleading docstring
> (Finding 5). Finding 3 (SHA-256, second injection site) must also be
> resolved or explicitly deferred with a tracked issue.
