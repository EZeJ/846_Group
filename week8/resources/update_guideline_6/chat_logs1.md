User: Fix load_ages(path) for CSV correctness and ~1M rows.
Use csv module (no split).
Skip: header (“age”), blank, non-integer, age < 0 or > 120.
Catch specific exceptions only. Single pass.
Prioritize correctness.

GitHub Copilot: Read [](file:///Users/alinalytovchenko/Documents/Code/846_Group/week8/resources/update_guideline_6/problem.py)

Generating patch (34 lines) in [](file:///Users/alinalytovchenko/Documents/Code/846_Group/week8/resources/update_guideline_6/problem.py)


```

```
The function `load_ages(path)` is now fixed to use the csv module, efficiently handle large files, and correctly skip header, blank, non-integer, and out-of-range ages, with only specific exceptions caught. Let me know if you want to test it or need further changes.

Made changes.