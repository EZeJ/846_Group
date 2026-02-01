# Exercise 1: How Role Formatting Affects LLM Understanding?

In this exercise, you will test how different dialogue formats affect an LLM’s ability to correctly interpret a technical discussion. (Updated guideline 6).

You will use the same conversation between TOM and JERRY, who are debating database schema design. Their discussion includes many capitalized SQL terms (e.g., JOIN, FOREIGN KEY, SELECT), which makes this a challenging case for speaker tracking.

Example prompt:
Who argues that performance problems are caused by indexing, and who argues they are caused by schema design choices? Quote the relevant statements.

Files to use:
Step 0: Use the regular version only of the chat. (file chat_0.txt)
Step 1: Use the version with capitalization of the chat. (file chat_1.txt)
Step 2: Use the json formatted version of the chat. (file chat_2.txt)

Task:
Analyze which format made it easier for the model to track each speaker’s position?