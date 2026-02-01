# Week X Guidelines: [Topic Title]

**Authors:** Liliana Hotsko, Alina Lytovchenko, Sofiia Tkach,  
**Readings Assigned:**  
- [Primary reading 1]  
- [Primary reading 2] ...

## 1. Guidelines

> **Note:** Guidelines should be actionable, specific, and usable during real coding tasks.

### Guideline 1: [Short, Actionable Title]
**Description:**  
State the guideline clearly and concretely.

**Reasoning:**  
Explain *why* this guideline is important, referencing readings and external sources where relevant.

**Example:**  
Provide a brief illustrative example (code or pseudo-code if helpful).

___

# Updated Guideline 4 - Provide few-shot examples (Positive + Negative)

## Description
When specifying the desired behavior of a program or system, provide **two contrasting examples**:
- **One good example** that follows the intended format and constraints, and  
- **One bad example** that demonstrates a common failure mode to avoid.

Explicitly state that the examples are to demonstrate **format + constraints**, not to lock the model into the example’s domain.

## Reasoning
Few-shot examples often improve LLM adherence to structure and output format, and examples can double as lightweight tests.  
However, few-shot can fail when the model treats the example as a **template to copy** (e.g., repeating the same roles, actions, or domain details), rather than learning the underlying constraints.  

Adding **one negative** and **one positive** example and **explicit invariants** shifts the model from **“copy this pattern”** to **“satisfy these rules,”** improving generalization across domains and preventing overfitting to the example scenario.


## Example

### Task
List and describe the real-world constraints that may impact the project, including **budget**, **technical feasibility**, and **time limitations** outside of what was stated in the interviews.

### Bad prompt
List real-world constraints for the project.

### Better prompt
List **8–12** real-world constraints **outside of the interviews**. Use the exact bullet format:  
`Constraint Type — Description — Impact — Mitigation/Next step`

I will provide **two contrasting examples** (one good, one bad) to demonstrate **format + quality constraints only** (do not copy the example’s specific details).

**Good example (follow this style; do not invent specifics):**  
- `Budget — Budget cap unknown (TBD) — May limit scope to MVP — Confirm budget owner + prioritize features`

**Bad example (do NOT do this; invented specifics / copied content):**  
- `Budget — We have exactly $50k — Must use AWS + Stripe — Ship in 8 weeks`

**Note:** The examples demonstrate **format + constraints only**. Do **not** reuse the example’s numbers/vendors/timelines unless they are explicitly given for this project.

**Invariants (must hold for every bullet):**
- Do **not** invent facts. If a number/date/vendor is unknown, use **TBD/unknown** and propose how to confirm it.
- Each bullet must include both **Impact** and **Mitigation/Next step**.
- Include at least one constraint each for **Budget**, **Time**, and **Technical feasibility**.
- Keep constraints concrete and verifiable; avoid vague words unless measurable.

 
---

### Updated Guideline 6: Use Structured and Standardized Role Formatting for Multi-Speaker Content

**Description:**

When providing conversations, transcripts, interviews, chats, or debates to an LLM, clearly structure speaker roles using consistent, high-visibility formatting.

Capitalizing role names helps, but for analytical tasks it is often not sufficient on its own.
Whenever the task depends on tracking viewpoints, responsibility, or technical reasoning, use structured role formatting such as JSON or tagged dialogue. 

**Reasoning:***
When reading transcripts, LLMs can sometimes misclassify which person was responsible for saying what, which leads to all sorts of errors. However, if speaker boundaries are weak or visually similar to the surrounding text, the model may:

- Blend perspectives

- Attribute arguments to the wrong person

- Lose track of stance over time

- Produce generic or inaccurate summaries

**Example:**

- Simple formatting:

```Jerry: No, they come from you adding FOREIGN KEY constraints everywhere.```

- Capitalization:

```JERRY: No, they come from you adding FOREIGN KEY constraints everywhere.```

- JSON formatting: 

```{"role": "TOM", "text": "We need a proper relational schema. THIRD NORMAL FORM exists for a reason."}```







## 2. References

[1]  
[2] 

---