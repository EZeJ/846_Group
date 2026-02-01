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