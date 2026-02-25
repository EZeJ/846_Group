# Week 9 Guidelines: Testing / QA

**Authors:** Liliana Hotsko, Alina Lytovchenko, Sofiia Tkach, Zesheng(Ethan) Jia
**Readings Assigned:**  
* Software Testing With Large Language Models: Survey, Landscape, and Vision [1]
* On the Evaluation of Large Language Models in Unit Test Generation [2]
* Software Testing with Large Language Models: An Interview Study with Practitioners [3]
* Using Large Language Models to Generate JUnit Tests: An Empirical Study [4]
* Evaluating and Improving ChatGPT for Unit Test Generation [5]
* Large Language Models for Software Testing: A Research Roadmap [6]

## 1. Guidelines

> **Note:** Guidelines should be actionable, specific, and usable during real coding tasks.

### Guideline 1: Specify the Testing Goal and Scope in the Prompt
**Description:**  
When asking an LLM to generate or improve tests, explicitly state:
* test level (unit / integration / API / E2E),
* target function/module,
* expected behavior,
* constraints (framework, style, mocks, side effects),
* what not to test

**Reasoning:**  
In their research roadmap, Augusto et al. highlight that prior work consistently shows prompt engineering substantially influences LLM testing outcomes, motivating an iterative rather than one-shot prompt design process.

**Good Example:**
“Generate pytest unit tests for parse_invoice(json_str) only. Cover valid input, missing required fields, malformed JSON, and currency normalization. Do not test database calls or network retries. Use parameterized tests and clear assertion messages.”

**Bad Example:**  
“Write tests for this.”

---

### Guideline x: [Short, Actionable Title]
**Description:**  
State the guideline clearly and concretely.

**Reasoning:**  
Explain *why* this guideline is important, referencing readings and external sources where relevant.

**Example:**  
Provide a brief illustrative example (code or pseudo-code if helpful).


### Guideline x: [Short, Actionable Title]
**Description:**  
State the guideline clearly and concretely.

**Reasoning:**  
Explain *why* this guideline is important, referencing readings and external sources where relevant.

**Example:**  
Provide a brief illustrative example (code or pseudo-code if helpful).


### Guideline 2: [Short, Actionable Title]
(Repeat the same structure for each guideline.)

---

### Guideline N: [Short, Actionable Title]
(Repeat the same structure for each guideline.)

---


## 2. References

[1]  
[2] 

---

