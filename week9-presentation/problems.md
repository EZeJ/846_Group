# Week 9 Example Problems: Testing / QA

**Authors:** Liliana Hotsko, Alina Lytovchenko, Sofiia Tkach, Zesheng(Ethan) Jia

## Relevant Guidelines per Problem

| Question | Guidelines |
|---------|------------|
|   A | 1, 2 |
|   B_1| 3 |
|   B_2 | 4      |
|   B_3 |  3 , 4 |

## 1. Example Problems

> All tasks should be completed in Python using pytest. Use the GPT-4.1 model. For testing, use the `@pytest.mark.parametrize` decorator to efficiently check multiple input cases and uncover bugs in the functions.

### Problem A: Checkout Service Testing

**Task Description:**
You have a checkout service module for an online store. This service handles item-level discounts (flash sales, bundle deals), three distinct coupon types (`SAVE10`, `SUMMER20`, `FLASH5`), a loyalty-points redemption system, shipping cost rules, tax calculation, and payment processing. You need to create unit tests that uncover if the implementation has any bugs.

**Starter Code:**
See `checkout_service.py` in the `problem_A` folder.
---

### Problem B_1: User Validation Testing

**Task Description:**  
You are given a user validation module with functions that validate email addresses, ages, usernames and passwords. Your task is to write comprehensive unit tests using pytest that will reveal bugs in the validation logic.

**Starter Code:**  
See `user_validator.py` in the Problem_B_1 folder.
---

### Problem B_2: Order Processing Decomposition (Guideline 4 Focus)

**Task Description:**  
You are given a complex `process_order()` method that handles validation, calculations, discounts, taxes, payment processing, and confirmation generation all in one function. Your task is to write comprehensive tests that expose the hidden bugs in this complex method.

**Starter Code:**  
See `order_processor.py` in the Problem_B_2 folder.
---

### Problem B_3: Data Parser Edge Cases (Combined Guidelines 3 & 4)

**Task Description:**  
You are given a data parsing module with functions for CSV parsing, JSON configuration validation, number extraction, and data type validation. Each function has multiple edge cases that need thorough testing.

**Starter Code:**  
See `data_parser.py` in the Problem_B_3 folder.

**Expected Discovery:** The combination of both guidelines will reveal numerous edge case bugs and parsing failures that simple testing approaches miss.

---


## 2. References

[1]  
[2] 

---

