User: Improve load_ages so it doesn’t crash on messy CSVs.
Prioritize correctness. Keep edge cases in mind.

GitHub Copilot: Search complete: Find load_ages implementation and usage

Searched for regex `def load_ages|load_ages\(`, 3 results

Read [](file:///Users/alinalytovchenko/Documents/Code/846_Group/week8/resources/update_guideline_6/problem.py)

Read [](file:///Users/alinalytovchenko/Documents/Code/846_Group/week8/updated_guidelines.md#160-160), lines 160 to 220

Read [](file:///Users/alinalytovchenko/Documents/Code/846_Group/week8/resources/update_guideline_6/problem.py)

Generating patch (26 lines) in [](file:///Users/alinalytovchenko/Documents/Code/846_Group/week8/resources/update_guideline_6/problem.py)


```

```
The `load_ages` function is now robust against messy CSVs: it skips blank lines, lines with too few columns, and lines where the age is missing or not an integer. This should prevent crashes and handle edge cases correctly. Let me know if you want logging or error reporting for skipped lines.

Made changes.