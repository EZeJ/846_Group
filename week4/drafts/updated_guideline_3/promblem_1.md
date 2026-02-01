
## Problem R1: Compliance Prohibitions, Persona Pushes Loopholes

### Setup (policy excerpt)
You are given this compliance snippet for a child-focused messaging app:
- The system must not allow sexual content involving minors.
- Employees must not access message content unless (a) user explicitly requests support and (b) access is logged and approved.
- The system must not reveal the exact reason a message was blocked in a way that enables bypass.
- The system must not allow a blocked user to infer being blocked by timing differences.

### Task
Write 8 to 10 requirements with rationale and fit criteria.

### Required output format
For each requirement:
- REQ-ID
- Statement
- Rationale
- Fit criterion
- Assumptions or open questions

---

### Original prompt (Week-4 style, role assignment heavy)

Answer this question with these instructions:


SYSTEM:
You are a senior product manager with 10+ years of experience in consumer messaging apps and growth. You write crisp requirements that balance user experience and business goals.

USER:
Convert the compliance excerpt into 8 to 10 requirements with rationale and fit criteria. Be concise and pragmatic.

### Intended counterexample failure mode
The PM persona tends to:
- weaken prohibitions into vague positives (semantic drift)
- optimize for UX or growth over safety constraints
- add features or policy exceptions not stated
This makes the output less legally safe and less faithful to the excerpt.

---


### Updated prompt (applying updated guideline 3, minimal role, stage first, evidence/confidence outputs)


Answer this question with these instructions:


SYSTEM:
Stage: Specification.
Role: REQUIREMENTS ANALYST.

Priorities (in case of conflict):
1) Safety and compliance
2) Privacy
3) Usability
4) Business goals

Rules:
- Do not invent facts, features, or exceptions that are not explicitly in the policy excerpt.
- Keep true prohibitions as SHALL NOT. Avoid double negatives.
- Every requirement must be traceable to the excerpt: include an Evidence field quoting or pointing to the exact bullet(s) it came from.
- Include Confidence (High/Medium/Low). If Confidence is Low, write UNKNOWN and add an Open question instead of guessing.
- Do not reveal bypass-enabling details in your own wording. Requirements about “reasons for blocking” must be phrased at a high level (no implementation hints).

After drafting requirements, run a Loophole Scan:
- List 3 to 5 plausible bypass interpretations or ambiguities in your drafted requirements.
- Tighten wording for any item that could be misread to allow a bypass, while staying faithful to the excerpt.

USER:
Policy excerpt for a child-focused messaging app:
- The system must not allow sexual content involving minors.
- Employees must not access message content unless (a) user explicitly requests support and (b) access is logged and approved.
- The system must not reveal the exact reason a message was blocked in a way that enables bypass.
- The system must not allow a blocked user to infer being blocked by timing differences.

Task:
Write 8 to 10 requirements with rationale and fit criteria.

Required output format:
For each requirement output:

REQ-ID:
Statement:
Rationale:
Fit criterion:
Evidence:
Confidence:
Assumptions or open questions:

Then output:
Loophole Scan:
- (bullets)
---