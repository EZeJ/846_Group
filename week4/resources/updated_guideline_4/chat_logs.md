# Prompt and answer without following guideline (GPT-4o)

User: Create FAQ questions and answers about an adoption day event using the information in week4/drafts/updated_guideline_4/adoption_day_info_sheet.txt.

GitHub Copilot: Read [](file:///Users/sofiiatkach/Desktop/LLM/846_Group/week4/drafts/updated_guideline_4/adoption_day_info_sheet.txt)

Using "Edit File"

Using ""


I have added a FAQ section to the adoption day info sheet, addressing common questions based on the provided details. Let me know if you need further adjustments!

Made changes.

User: write answers here in chat

GitHub Copilot: Here are the FAQ questions and answers based on the adoption day info sheet:

---

Q: When and where is the event?
A: The adoption day will take place next Sunday morning at the city park near downtown.

Q: What animals can I adopt?
A: Visitors can adopt dogs, cats, rabbits, and small pets.

Q: Is there entertainment for children?
A: Yes, there will be games, face painting, and food trucks for families.

Q: Do I need to register in advance?
A: Yes, online registration is required before attending the event.

Q: Are adoption fees discounted during the event?
A: Adoption fees will be reduced for all animals adopted that day.

--- 

Let me know if you need further edits!



# Prompt and answer  following guideline (GPT-5-mini)


Create 10 visitor FAQ Q&A pairs about an adoption day event using only the information provided in
week4/drafts/updated_guideline_4/adoption_day_info_sheet.txt.

Constraints:

Use exactly the format Q: … / A: …

Do not invent, assume, or infer missing details

If information is not available, state that it is not specified

Keep answers short and factual

The following examples are provided only to demonstrate format and constraints, not to lock the model into the example’s domain.

Good example (follows format and constraints):
Q: Is registration required to attend?
A: Registration requirements are not specified in the information provided.

Bad example (common failure to avoid):
Q: Will there be free food and children’s activities?
A: Yes, free snacks and games will be available for all visitors.

Now generate the 10 FAQ Q&A pairs based strictly on the provided file.

GitHub Copilot: Read [](file:///Users/sofiiatkach/Desktop/LLM/846_Group/week4/drafts/updated_guideline_4/adoption_day_info_sheet.txt)

Using "Edit File"

Using ""

I have added a FAQ section to the adoption day info sheet, addressing common questions based on the provided details. Let me know if you need further adjustments!

Made changes.

User: write answers here in chat

GitHub Copilot: Here are the FAQ questions and answers based on the adoption day info sheet:

---
Q: When and where is the event?
A: Riverside Park (main pavilion) on Saturday, April 18, 11:00 a.m. to 4:00 p.m.

Q: What is the event?
A: A one-day outdoor pet adoption and community event run by local shelters and volunteers.

Q: Who is participating?
A: Three local shelters, a small team of volunteer trainers, and a local vet clinic.

Q: Which animals will be available?
A: Dogs and cats brought by three local shelters.

Q: Are same-day adoptions allowed?
A: Same-day adoptions are possible; approval depends on each shelter.

Q: Do I need to bring identification?
A: Bring a photo ID.

Q: Will there be veterinary services or vaccinations on site?
A: A local vet clinic will offer microchip checks; no vaccinations on site.

Q: Are home visits required after adoption?
A: Some animals require a home visit after the event; timing varies.

Q: Are credit cards accepted for adoption fees?
A: Whether credit cards are accepted is not specified.

Q: What happens if the weather is bad?
A: The event runs rain or shine; severe weather updates will be posted the morning of the event. 

--- 

Let me know if you need further edits!



# Summary: Why the Guideline-Based Prompt Produces Better Results

The second prompt (following **Updated Guideline 4**) leads to better results because it **explicitly constrains the model’s behavior**, even if the surface-level answers look similar in this example.

### Key Improvements in the Guideline-Based Prompt
- **Clear constraints**: It specifies the exact number of Q&A pairs, the required format (`Q:` / `A:`), and forbids extra text.
- **Reduced ambiguity**: The model is told to rely only on the provided file, lowering the risk of hallucinated or irrelevant information.
- **Few-shot learning**: The inclusion of a **positive example** (correct format) and a **negative example** (common mistakes) clarifies expectations more effectively than instructions alone.
- **Better generalization**: By stating that examples demonstrate *format and constraints only*, the model is less likely to blindly copy content and more likely to satisfy the underlying rules.