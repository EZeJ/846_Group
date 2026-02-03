# Prompt and answer without following guideline (GPT-4o)

User: Create some FAQ questions and answers about an adoption day event. look at info at week4/drafts/updated_guideline_4/adoption_day_info_sheet.txt

GitHub Copilot: Read [](file:///Users/sofiiatkach/Desktop/LLM/846_Group/week4/drafts/updated_guideline_4/adoption_day_info_sheet.txt)

Using "Edit File"

Using ""


I have added a FAQ section to the adoption day info sheet, addressing common questions based on the provided details. Let me know if you need further adjustments!

Made changes.

User: write answers here in chat

GitHub Copilot: Here are the FAQ questions and answers based on the adoption day info sheet:

---

**Q: What is "Paws & Parks Adoption Day"?**  
A: It is a one-day outdoor pet adoption and community event run by local shelters and volunteers.

**Q: Where and when is the event happening?**  
A: The event will take place at Riverside Park (main pavilion) on Saturday, April 18, from 11:00 a.m. to 4:00 p.m.

**Q: Who will be participating in the event?**  
A: Three local shelters will bring dogs and cats. Volunteer trainers will offer short “meet & greet” coaching sessions, and a local vet clinic will provide microchip checks (no vaccinations).

**Q: Can I adopt a pet on the same day?**  
A: Same-day adoptions are possible, but approval depends on each shelter. Some animals may require a home visit after the event.

**Q: What should I bring if I want to adopt a pet?**  
A: Bring a photo ID. Note that adoption fees vary by shelter and by animal.

**Q: Are kids allowed at the event?**  
A: Yes, kids are welcome but must stay with an adult at all times.

**Q: Can I bring my own dog to the event?**  
A: Yes, but your dog must stay leashed and away from the adoption area.

**Q: What happens if it rains?**  
A: The event will run rain or shine. Updates for severe weather will be posted the morning of the event.

**Q: Are there any details not specified in the info sheet?**  
A: Yes, the sheet does not specify exact adoption fees, parking details, whether credit cards are accepted, or the shelters’ full approval criteria.

--- 

Let me know if you need further edits!




# Prompt and answer  following guideline (GPT-5-mini)


User: Create some FAQ questions and answers about an adoption day event. look at info at week4/drafts/updated_guideline_4/adoption_day_info_sheet.txt

GitHub Copilot: Read [](file:///Users/sofiiatkach/Desktop/LLM/846_Group/week4/drafts/updated_guideline_4/adoption_day_info_sheet.txt)

Using "Edit File"

Using ""

I have added a FAQ section to the adoption day info sheet, addressing common questions based on the provided details. Let me know if you need further adjustments!

Made changes.

User: write answers here in chat

GitHub Copilot: Here are the FAQ questions and answers based on the adoption day info sheet:

---

**Q: What is "Paws & Parks Adoption Day"?**  
A: It is a one-day outdoor pet adoption and community event run by local shelters and volunteers.

**Q: Where and when is the event happening?**  
A: The event will take place at Riverside Park (main pavilion) on Saturday, April 18, from 11:00 a.m. to 4:00 p.m.

**Q: Who will be participating in the event?**  
A: Three local shelters will bring dogs and cats. Volunteer trainers will offer short “meet & greet” coaching sessions, and a local vet clinic will provide microchip checks (no vaccinations).

**Q: Can I adopt a pet on the same day?**  
A: Same-day adoptions are possible, but approval depends on each shelter. Some animals may require a home visit after the event.

**Q: What should I bring if I want to adopt a pet?**  
A: Bring a photo ID. Note that adoption fees vary by shelter and by animal.

**Q: Are kids allowed at the event?**  
A: Yes, kids are welcome but must stay with an adult at all times.

**Q: Can I bring my own dog to the event?**  
A: Yes, but your dog must stay leashed and away from the adoption area.

**Q: What happens if it rains?**  
A: The event will run rain or shine. Updates for severe weather will be posted the morning of the event.

**Q: Are there any details not specified in the info sheet?**  
A: Yes, the sheet does not specify exact adoption fees, parking details, whether credit cards are accepted, or the shelters’ full approval criteria.

--- 

Let me know if you need further edits!



# Summary: Why the Guideline-Based Prompt Produces Better Results

The second prompt (following **Updated Guideline 4**) leads to better results because it **explicitly constrains the model’s behavior**, even if the surface-level answers look similar in this example.

### Key Improvements in the Guideline-Based Prompt
- **Clear constraints**: It specifies the exact number of Q&A pairs, the required format (`Q:` / `A:`), and forbids extra text.
- **Reduced ambiguity**: The model is told to rely only on the provided file, lowering the risk of hallucinated or irrelevant information.
- **Few-shot learning**: The inclusion of a **positive example** (correct format) and a **negative example** (common mistakes) clarifies expectations more effectively than instructions alone.
- **Better generalization**: By stating that examples demonstrate *format and constraints only*, the model is less likely to blindly copy content and more likely to satisfy the underlying rules.