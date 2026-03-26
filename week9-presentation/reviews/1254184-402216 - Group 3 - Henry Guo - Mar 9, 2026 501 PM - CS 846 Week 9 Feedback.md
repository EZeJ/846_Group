# Guideline 7 Counterexample

Authors: Anudeep Das, Henry Guo, Mariia Ponomarenko

# Counterexample for Guideline 7

Guideline 7 is “Counterexample-First Prompting to Generate Discriminative Tests”  
“Before generating final tests, first ask the model to propose plausible wrong variants and minimal counterexamples. Then generate tests that pass for the intended contract and would fail for each wrong variant.”

This guideline works well if bugs are expected to be in the file/repository being analyzed. However, if there is an intentional bug in a custom library function, those bugs will not be found. 

## Problem

Consider the following code.

from deep.repo.week9\_counter\_module import add

def add\_ints(int1, int2):  
   return add(int1, int2)

Where deep/repo/week9\_counter\_module/[add.py](http://add.py) is

def add(num1, num2):  
   if num1 \== 666:  
       return num1 \+ num2 \+ 1  
   return num1 \+ num2 \+ 1

There is a backdoor in the custom add library function, which is a bug since it will give the wrong result.

# Prompting GPT-4o

Following the guideline, we prompt with the following text:

You are helping me write discriminative pytest unit tests.  
Target: add\_ints(int num1, int num2) \-\> int  
Contract summary: Adds two ints together and returns the result.  
Task: list 4–6 plausible wrong variants that are easy to accidentally implement  
For each wrong variant, provide the smallest counterexample inputs that would reveal the bug.  
Return a table: wrong\_variant | symptom | counterexample\_inputs.

## GPT-4o Response

GPT-4o returned the following response.

Here is a table listing plausible wrong variants of the add\_ints function, their symptoms, and the smallest counterexample inputs that would reveal the bug:

| Wrong Variant | Symptom | Counterexample Inputs |
| ----- | ----- | ----- |
| Returns num1 instead of num1 \+ num2 | Ignores num2, always returns num1 | (3, 5\) |
| Returns num2 instead of num1 \+ num2 | Ignores num1, always returns num2 | (3, 5\) |
| Returns num1 \- num2 instead of num1 \+ num2 | Subtracts instead of adding | (5, 3\) |
| Returns num1 \* num2 instead of num1 \+ num2 | Multiplies instead of adding | (2, 3\) |
| Returns num1 / num2 instead of num1 \+ num2 | Divides instead of adding (if num2 \!= 0) | (6, 3\) |
| Returns num1 \+ num2 \+ 1 | Adds an extra 1 to the result | (2, 3\) |

And the following are the tests it generated:  
import pytest  
from week9\_counter import add\_ints

\# Test cases for discriminative testing of add\_ints  
@pytest.mark.parametrize("num1, num2, expected", \[  
   (3, 5, 8),  \# Correct behavior  
   (5, 3, 8),  
   (2, 3, 5),  
\])  
def test\_add\_ints\_correct(num1, num2, expected):  
   assert add\_ints(num1, num2) \== expected

@pytest.mark.parametrize("num1, num2, expected", \[  
   (3, 5, 3),  \# Returns num1 instead of num1 \+ num2  
\])  
def test\_add\_ints\_returns\_num1(num1, num2, expected):  
   assert add\_ints(num1, num2) \!= expected

@pytest.mark.parametrize("num1, num2, expected", \[  
   (3, 5, 5),  \# Returns num2 instead of num1 \+ num2  
\])  
def test\_add\_ints\_returns\_num2(num1, num2, expected):  
   assert add\_ints(num1, num2) \!= expected

@pytest.mark.parametrize("num1, num2, expected", \[  
   (5, 3, 2),  \# Returns num1 \- num2 instead of num1 \+ num2  
\])  
def test\_add\_ints\_subtracts(num1, num2, expected):  
   assert add\_ints(num1, num2) \!= expected

@pytest.mark.parametrize("num1, num2, expected", \[  
   (2, 3, 6),  \# Returns num1 \* num2 instead of num1 \+ num2  
\])  
def test\_add\_ints\_multiplies(num1, num2, expected):  
   assert add\_ints(num1, num2) \!= expected

@pytest.mark.parametrize("num1, num2, expected", \[  
   (6, 3, 2),  \# Returns num1 / num2 instead of num1 \+ num2  
\])  
def test\_add\_ints\_divides(num1, num2, expected):  
   assert add\_ints(num1, num2) \!= expected

@pytest.mark.parametrize("num1, num2, expected", \[  
   (2, 3, 6),  \# Returns num1 \+ num2 \+ 1 instead of num1 \+ num2  
\])  
def test\_add\_ints\_adds\_extra(num1, num2, expected):  
   assert add\_ints(num1, num2) \!= expected

None of these tests will expose the backdoor bug that is in the library function.

# Alternative Guideline

## Prompt the model to make you aware of any possible bugs/backdoors in external libraries, and notify you about standard libraries that can do the same external function.

## In general, standardized libraries are less likely to have bugs and backdoors, hence, programmers should be aware of their existence. However, the model should not replace the current implementation with the one from the standard library in the case of specific company policy and because even standardized libraries can be hallucinated or be untrustworthy. The human programmer simply needs to make the final call and beware.

# Prompting GPT-4o again

We append the text pertaining to our new guideline to the original guideline.

You are helping me write discriminative pytest unit tests.  
Target: add\_ints(int num1, int num2) \-\> int  
Contract summary: Adds two ints together and returns the result.  
Task: list 4–6 plausible wrong variants that are easy to accidentally implement  
For each wrong variant, provide the smallest counterexample inputs that would reveal the bug.  
Return a table: wrong\_variant | symptom | counterexample\_inputs.

**Let me know if there are any risks of backdoors or bugs with the library functions that are called, and let me know if there are standardized libraries that implement the same functions.**

## Results

Here is a table of plausible wrong variants for the add\_ints function, along with their symptoms and the smallest counterexample inputs that would reveal the bug:

| Wrong Variant | Symptom | Counterexample Inputs |
| ----- | ----- | ----- |
| Returns the product instead of sum | Multiplies the inputs instead of adding them | num1 \= 2, num2 \= 3 |
| Returns the difference instead of sum | Subtracts num2 from num1 instead of adding | num1 \= 5, num2 \= 3 |
| Concatenates inputs as strings | Treats inputs as strings and concatenates them instead of adding numerically | num1 \= 2, num2 \= 3 |
| Returns only the first input | Ignores num2 and always returns num1 | num1 \= 4, num2 \= 5 |
| Returns the absolute sum | Returns the sum of absolute values of inputs | num1 \= \-3, num2 \= 2 |
| Returns the sum plus a constant | Adds a constant (e.g., 1) to the sum | num1 \= 2, num2 \= 3 |

**Risks of Backdoors or Bugs**

1. **Backdoors**: The add\_ints function itself is simple and unlikely to have backdoors. However, if the function relies on external libraries or modules for arithmetic operations, there could be risks if those libraries are compromised.  
2. **Bugs**: Bugs could arise if the function does not validate input types (e.g., non-integer inputs) or if it relies on implicit type coercion.

**Standardized Libraries**

* Python's built-in arithmetic operators (\+) are sufficient for this task and are highly reliable.  
* If extended functionality is needed (e.g., handling large integers), libraries like decimal or numpy can be used. These libraries are well-tested and widely used in the Python ecosystem.

## Why Better

Although the tests are still unaware of the existence of the backdoor, and will not catch it, the model has now notified the human programmer of standardized operators they can use instead. These standardized operators are more likely to be trustworthy since they are built-in or trusted.

It should be noted that the model does not consider the add function in deep/repo to be a library module, which would be incorrect. However, it still indicates that there could be bugs in this add() function: “Bugs could arise if the function does not validate input types (e.g., non-integer inputs) or if it relies on implicit type coercion.”, which is good.

# Guideline 1 Counterexample

Authors: Anudeep Das, Henry Guo, Mariia Ponomarenko

# Counterexample for Guideline 3

**Guideline 1:** Specify the Testing Goal and Scope in the Prompt

**Description:**   
When asking an LLM to generate or improve tests, explicitly state:

* test level (unit / integration / API / E2E),  
* target function/module,  
* expected behavior,  
* constraints (framework, style, mocks, side effects),  
* what not to test

**Reasoning:** Clear scope reduces ambiguity, so the model produces more relevant and accurate tests instead of generic or off-target output. LLM testing results depend heavily on prompt quality/prompt engineering and that prompt design \[6\].

**Problem**  
Make unit tests for the simple matrix multiplication function in matmul.py. This function’s purpose is to multiply 2 matrices together and return their product. This is a low-level function used by many other programs.  
def matmul(A, B):  
    rows\_a \= len(A)  
    if rows\_a \== 0:  
        return \[\]

    cols\_a \= len(A\[0\])  
    rows\_b \= len(B)  
    cols\_b \= len(B\[0\]) if rows\_b \> 0 else 0

    result \= \[\[0\] \* cols\_b for \_ in range(rows\_a)\]

    for i in range(rows\_a):  
        for j in range(cols\_b):  
            total \= 0  
            for k in range(cols\_a):  
                total \+= A\[i\]\[k\] \* B\[k\]\[j\]  
            result\[i\]\[j\] \= total

    return result

Use GPT-4.1 to generate the tests.

**Response with Old Guideline**  
Prompt:  
Generate tests for this matmul function. This function’s purpose is to multiply 2 matrices together and return their product. This is a low-level function used by many other programs. Use pytest as the testing framework.

Response:

import pytest  
from matmul import matmul

def test\_matmul\_basic():  
    A \= \[\[1, 2\], \[3, 4\]\]  
    B \= \[\[5, 6\], \[7, 8\]\]  
    expected \= \[\[19, 22\], \[43, 50\]\]  
    assert matmul(A, B) \== expected

def test\_matmul\_identity():  
    A \= \[\[1, 2\], \[3, 4\]\]  
    I \= \[\[1, 0\], \[0, 1\]\]  
    assert matmul(A, I) \== A  
    assert matmul(I, A) \== A

def test\_matmul\_zero\_matrix():  
    A \= \[\[1, 2\], \[3, 4\]\]  
    Z \= \[\[0, 0\], \[0, 0\]\]  
    expected \= \[\[0, 0\], \[0, 0\]\]  
    assert matmul(A, Z) \== expected  
    assert matmul(Z, A) \== expected

def test\_matmul\_rectangular():  
    A \= \[\[1, 2, 3\], \[4, 5, 6\]\]  
    B \= \[\[7, 8\], \[9, 10\], \[11, 12\]\]  
    expected \= \[\[58, 64\], \[139, 154\]\]  
    assert matmul(A, B) \== expected

def test\_matmul\_empty():  
    assert matmul(\[\], \[\]) \== \[\]  
    assert matmul(\[\[\]\], \[\[\]\]) \== \[\[0\]\]

def test\_matmul\_single\_element():  
    A \= \[\[2\]\]  
    B \= \[\[3\]\]  
    assert matmul(A, B) \== \[\[6\]\]

def test\_matmul\_row\_vector\_col\_vector():  
    A \= \[\[1, 2, 3\]\]  \# 1x3  
    B \= \[\[4\], \[5\], \[6\]\]  \# 3x1  
    expected \= \[\[32\]\]  
    assert matmul(A, B) \== expected

def test\_matmul\_col\_vector\_row\_vector():  
    A \= \[\[1\], \[2\], \[3\]\]  \# 3x1  
    B \= \[\[4, 5, 6\]\]      \# 1x3  
    expected \= \[\[4, 5, 6\], \[8, 10, 12\], \[12, 15, 18\]\]  
    assert matmul(A, B) \== expected

def test\_matmul\_incompatible\_dimensions():  
    A \= \[\[1, 2\]\]  
    B \= \[\[3, 4\]\]  
    with pytest.raises(IndexError):  
        matmul(A, B)

The problem with this response is that the fundamental bug with the code is that it’s slow. It is a very inefficient implementation of matrix multiplication. The problem description implies that this method should be fast as it is a low-level function used by many other programs. The LLM test did not write any tests related to performance or even raise it as a concern. Heavy focus on functionality could hide away performance bugs.

**New Guideline**  
**Description:** This new guideline just adds one more item to the checklist of descriptions for the expected behavior to feed to the LLM. 

* Include other performance and stylistic behavior that the code being tested should possess.

If possible, include some performance metrics that the code should meet as a part of the test.

**Reasoning:** Pure heavy focus on input handling and output correctness diverts attention away from performance. For many low-level tests, inputs and outputs are often very simple and easily tested. However, the main focus of those functions is performance. Just also mention performance in the explicit list of concerns to test for.

**Good Example:**  
This function is a simple matrix multiplication function. Make sure it can handle any type of input correctly to generate the appropriate output. Also make sure that it is fast and performant. It should be able to compute a 100x100 input in less than 10s.

**Bad Example:**  
Test this code. Make sure it can handle any type of input correctly to generate the appropriate output.

**Response with New Guideline**  
Prompt:  
Generate tests for this matmul function. This function’s purpose is to multiply 2 matrices together and return their product. This is a low-level function used by many other programs. Make sure it is fast and performant. Use pytest as the testing framework.

Response:  
import pytest  
import random  
import time  
from matmul import matmul

\# Basic correctness tests  
def test\_matmul\_identity():  
    A \= \[\[1, 2\], \[3, 4\]\]  
    I \= \[\[1, 0\], \[0, 1\]\]  
    assert matmul(A, I) \== A  
    assert matmul(I, A) \== A

def test\_matmul\_zero():  
    A \= \[\[1, 2\], \[3, 4\]\]  
    Z \= \[\[0, 0\], \[0, 0\]\]  
    assert matmul(A, Z) \== Z  
    assert matmul(Z, A) \== Z

def test\_matmul\_rectangular():  
    A \= \[\[1, 2, 3\], \[4, 5, 6\]\]  
    B \= \[\[7, 8\], \[9, 10\], \[11, 12\]\]  
    expected \= \[\[58, 64\], \[139, 154\]\]  
    assert matmul(A, B) \== expected

def test\_matmul\_empty():  
    assert matmul(\[\], \[\]) \== \[\]  
    assert matmul(\[\[\]\], \[\[\]\]) \== \[\[0\]\]

def test\_matmul\_single\_element():  
    assert matmul(\[\[2\]\], \[\[3\]\]) \== \[\[6\]\]

\# Performance test for large matrices  
def test\_matmul\_large\_performance():  
    size \= 200  
    A \= \[\[random.randint(0, 10) for \_ in range(size)\] for \_ in range(size)\]  
    B \= \[\[random.randint(0, 10) for \_ in range(size)\] for \_ in range(size)\]  
    start \= time.time()  
    result \= matmul(A, B)  
    end \= time.time()  
    assert len(result) \== size  
    assert len(result\[0\]) \== size  
    assert (end \- start) \< 2.0  \# Should complete within 2 seconds

\# Test for non-square matrices  
def test\_matmul\_non\_square():  
    A \= \[\[1, 2, 3\]\]  
    B \= \[\[4\], \[5\], \[6\]\]  
    expected \= \[\[32\]\]  
    assert matmul(A, B) \== expected

\# Test for mismatched dimensions (should raise IndexError)  
def test\_matmul\_mismatched\_dimensions():  
    A \= \[\[1, 2\]\]  
    B \= \[\[3, 4\]\]  
    with pytest.raises(IndexError):  
        matmul(A, B)

Now since we asked for it to also test for performance. A performance test was also generated, as desired. Other guidelines can be used in tandem with this new updated guideline so that the performance tests can be validated and repaired further in a loop. Other performance and stability concerns can also be discovered, e.g. stability of this low-level matrix multiplication function in different hardware setups and operating systems.

# Guideline 3 Counterexample

Authors: Anudeep Das, Henry Guo, Mariia Ponomarenko

# Counterexample for Guideline 3

**Description**:   
Do not rely on the LLM to independently enumerate edge cases. In the prompt, explicitly require categories of non-happy-path tests with (ideally) minimum counts and strong assertions. At a minimum, request: 

Boundary values: min/max, zero, empty string/collection, single-element, off-by-one Null / missing inputs: null, absent keys/fields, optional values missing 

Invalid formats: malformed JSON/CSV, invalid dates, illegal enum values, wrong encoding 

Exception/error paths: inputs that must trigger validation failures or thrown exceptions (use pytest.raises or equivalent) 

State/contract violations: precondition breaches, invalid state transitions (if applicable) Invariant/property checks: conditions that must always hold regardless of input 

Strong assertions: not just "test runs without crashing", but verify exact expected outputs, state changes, and side effects 

**Reasoning**: LLMs usually generate "happy-path" tests first. They often don't invent the weird or extreme inputs that actually trigger validation errors and exception branches. The papers   
show that many bugs are missed because the tests don't hit those paths, so you need to tell the model directly to create boundary and negative cases.

## Problem 

import re  
from datetime import datetime

def parse\_date(value: str) \-\> datetime:  
   """Accepts dates like '2024-01-15', '15/01/2024', 'Jan 15 2024'"""  
   formats \= \["%Y-%m-%d", "%d/%m/%Y", "%b %d %Y"\]  
   for fmt in formats:  
       try:  
           return datetime.strptime(value.strip(), fmt)  
       except ValueError:  
           continue  
   raise ValueError(f"Unrecognized date format: {value\!r}")

def normalize\_username(username: str) \-\> str:  
   """Lowercase, strip whitespace, collapse internal spaces to underscores"""  
   if not isinstance(username, str):  
       raise TypeError("Username must be a string")  
   result \= username.strip().lower()  
   result \= re.sub(r'\\s\+', '\_', result)  
   if not result:  
       raise ValueError("Username cannot be empty")  
   return result

def merge\_configs(base: dict, override: dict) \-\> dict:  
   """Deep merge two config dicts. Override values win."""  
   result \= dict(base)  
   for key, value in override.items():  
       if key in result and isinstance(result\[key\], dict) and isinstance(value, dict):  
           result\[key\] \= merge\_configs(result\[key\], value)  
       else:  
           result\[key\] \= value  
   return result

def calculate\_discount(price: float, discount\_pct: float) \-\> float:  
   """Returns final price after discount. Discount is 0–100."""  
   if not (0 \<= discount\_pct \<= 100):  
       raise ValueError("Discount must be between 0 and 100")  
   return round(price \* (1 \- discount\_pct / 100), 2)

**P.S. The code was generated with Claude Sonnet 4.6.**

## Prompt using Original Guideline

Generate pytest for [example.py](http://example.py).

Required test categories for EACH function (minimum 2 tests per  
category):

parse\_date — whitespace padding, Unicode lookalike digits (e.g. ２０２４), Feb 29 on non-leap years, Dec 31 / Jan 1 boundary, ambiguous dates like 01/02/2024 (month-first vs day-first), empty string, None.  
normalize\_username — tabs and newlines (not just spaces), Unicode spaces like \\u00a0 (non-breaking space), all-whitespace input, Unicode letters that survive .lower() unexpectedly (e.g. ß → ss), very long strings, already-normalized input (idempotency).  
merge\_configs — one or both args are empty dicts, nested keys where base has a dict but override has a scalar (type collision), deeply nested structures, keys with None values, non-string keys, same object passed as both args (identity merge).  
calculate\_discount — exactly 0 and 100 (boundary), 100 should return 0.0 not \-0.0, floating point precision (e.g. 0.1 \+ 0.2 style issues), negative price, NaN or inf as inputs, discount of 100 on a zero price.

**P.S. The edge cases were generated with Claude Sonnet 4.6.**

## Result after using Original Guideline

import math  
import pytest  
from datetime import datetime

from example import (  
   parse\_date,  
   normalize\_username,  
   merge\_configs,  
   calculate\_discount,  
)

\# parse\_date tests  
def test\_parse\_date\_whitespace\_padding\_spaces():  
   assert parse\_date(' 2024-01-15 ') \== datetime(2024, 1, 15)

def test\_parse\_date\_whitespace\_padding\_tabs\_newlines():  
   assert parse\_date('\\t15/01/2024\\n') \== datetime(2024, 1, 15)

def test\_parse\_date\_unicode\_lookalike\_digits\_leading\_year():  
   with pytest.raises(ValueError):  
       parse\_date('２０２４-01-15')

def test\_parse\_date\_unicode\_lookalike\_digits\_all\_components():  
   with pytest.raises(ValueError):  
       parse\_date('２０２４/０１/１５')

def test\_parse\_date\_feb29\_non\_leap\_slash\_format():  
   with pytest.raises(ValueError):  
       parse\_date('29/02/2019')

def test\_parse\_date\_feb29\_non\_leap\_text\_format():  
   with pytest.raises(ValueError):  
       parse\_date('Feb 29 2019')

def test\_parse\_date\_dec31\_and\_jan1\_boundary\_dec():  
   assert parse\_date('2024-12-31') \== datetime(2024, 12, 31)

def test\_parse\_date\_dec31\_and\_jan1\_boundary\_jan():  
   assert parse\_date('01/01/2025') \== datetime(2025, 1, 1)

def test\_parse\_date\_ambiguous\_day\_first\_slash\_01022024():  
   \# slash format is day-first in this implementation  
   assert parse\_date('01/02/2024') \== datetime(2024, 2, 1)

def test\_parse\_date\_ambiguous\_day\_first\_slash\_02012024():  
   assert parse\_date('02/01/2024') \== datetime(2024, 1, 2)

def test\_parse\_date\_empty\_string():  
   with pytest.raises(ValueError):  
       parse\_date('')

def test\_parse\_date\_all\_spaces\_string():  
   with pytest.raises(ValueError):  
       parse\_date('   ')

def test\_parse\_date\_none\_raises\_typeerror():  
   with pytest.raises(TypeError):  
       parse\_date(None)  \# type: ignore

def test\_parse\_date\_non\_string\_input\_raises\_typeerror():  
   with pytest.raises(AttributeError):  
       \# integers do not have .strip(); ensure non-strings fail  
       parse\_date(20240115)  \# type: ignore

\# normalize\_username tests  
def test\_normalize\_username\_tabs\_and\_newlines():  
   assert normalize\_username('\\tUser\\nName  ') \== 'user\_name'

def test\_normalize\_username\_unicode\_nbsp\_spaces():  
   \# NBSP between words should be treated as whitespace by \\s+  
   nb \= 'Name\\u00a0WithNBSP'  
   assert normalize\_username(nb) \== 'name\_withnbsp'

def test\_normalize\_username\_all\_whitespace\_input\_raises():  
   with pytest.raises(ValueError):  
       normalize\_username('   \\t\\n  ')

def test\_normalize\_username\_unicode\_sharp\_s\_idempotency():  
   \# ß lower() remains ß; ensure function is idempotent for already normalized  
   s \= 'straße'  
   assert normalize\_username(s) \== 'straße'

def test\_normalize\_username\_very\_long\_string():  
   long \= 'User' \+ (' ' \* 1000) \+ 'End'  
   out \= normalize\_username(long)  
   assert out.startswith('user\_') and out.endswith('end')

def test\_normalize\_username\_already\_normalized\_idempotent():  
   u \= 'already\_normalized'  
   assert normalize\_username(u) \== normalize\_username(normalize\_username(u))

\# merge\_configs tests  
def test\_merge\_configs\_one\_empty\_base():  
   base \= {}  
   override \= {'a': 1}  
   assert merge\_configs(base, override) \== {'a': 1}

def test\_merge\_configs\_one\_empty\_override():  
   base \= {'a': 1}  
   override \= {}  
   assert merge\_configs(base, override) \== {'a': 1}

def test\_merge\_configs\_type\_collision\_override\_scalar():  
   base \= {'a': {'b': 2}}  
   override \= {'a': 5}  
   assert merge\_configs(base, override) \== {'a': 5}

def test\_merge\_configs\_type\_collision\_base\_scalar\_override\_dict():  
   base \= {'a': 5}  
   override \= {'a': {'b': 2}}  
   assert merge\_configs(base, override) \== {'a': {'b': 2}}

def test\_merge\_configs\_deeply\_nested():  
   base \= {'a': {'b': {'c': 1}, 'x': 9}}  
   override \= {'a': {'b': {'d': 2}}}  
   expected \= {'a': {'b': {'c': 1, 'd': 2}, 'x': 9}}  
   assert merge\_configs(base, override) \== expected

def test\_merge\_configs\_keys\_with\_none\_values():  
   base \= {'a': 1, 'b': None}  
   override \= {'b': 2}  
   assert merge\_configs(base, override) \== {'a': 1, 'b': 2}

def test\_merge\_configs\_non\_string\_keys():  
   base \= {1: 'one'}  
   override \= {(2, 3): 'tuple'}  
   out \= merge\_configs(base, override)  
   assert out\[1\] \== 'one' and out\[(2, 3)\] \== 'tuple'

def test\_merge\_configs\_same\_object\_identity():  
   d \= {'a': 1}  
   res \= merge\_configs(d, d)  
   assert res \== d and res is not d

\# calculate\_discount tests  
def test\_calculate\_discount\_zero\_and\_hundred\_boundaries\_zero():  
   assert calculate\_discount(100.0, 0) \== 100.00

def test\_calculate\_discount\_hundred\_returns\_zero\_positive\_sign():  
   res \= calculate\_discount(50.0, 100)  
   assert res \== 0.00  
   assert math.copysign(1.0, res) \== 1.0

def test\_calculate\_discount\_precision\_rounding():  
   \# 0.1 \+ 0.2 style input  
   price \= round(0.1 \+ 0.2, 2)  
   assert calculate\_discount(price, 0) \== 0.3

def test\_calculate\_discount\_negative\_price():  
   assert calculate\_discount(\-100.0, 10) \== round(\-100.0 \* 0.9, 2)

def test\_calculate\_discount\_nan\_and\_inf\_inputs():  
   nan \= calculate\_discount(float('nan'), 10)  
   inf \= calculate\_discount(float('inf'), 10)  
   assert math.isnan(nan)  
   assert math.isinf(inf)

def test\_calculate\_discount\_100\_on\_zero\_price\_is\_zero():  
   res \= calculate\_discount(0.0, 100)  
   assert res \== 0.00  
   assert math.copysign(1.0, res) \== 1.0

def test\_calculate\_discount\_invalid\_discount\_raises():  
   with pytest.raises(ValueError):  
       calculate\_discount(100.0, \-1)  
   with pytest.raises(ValueError):  
       calculate\_discount(100.0, 101)

## Analysis

Sometimes it can be hard to account for all possible edgecases. Humans often might not possess the same level of creativity when it comes to coming up with ideas. On the other hand, LLM cannot know about certain rules that need to be followed in the project. Still, it is important to give LLMs a degree of freedom to propose its own edgecases beside those that the user provides. It can lead to interesting discoveries and richer test coverage. 

## New Guideline

**Description**:   
Provide LLM with edge-cases that should be covered. Those edge-cases can be specific to your business logic. Prompt LLM to come up with additional edge-cases that it might find useful. 

At a minimum, request: 

Boundary values: min/max, zero, empty string/collection, single-element, off-by-one Null / missing inputs: null, absent keys/fields, optional values missing 

Invalid formats: malformed JSON/CSV, invalid dates, illegal enum values, wrong encoding 

Exception/error paths: inputs that must trigger validation failures or thrown exceptions (use pytest.raises or equivalent) 

State/contract violations: precondition breaches, invalid state transitions (if applicable) Invariant/property checks: conditions that must always hold regardless of input 

Strong assertions: not just "test runs without crashing", but verify exact expected outputs, state changes, and side effects 

**Reasoning**: While LLMs can miss certain edge-cases that are essential for your business logic, they can also utilize its creativity and come up with potential mistakes you have not thought of. Without explicitly prompting LLM to do so, it would just implement the edgecases that you have described. Encourage LLM to be not just a test-typist but also a test–designer,

**Good example:**

Come up with tests for the file “[example.py](http://example.py)”.

Take into account these edgecases:

- Edge case 1:....  
- Edge case 2:...  
- ….

Also, take a look yourself and think what other edgecases there might be. Add them as well.

**Bad example:**

Come up with tests for the file “[example.py](http://example.py)”.

Take into account these edgecases:

- Edge case 1:....  
- Edge case 2:...  
- ….

## Results after using New Guideline

import math  
import sys  
from pathlib import Path  
import pytest

\# Ensure example.py in this folder is importable  
sys.path.insert(0, str(Path(\_\_file\_\_).resolve().parent))  
import example  
from datetime import datetime

\# \--- parse\_date tests \---

def test\_parse\_date\_whitespace\_padding():  
   dt \= example.parse\_date(' 2024-01-15 ')  
   assert isinstance(dt, datetime)  
   assert dt.year \== 2024 and dt.month \== 1 and dt.day \== 15

def test\_parse\_date\_unicode\_fullwidth\_digits\_rejected():  
   \# Fullwidth (lookalike) digits should not be parsed by the current implementation  
   with pytest.raises(ValueError):  
       example.parse\_date('２０２４-０１-１５')

def test\_parse\_date\_feb29\_non\_leap\_year\_raises():  
   with pytest.raises(ValueError):  
       example.parse\_date('2019-02-29')

def test\_parse\_date\_dec31\_and\_jan1\_boundary():  
   d1 \= example.parse\_date('2023-12-31')  
   d2 \= example.parse\_date('2024-01-01')  
   assert d1.year \== 2023 and d1.month \== 12 and d1.day \== 31  
   assert d2.year \== 2024 and d2.month \== 1 and d2.day \== 1

def test\_parse\_date\_ambiguous\_day\_first\_behavior():  
   \# The implementation expects day-first for slash format  
   d \= example.parse\_date('01/02/2024')  
   assert d.day \== 1 and d.month \== 2 and d.year \== 2024

def test\_parse\_date\_empty\_string\_raises():  
   with pytest.raises(ValueError):  
       example.parse\_date('')

def test\_parse\_date\_none\_raises\_attribute\_error():  
   with pytest.raises(AttributeError):  
       example.parse\_date(None)

\# Additional edgecases for parse\_date

def test\_parse\_date\_short\_month\_name():  
   d \= example.parse\_date('Jan 15 2024')  
   assert d.month \== 1 and d.day \== 15 and d.year \== 2024

\# \--- normalize\_username tests \---

def test\_normalize\_username\_tabs\_and\_newlines():  
   raw \= "  Alice\\tBob\\nCarol  "  
   norm \= example.normalize\_username(raw)  
   \# whitespace collapsed to single underscores and trimmed  
   assert norm \== 'alice\_bob\_carol'

def test\_normalize\_username\_unicode\_nbsp\_and\_spaces():  
   raw \= '\\u00a0User\\u00a0Name\\u00a0'  
   norm \= example.normalize\_username(raw)  
   assert norm \== 'user\_name'

def test\_normalize\_username\_all\_whitespace\_raises():  
   with pytest.raises(ValueError):  
       example.normalize\_username('   \\t\\n  ')

def test\_normalize\_username\_unicode\_sharp\_s\_behavior\_and\_idempotency():  
   \# 'ß' remains when using .lower() in this implementation (not casefold)  
   raw \= 'Maß'  
   norm \= example.normalize\_username(raw)  
   assert norm \== 'maß'  
   \# idempotency: running again yields same result  
   assert example.normalize\_username(norm) \== norm

def test\_normalize\_username\_very\_long\_string():  
   long \= 'User' \+ (' ' \* 1000) \+ 'Name'  
   norm \= example.normalize\_username(long)  
   assert norm.startswith('user\_') and norm.endswith('\_name')

def test\_normalize\_username\_already\_normalized\_idempotent():  
   s \= 'alice'  
   assert example.normalize\_username(s) \== 'alice'

\# \--- merge\_configs tests \---

def test\_merge\_configs\_with\_empty\_base():  
   base \= {}  
   override \= {'a': 1}  
   res \= example.merge\_configs(base, override)  
   assert res \== {'a': 1}

def test\_merge\_configs\_with\_empty\_override\_returns\_copy\_of\_base():  
   base \= {'a': {'b': 2}}  
   override \= {}  
   res \= example.merge\_configs(base, override)  
   assert res \== base and res is not base

def test\_merge\_configs\_type\_collision\_override\_scalar\_wins():  
   base \= {'k': {'inner': 1}}  
   override \= {'k': 42}  
   res \= example.merge\_configs(base, override)  
   assert res\['k'\] \== 42

def test\_merge\_configs\_deeply\_nested():  
   base \= {'a': {'b': {'c': 1}}, 'x': 0}  
   override \= {'a': {'b': {'d': 2}}, 'x': None}  
   res \= example.merge\_configs(base, override)  
   assert res\['a'\]\['b'\]\['c'\] \== 1  
   assert res\['a'\]\['b'\]\['d'\] \== 2  
   assert 'x' in res and res\['x'\] is None

def test\_merge\_configs\_keys\_with\_none\_values\_override():  
   base \= {'a': 1, 'b': 2}  
   override \= {'b': None}  
   res \= example.merge\_configs(base, override)  
   assert res\['b'\] is None

def test\_merge\_configs\_non\_string\_keys\_and\_identity\_merge():  
   base \= {1: {'nested': True}}  
   \# Pass same object as both args to ensure function handles it  
   res \= example.merge\_configs(base, base)  
   \# keys should be present, and result should be equivalent to base  
   assert 1 in res and res\[1\]\['nested'\] is True  
   \# ensure it's a new dict object (shallow copy behavior)  
   assert res is not base

\# \--- calculate\_discount tests \---

def test\_calculate\_discount\_zero\_and\_hundred\_boundaries():  
   assert example.calculate\_discount(100.0, 0) \== 100.00  
   res \= example.calculate\_discount(100.0, 100)  
   assert res \== 0.00  
   \# ensure it's \+0.0 not \-0.0  
   assert math.copysign(1.0, res) \== 1.0

def test\_calculate\_discount\_negative\_price\_allowed():  
   \# Current implementation allows negative prices (shouldn't crash)  
   assert example.calculate\_discount(\-50.0, 10) \== round(\-50.0 \* 0.9, 2)

def test\_calculate\_discount\_float\_precision\_rounding():  
   \# 0.1 \+ 0.2 precision quirks should be handled by rounding to 2 decimals  
   price \= 0.1 \+ 0.2  
   assert example.calculate\_discount(price, 0) \== round(price, 2)

def test\_calculate\_discount\_nan\_and\_inf\_inputs():  
   nan\_price \= float('nan')  
   inf\_price \= float('inf')  
   res\_nan \= example.calculate\_discount(nan\_price, 0)  
   assert math.isnan(res\_nan)  
   res\_inf \= example.calculate\_discount(inf\_price, 0)  
   assert math.isinf(res\_inf) and res\_inf \> 0

def test\_calculate\_discount\_invalid\_discount\_raises():  
   with pytest.raises(ValueError):  
       example.calculate\_discount(10.0, \-1)  
   with pytest.raises(ValueError):  
       example.calculate\_discount(10.0, 101)

def test\_calculate\_discount\_100\_percent\_on\_zero\_price():  
   res \= example.calculate\_discount(0.0, 100)  
   assert res \== 0.0 and math.copysign(1.0, res) \== 1.0

## 

## Analysis of two test files done by GPT-5-mini

*Test\_example\_pytest.py \- tests after using guideline*  
*Test\_example.py \- test after using original guideline*

Progress: I read both tests and compared their coverage.

* Files compared: test\_example\_pytest.py and test\_example.py

Findings (concise):

* Scope: Both target the same functions (parse\_date, normalize\_username, merge\_configs, calculate\_discount) and exercise many similar cases.  
* test\_example\_pytest.py: More nuanced assertions and edge checks — type checks (isinstance), idempotency, explicit handling of None vs. AttributeError, checks for Unicode NBSP and fullwidth digits, explicit sign checks via math.copysign, NaN/Inf behavior with sign, short month-name parsing, and object-identity/assert-copy expectations for merges.  
* test\_example.py: Covers a few extra format variants (additional unicode-lookalike digit cases and more ambiguous-day examples) and mirrors many merge/discount scenarios, but its assertions are generally simpler (direct equality or presence).  
* Differences in failure expectations: they disagree on the exception type for parse\_date(None) (one expects AttributeError, the other TypeError), which is important for spec clarity.

Conclusion:

* **Overall, test\_example\_pytest.py is richer and covers more edge cases and nuanced behaviors (types, idempotency, sign semantics, specific Unicode behaviors).** test\_example.py is comprehensive too but a bit more focused on straightforward value-equality checks and extra format variants.

