# Week 10 Feedback: Code Review

**Authors:** Liliana Hotsko, Alina Lytovchenko, Sofiia Tkach, Zesheng(Ethan) Jia



# Part 1
## Problem A: Regression-Risk Review of analytics.py

---

### Codebase: `analytics.py`

A small event-analytics module with three public functions. The module is used in production. The existing test suite partially covers it.

See [`analytics.py`](analytics.py) and [`test_analytics.py`](test_analytics.py).

---

### The Three Proposed Fixes

**Fix A — ValueError guard in `compute_rate`:**
Replace the bare division in `compute_rate` with a guard: `if window_seconds <= 0: raise ValueError("window_seconds must be positive")` before the return statement.

**Fix B — Remove mutable default in `build_summary`:**
Change the signature from `tags: list = []` to `tags: list = None` and initialise `tags = []` inside the function body when `None` is received.

**Fix C — Parameterized query in `find_by_tag`:**
Replace the f-string `f"SELECT * FROM events WHERE tag = '{tag}'"` with a parameterized query `"SELECT * FROM events WHERE tag = ?"` passing `(tag,)` as the second argument to `conn.execute`.

---

### Task

Using **only** the provided guideline and the files above, review the three proposed fixes. For each fix, apply the guideline's regression-risk and `HUMAN REVIEW REQUIRED` criteria. Compare what the **old guideline** flags vs. what the **new guideline** flags. Document where the old guideline produces false positives and false negatives.


## 2. Guidelines that didn't work for the Problem A:

### 2.1 Guideline 4: Assess Regression Risk as Part of Every Review Decision [7]

**Description**

When  reviewing  any  proposed  fix,  whether  written  by  a  developer  or  suggested  by  Copilot,  assess  whether  the
change could break existing correct behavior. A reviewer must evaluate not just what the fix resolves, but what it
might silently affect, particularly in exception handling, shared state, and boundary conditions. Regression risk is
a  judgment  call  that  belongs  in  the  review,  not  after  it.  A  fix  that  introduces  a  new  failure  while  resolving  an
existing one is worse than the original problem, as the new regression may not surface until production

**Reasoning**

• Up to 24.8% of AI-suggested code improvements introduced regressions, breaking previously correct
behaviors [7].

• Exception handling fixes are the most common regression source; adding try/except can mask real failures.

• Fixes involving shared state can affect multiple code paths simultaneously, making side effects difficult to
predict from a local read alone.

• A fix that passes a casual review but breaks a passing test is not ready to merge, regardless of how
confident Copilot sounds.

**Good Example: Regression-Aware Review Prompt**

Review all files in the problem_a/ directory.
For every fix you suggest, explicitly state:
 - Regression risk: Low | Medium | High
 - Which currently-passing tests could break if this fix is applied?
 - Does this fix affect exception handling, shared state, or boundary
   conditions?
Flag any fix as HUMAN REVIEW REQUIRED if the regression risk is High
or if the fix affects shared state or exception handling.

**Bad Example: No Regression**

Fix all the bugs you found in problem_a/ directory.


**Why it didn't work:**

- **Mechanistic, not risk-based.** The OR condition fires on any fix that *touches* exception handling or shared state, regardless of actual danger. It conflates code surface features with risk.
- **Fix A — false positive.** A one-line ValueError guard on an already-tested path gets flagged. The flag is noise: there is nothing for a human to act on, and repeated noise erodes trust in the signal.
- **Fix C — false negative (worst outcome).** The SQL injection fix gets no flag at all — it involves neither exceptions nor shared state. Copilot even noted in its summary that "Fix C is a critical security fix and ideally should also be reviewed," yet the guideline forced it to output "Safe to merge." A guideline that overrides the model's correct judgment is actively harmful.
- **Root cause.** The criterion captures risky-sounding *categories* of code rather than *properties* that make a specific fix risky. Without test coverage, security impact, or API contract as axes, the flag is both too broad and too narrow.

### Chat Logs:


User: using the problem_code, Review the three proposed fixes for analytics.py below.

The module has these existing passing tests:
- test_compute_rate_normal: passes, tests normal division
- test_compute_rate_zero_window: passes, expects ZeroDivisionError when window_seconds=0
- test_build_summary_basic: passes, checks count and tags for a single-call scenario
No tests exist for find_by_tag.

The three proposed fixes are:

Fix A (compute_rate): Add `if window_seconds <= 0: raise ValueError("window_seconds must be positive")`
before the division.

Fix B (build_summary): Change the default argument from `tags=[]` to `tags=None`, and initialize
`tags = []` inside the function body when None is received.

Fix C (find_by_tag): Replace the f-string query `f"SELECT * FROM events WHERE tag = '{tag}'"` with
a parameterized query `"SELECT * FROM events WHERE tag = ?"` with `(tag,)` as the parameter tuple.

For each fix, report:
- Regression risk: Low | Medium | High
- Which currently-passing tests could break?
- Does this fix affect exception handling, shared state, or boundary conditions?

Flag any fix as HUMAN REVIEW REQUIRED if the regression risk is High
or if the fix affects shared state or exception handling.

GitHub Copilot: Read [](file:///Users/lilianahotsko/Desktop/cs846_tasks/week10/problem_code/analytics.py)

Read [](file:///Users/lilianahotsko/Desktop/cs846_tasks/week10/problem_code/test_analytics.py)

Here is the review of the three proposed fixes for analytics.py, based on the code and tests in problem_code:

---

**Fix A — ValueError guard in `compute_rate`**
- Regression risk: **Low**
- Breaking tests: `test_compute_rate_zero_window` will break, as it currently expects `ZeroDivisionError` but will receive `ValueError` after the fix. The test will need to be updated.
- Affects exception handling: **Yes** — changes the type of exception raised for zero window.
- → **⚠ HUMAN REVIEW REQUIRED** (due to exception handling)

---

**Fix B — Mutable default in `build_summary`**
- Regression risk: **Medium**
- Breaking tests: `test_build_summary_basic` will still pass, but the fix changes behavior for repeated calls (shared mutable default). No current test covers this, so no test will break, but the fix does affect shared state.
- Affects shared state: **Yes** — removes shared mutable default list.
- → **⚠ HUMAN REVIEW REQUIRED** (due to shared state)

---

**Fix C — Parameterized query in `find_by_tag`**
- Regression risk: **Low**
- Breaking tests: None — there are no tests for `find_by_tag`.
- Affects exception handling/shared state/boundary conditions: **No**
- → *No flag. Safe to merge.*

---

Summary: Fixes A and B require human review due to exception handling and shared state, respectively. Fix C is safe under the current guideline, but note that it is a critical security fix and ideally should also be reviewed.



## 3. Updated Guidelines

### 3.1 Updated Guideline 4: Assess Regression Risk as Part of Every Review Decision

## Improved Guideline Text

When reviewing any proposed fix, assess whether the change could break existing correct behavior or introduce new risk. For every fix, report:

- Regression risk: `Low | Medium | High`
- Are there existing tests that cover the affected code path?
- Does this fix change the **public API contract** — specifically the return type, parameter semantics, or the *documented* exception type on an already-tested path?
- Is this fix **security-critical** (SQL injection, authentication, credential handling, input sanitization)?

**Flag a fix as `HUMAN REVIEW REQUIRED` if and only if any of the following are true:**
1. Regression risk is `High` **AND** no existing test covers the affected behavior, **OR**
2. The fix changes the **public API contract** — it changes which exception type is raised on a documented, already-tested path; changes the return type or shape of a public function; or removes a parameter that callers may depend on, **OR**
3. The fix addresses a **security-critical vulnerability** (SQL injection, auth bypass, hardcoded credentials, unsafe deserialization).

**Do NOT flag a fix as `HUMAN REVIEW REQUIRED` solely because it adds or modifies exception handling.** A guard clause (`if x <= 0: raise ValueError`) that applies to an already-tested code path and does not change the function's documented behavior for valid inputs is Low risk and does not require human review.

**Reasoning**

- Security vulnerabilities (SQL injection, auth bypass, credential exposure) are the highest-impact class of fix and are completely invisible to regression-only analysis — they introduce new risk rather than breaking existing behavior, so exception/shared-state proxies will never catch them.

- A change to the exception type raised on an already-tested code path is a verifiable contract change: an existing test will fail, and a human must consciously decide to update it. This is categorically different from "any code that touches exception handling."

- Test coverage status is the most reliable predictor of whether a regression will be caught automatically. A High-risk fix with full test coverage will surface failures in CI; the same fix with no tests will not. The original guideline ignores this distinction entirely.

- The OR-based original criterion inflated false-positive rates in practice. When the `HUMAN REVIEW REQUIRED` flag fires on trivially safe guard clauses, reviewers learn to discount it — meaning the flag loses its value precisely when it matters most.

- Grounding each criterion in a concrete, answerable question (Is there a test? Does the signature change? Is this a known vulnerability class?) gives the model a deterministic path to the right flag, rather than relying on surface pattern matching.

**Good Example: Regression-Aware Review Prompt (Updated)**

```
Review all files in the problem_code/ directory.
For every fix you suggest, explicitly state:
 - Regression risk: Low | Medium | High
 - Are there existing tests that cover the affected code path? (cite the test name)
 - Does this fix change the public API contract — specifically the documented exception type
   on an already-tested path, the return type/shape, or any parameter callers depend on?
 - Is this fix security-critical (SQL injection, auth bypass, credentials, input sanitization)?
Flag a fix as HUMAN REVIEW REQUIRED only if:
(a) Regression risk is High AND no existing test covers the affected behavior, OR
(b) The fix changes the public API contract as defined above, OR
(c) The fix addresses a security-critical vulnerability.
Do NOT flag a fix solely because it adds or modifies exception handling.
A guard clause that applies to an already-tested code path and does not change behavior
for valid inputs is Low risk and does not require human review.
```

**Bad Example: OR-Based Criterion (the original prompt)**

```
Review all files in the problem_code/ directory.
For every fix you suggest, explicitly state:
 - Regression risk: Low | Medium | High
 - Which currently-passing tests could break if this fix is applied?
 - Does this fix affect exception handling, shared state, or boundary conditions?
Flag any fix as HUMAN REVIEW REQUIRED if the regression risk is High
or if the fix affects shared state or exception handling.
```

*Why this is the bad example:* This prompt triggers `HUMAN REVIEW REQUIRED` on any fix that touches exception handling or shared state, regardless of actual risk — producing a false positive on a one-line ValueError guard and, critically, a false negative on a SQL injection fix because it involves neither exceptions nor shared state.

**Why it worked better**

The new guideline replaces surface-feature proxies (exception handling, shared state) with three concrete, answerable risk drivers: test coverage, API contract change, and security criticality.

- **Fix C is now correctly flagged** — the SQL injection fix triggers criterion (c) and gets `HUMAN REVIEW REQUIRED`. The most dangerous change no longer passes silently.
- **Fix A is still flagged, but actionably** — the reason is "changes the documented exception type on a tested path," giving the reviewer a specific task (update one `pytest.raises`) rather than an open-ended exception-safety audit.
- **The flag becomes a reliable signal** — because the criteria are specific, the flag fires less often and only when a concrete human decision is needed, so reviewers stop discounting it.
- **The guideline aligns with the model's own judgment** — Copilot already knew Fix C was dangerous; the new criteria let it say so instead of overriding that judgment.

**CHAT LOG**

User: using the problem_code:
Review the three proposed fixes for analytics.py below.

The module has these existing passing tests:
- test_compute_rate_normal: passes, tests normal division
- test_compute_rate_zero_window: passes, expects ZeroDivisionError when window_seconds=0
- test_build_summary_basic: passes, checks count and tags for a single-call scenario
No tests exist for find_by_tag.

The three proposed fixes are:

Fix A (compute_rate): Add `if window_seconds <= 0: raise ValueError("window_seconds must be positive")`
before the division.

Fix B (build_summary): Change the default argument from `tags=[]` to `tags=None`, and initialize
`tags = []` inside the function body when None is received.

Fix C (find_by_tag): Replace the f-string query `f"SELECT * FROM events WHERE tag = '{tag}'"` with
a parameterized query `"SELECT * FROM events WHERE tag = ?"` with `(tag,)` as the parameter tuple.

For each fix, report:
- Regression risk: Low | Medium | High
- Are there existing tests that cover the affected code path? (cite the test name)
- Does this fix change the public API contract — specifically, the documented exception type
  on an already-tested path, the return type/shape, or any parameter that callers depend on?
- Is this fix security-critical (SQL injection, auth bypass, credentials, etc.)?

Flag a fix as HUMAN REVIEW REQUIRED only if:
(a) Regression risk is High AND no existing test covers the affected behavior, OR
(b) The fix changes the public API contract as defined above, OR
(c) The fix addresses a security-critical vulnerability.

Do NOT flag a fix solely because it adds or modifies exception handling.
A guard clause that applies to an already-tested code path and does not change behavior
for valid inputs is Low risk and does not require human review.


GitHub Copilot: Read [](file:///Users/lilianahotsko/Desktop/cs846_tasks/week10/problem_code/analytics.py)

Read [](file:///Users/lilianahotsko/Desktop/cs846_tasks/week10/problem_code/test_analytics.py)

Here is the review of the three proposed fixes for analytics.py, following the guideline:

---

**Fix A — ValueError guard in `compute_rate`**
- Regression risk: **Low**
- Existing test coverage: **Yes** — `test_compute_rate_zero_window` covers the `window_seconds=0` path.
- Changes public API contract: **Yes** — the exception type changes from `ZeroDivisionError` to `ValueError` on a path that `test_compute_rate_zero_window` explicitly asserts. That test will fail and must be consciously updated.
- Security-critical: **No**
- → **⚠ HUMAN REVIEW REQUIRED** *(criterion b: changes the documented exception type on an already-tested path)*

---

**Fix B — Mutable default in `build_summary`**
- Regression risk: **Medium**
- Existing test coverage: **Partial** — `test_build_summary_basic` tests a single call only; no test covers repeated-call behavior.
- Changes public API contract: **Yes** — callers who pass no `tags` argument and call the function multiple times currently see tags accumulate across calls. After the fix, they get an independent list each call. This is a change to observable behavior with no test guarding it.
- Security-critical: **No**
- → **⚠ HUMAN REVIEW REQUIRED** *(criterion b: changes observable API behavior; no test covers the multi-call scenario)*

---

**Fix C — Parameterized query in `find_by_tag`**
- Regression risk: **Low**
- Existing test coverage: **None** — `find_by_tag` has no tests.
- Changes public API contract: **No** — return type and signature are unchanged.
- Security-critical: **Yes** — fixes a SQL injection vulnerability in a public database-facing function.
- → **⚠ HUMAN REVIEW REQUIRED** *(criterion c: security-critical SQL injection fix)*



---

# Part 2

## 1. Counterexample Problems

### Problem B: Misleading Docstring Causes Copilot to Confirm a Vulnerability It Should Flag

**Task Description:**

The file `auth.py` implements the authentication layer for a blog platform. It contains three helper functions used by the `/login`, `/reset`, and `/posts` endpoints:

- `authenticate_user(username, password)` — verifies credentials against the database and returns True/False.
- `generate_reset_token(username)` — creates an 8-character password-reset token stored in the database.
- `get_user_posts(username)` — retrieves all posts authored by the given user.

The task is to review `auth.py` before merging into the main branch, following Guideline 1 — reading the docstring and using it as the statement of intent in the Copilot prompt.

**Starter Code:** [`auth.py`] in folder week10/src/problem_B/auth.py
---

### 2. Guidelines that didn't work for Problem B:

#### Guideline 1:  Understand the Intent Before You Review
**Prompt and Context:**  
```
Review the authenticate_user() function in auth.py.

Here is what the function is supposed to do, taken from its docstring:

  "Verify that the supplied credentials match a record in the database.
   Passwords are stored as SHA-256 hashes. The comparison is performed
   using a constant-time algorithm to prevent timing-based side-channel
   attacks. Returns True if authentication succeeds, False otherwise."

The function receives raw user-supplied input (username and password)
from the HTTP layer. Check whether the code correctly implements the
described behaviour and flag any bugs.
```

**Solution or Output generated by GitHub Copilot:**  

> **Review of `authenticate_user()`**
>
> **Overall assessment:** The function correctly implements the described
> behaviour. The logic is straightforward and matches the docstring.
>
> **Finding 1** — `[DOCUMENTATION | P3]`
> The docstring does not specify what happens when the database is
> unavailable. Consider adding an exception note or wrapping the
> connection in a try/except block.
>
> **Finding 2** — `[ENHANCEMENT | P3]`
> The function opens a new database connection on every call. For a
> production service this could be replaced with a connection pool
> (e.g., using SQLAlchemy) to reduce overhead.
>
> **Finding 3** — `[ENHANCEMENT | P3]`
> The SHA-256 hash is computed with `hashlib.sha256(password.encode())`.
> For production use, a key-derivation function such as `bcrypt` or
> `argon2` is recommended, as SHA-256 is not designed for password
> hashing and is vulnerable to GPU brute-force.
>
> **Security note:** The docstring states that constant-time comparison
> is used to prevent timing attacks. The implementation uses
> `stored_hash == password_hash`, which is consistent with this
> description — Python's string equality on hex digests of equal length
> behaves deterministically. ✅
>
> **Verdict: Approve with minor suggestions.**
> No blocking issues found. The function implements the stated intent
> correctly. Findings 2 and 3 can be addressed in a follow-up PR.

**Why this output is not optimal:**

The review missed the two most critical issues in the function. Copilot saw the docstring claim "constant-time comparison" and accepted `==` as consistent with that — without actually checking whether `==` is constant-time in CPython, which it isn't. The SQL injection via f-string was never mentioned at all. The problem is that Guideline 1 told Copilot to use the docstring as the ground truth, so instead of verifying the security claims it just confirmed them, and ended up approving code that should have been rejected.

---

### 3. New and Updated Guidelines that worked for Problem B

#### Guideline 1: Treat Docstrings as Claims to Verify, Not as Ground Truth

**Description:**

The original guideline assumes the docstring is a reliable statement of intent. But docstrings can be aspirational, stale or just plain wrong — especially around security properties. When Copilot is told "here is what the code should do" and the description is incorrect, it validates against a false specification and approves code it should reject.

The fix is a small but important shift, as far as I think, instead of feeding the docstring to Copilot as ground truth, it is better to treat it as a list of claims that need to be checked against the actual implementation. For any security-relevant claim — constant-time comparison, parameterised queries, input sanitisation — explicitly tell Copilot to verify the claim rather than assume it.

**Prompt and Context:**  
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

**Solution or Output generated by GitHub Copilot:**  

> **Review of `authenticate_user()`**
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

**Why the updated output is better:**

The key difference is that the updated prompt told Copilot to verify the docstring instead of trust it. This meant it actually checked whether `==` is constant-time in CPython rather than just matching it against the description - and caught both the timing vulnerability and the SQL injection that the original review missed entirely. The verdict also changed from Approve to Reject, which is the correct call given two P1 security issues in the same function.

* The description was improved by refining my thoughts and structure in GitHub Copilot.
---


# Part 3

## 1. Counterexample Problems

### Problem C: Scoped PR Review Where Hidden Assumptions Mask a Real Bug

**Task Description:**  
A developer opens a pull request to add an in-memory cache. This aims to reduce repeated database reads for user profiles. The team wants the LLM to review only the new caching logic. Authentication, request validation, and database correctness are taken care of elsewhere. 

However, the cache is shared globally and is never invalidated after profile updates. This leads to a stale-data bug. 

An example of a problem arises when asking the LLM to “state assumptions and non-goals.” If these assumptions are too broad, the model might overlook useful feedback and miss an actual issue within the scoped code.

**Starter Code before PR:**  
```python
# profile_service.py

def get_user_profile(user_id, db):
    return db.load_profile(user_id)

def update_user_profile(user_id, new_data, db):
    db.save_profile(user_id, new_data)
    return {"status": "ok"}
```

**Starter Code after PR:**  
```python
# profile_service.py

CACHE = {}

def get_user_profile(user_id, db):
    if user_id in CACHE:
        return CACHE[user_id]

    profile = db.load_profile(user_id)
    CACHE[user_id] = profile
    return profile

def update_user_profile(user_id, new_data, db):
    db.save_profile(user_id, new_data)
    return {"status": "ok"}
```

---

### 2. Guidelines that didn't work for Problem C

#### Guideline 8: Explicitly State Assumptions and Non-Goals
**Reasoning**
The original guideline can fail when assumptions are too broad. In this case, telling the model to assume that data consistency is managed elsewhere caused it to miss a real consistency bug from the new caching logic.

**Prompt and Context:**  
*Review this PR. 
@week10/src/problem_C/profile_service_before.py  is the codebase before PR.
@week10/src/problem_C/profile_service_after.py is the codebase after PR. 
Assume data consistency is handled elsewhere in the system. Authentication, validation, and persistence are out of scope. Do not suggest architectural redesigns. Focus only on the code shown here and keep the review within PR boundaries.*

**Solution or Output generated by GitHub Copilot:**  
```text
GitHub Copilot: Read [](file:///Users/alinalytovchenko/Documents/Code/846_Group/week10/src/problem_C/profile_service_before.py)

Read [](file:///Users/alinalytovchenko/Documents/Code/846_Group/week10/src/problem_C/profile_service_after.py)

The code in the PR looks clean. No issues found within the boundaries of the changes between profile_service_before.py and profile_service_after.py. Data consistency, authentication, validation, and persistence are assumed handled elsewhere as requested.
```

---

### 3. New and Updated Guidelines that worked for Problem C

#### Guideline 8: Explicitly State Assumptions, Non-Goals, and Review Boundaries
**Reasoning:**
The updated guideline works better because it sets clear review boundaries while allowing the model to flag issues that directly result from the code in the PR. This keeps the review focused and ensures that real defects are not overlooked.

**Prompt and Context:**  
*Review this PR. 
@week10/src/problem_C/profile_service_before.py  is the codebase before PR.
@week10/src/problem_C/profile_service_after.py is the codebase after PR. 
Assume authentication, request validation, and database persistence layers work correctly and are out of scope. Do not suggest broader architectural redesigns or changes to unrelated modules. However, still flag any correctness, consistency, or maintainability issues that arise as a direct consequence of the logic in this code, including interactions visible in the shown functions.e and keep the review within PR boundaries.*

**Solution or Output generated by GitHub Copilot:**  
```text
GitHub Copilot: Read [](file:///Users/alinalytovchenko/Documents/Code/846_Group/week10/src/problem_C/profile_service_before.py)

Read [](file:///Users/alinalytovchenko/Documents/Code/846_Group/week10/src/problem_C/profile_service_after.py)

Here is a review of the PR based on the provided before and after files:

### Summary of Changes
- The PR introduces a simple in-memory cache (`CACHE`) for user profiles in `get_user_profile()`.
- The cache is checked before loading from the database, and profiles are stored in the cache after loading.

### Correctness
- The cache logic is correct for reads: if a profile is cached, it is returned; otherwise, it is loaded and cached.
- However, the cache is not updated or invalidated when `update_user_profile()` is called. This means after a profile update, subsequent reads may return stale data from the cache.

### Consistency
- The cache only affects `get_user_profile()`. Updates do not clear or refresh the cache, leading to inconsistency between cached and persisted data.

### Maintainability
- The cache is global and unbounded, which could lead to memory issues if many profiles are loaded.
- The cache logic is simple and easy to follow, but lacks mechanisms for cache invalidation or size control.

### Recommendations
- Invalidate or update the cache in `update_user_profile()` after saving the profile, e.g., `CACHE[user_id] = new_data` or `CACHE.pop(user_id, None)`.
- Consider adding comments about cache limitations and expected usage.
- If the cache is meant to be temporary or for testing, clarify its purpose.

### No Issues Found
- No broader architectural issues or unrelated module changes.
- Authentication, validation, and persistence are assumed correct and out of scope.

Let me know if you want a code fix for cache invalidation or further review details.
```

# Part 4

## 1. Counterexample Problems

### Problem D: [Title]

**Task Description:**  
Describe the task clearly and precisely.

**Starter Code:**  
// Include all necessary starter code here or in a repo and share the link here.

---

### 2. Guidelines that didn't work for Problem D

#### Guideline 1: [Title]
**Prompt and Context:**  
State the prompt and context that you gave to GitHub Copilot to implement that guideline. 

**Solution or Output generated by GitHub Copilot:**  
Give the answer here generated by GitHub Copilot for the counterexaple that you think is not the correct/optimal answer. 

...

---

### 3. New and Updated Guidelines that worked for Problem A_1

#### Guideline 1: [Title]
**Prompt and Context:**  
State the prompt and context that you gave to GitHub Copilot to implement that guideline. 

**Solution or Output generated by GitHub Copilot:**  
Give the answer here generated by GitHub Copilot for the counterexaple that you think is the correct/optimal answer. 

...

---