# Exercise 1: How Role Formatting Affects LLM Understanding? 

In this exercise, you will test how different dialogue formats affect an LLM’s ability to correctly interpret a technical discussion. (Updated guideline 6).

You will use the same conversation between TOM and JERRY, who are debating database schema design. Their discussion includes many capitalized SQL terms (e.g., JOIN, FOREIGN KEY, SELECT), which makes this a challenging case for speaker tracking.

**Example prompt:**
Who argues that performance problems are caused by indexing, and who argues they are caused by schema design choices? Quote the relevant statements.

**Files to use:**

Folder: ```week4/drafts/updated_guideline_6```

- Step 0: Use the regular version only of the chat. ```(file: chat_0.txt)```

- Step 1: Use the version with capitalization of the chat. ```(file: chat_1.txt)```

- Step 2: Use the json formatted version of the chat. ```(file: chat_2.txt)```

**Task:**
Using the **Updated Guideline 6**, analyze which format made it easier for the model to track each speaker’s position?

---

# Exercise 2: 
## Task Description
Using the event information provided in `week4/drafts/updated_guideline_4/adoption_day_info_sheet.txt`, create **10 visitor FAQ Q&A pairs** to help attendees understand what to expect and how to prepare for the event.

## Format
Write each item in this exact format:

`Q: …`  
`A: …`

## Starter Code
There is a txt document with the event description in `week4/drafts/updated_guideline_4/adoption_day_info_sheet.txt`.

---

## Exercise 3: Compliance Prohibitions, Persona Pushes Loopholes

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

## Exercise 4: Fix a Username Validation Bug

### Setup (policy excerpt)
A username is valid if and only if:
* The input is not None.
* Leading and trailing whitespace is ignored (validation uses the trimmed value).
* The length is between 3 and 20 characters (inclusive).
* The first character is a letter.
* Every character is alphanumeric or _.
* The username does not end with _.

### Task
You are given an implementation of is_valid_username(username: str) -> bool that is intended to follow the policy above.
Identify the mismatch between the policy and the code, and propose the minimal code change needed to make the implementation comply with the policy.

### Required output format
Bug: One sentence describing the violated rule.
Failing example: One concrete input that demonstrates the bug.
Fix: A minimal code snippet (only the new/changed lines).

---
