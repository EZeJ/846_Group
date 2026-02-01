# USING CHAT 0:

lilianahotsko: Who argues that performance problems are caused by indexing, and who argues they are caused by schema design choices? Quote the relevant statements.

GitHub Copilot: Tom argues that performance problems are caused by indexing, while Jerry argues they are caused by schema design choices.

Relevant quotes:

Tom (indexing):
- "JOIN performance issues come from BAD INDEXING, not normalization."
- "Only if you don’t create proper INDEXES on the FOREIGN KEY columns."
- "That’s what INDEXES are for."

Jerry (schema design choices):
- "No, they come from you adding FOREIGN KEY constraints everywhere."
- "It is when every SELECT requires five JOIN operations just to render a dashboard."
- "And causes query planners to choke on overly complex JOIN trees."
- "Not when you force them to JOIN six tables to get a user profile."
- "No, it’s because we normalized USERS into five separate tables."


# USING CHAT 1:




# USING CHAT 2:

