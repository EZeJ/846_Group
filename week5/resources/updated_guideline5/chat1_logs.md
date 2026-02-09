User: First summarize each logical section. Then add a required ‘cross-section invariants’ block listing conditions/resources that must hold across all sections, including every return and exception path.

GitHub Copilot: Read [](file:///Users/alinalytovchenko/Documents/Code/846_Group/week5/resources/updated_guideline5/problem_c.py)

### Summary of Logical Sections

1. **Section 1: Validate + Derive Authorization State**
   - Validates the input `amount` to ensure it is positive.
   - Prevents self-transfers by checking if `src.id` equals `dst.id`.
   - Determines if the transaction is risky (based on `amount` and `limits.instant_threshold`) or if two-factor authentication (2FA) is required.
   - Places a soft hold on the source account (`src`) for the transaction amount.

2. **Section 2: Fraud + Policy Checks**
   - Ensures the transaction does not exceed the daily outgoing limit (`limits.daily_cap`) for the source account.
   - Verifies if 2FA is required and whether the source session has 2FA enabled.
   - Releases the soft hold and exits early if any of these checks fail.

3. **Section 3: Commit + Audit**
   - Attempts to debit the source account and credit the destination account.
   - Records the transaction in the transaction log (`txlog`), including risk information.
   - Releases the soft hold and returns a success response if all operations succeed.
   - Ensures the soft hold is released even in the event of an exception, and re-raises the exception.

---

### Required `cross-section invariants` Block

I'll add a `cross-section invariants` block to ensure that conditions/resources are consistent across all sections, including every return and exception path. 

Using "Edit File"

Using ""


````

````


Made changes.