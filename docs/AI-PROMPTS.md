# AI-Assisted Development Guide

**How to use AI (like me!) to help you build the ShowUp project**

---

## 🤖 Why AI-Assisted Development Works

You don't need to be an expert programmer to build real applications anymore. With AI assistants like:
- **Claude** (me!)
- **GitHub Copilot**
- **ChatGPT**
- **Cursor AI**

You can build professional-quality software by describing what you want in plain English.

**The key:** Asking the right questions and knowing how to work with AI effectively.

---

## 🎯 Golden Rules of AI-Assisted Coding

### **Rule #1: Be Specific**

❌ **Bad:** "Help me with the database"  
✅ **Good:** "I need to create a database table for appointments that stores: appointment_datetime, patient_id, status, and notes. Show me the SQLAlchemy model code."

### **Rule #2: Provide Context**

Always include:
- What you're trying to do
- What code you already have
- What errors you're getting (full error text)
- What you've already tried

### **Rule #3: Ask for Explanations**

Don't just copy code - understand it!

After getting code, ask:
- "Explain what each part of this code does"
- "Why did you use X instead of Y?"
- "What could go wrong with this approach?"

### **Rule #4: Iterate**

It's okay if the first response isn't perfect. Follow up with:
- "This works, but how can I also add [feature]?"
- "I'm getting this error: [error]. How do I fix it?"
- "Can you show me a better way to do this?"

### **Rule #5: Test Everything**

AI makes mistakes! Always:
- Run the code
- Test it with different inputs
- Ask AI to help you write tests

---

## 📝 Prompt Templates for Common Tasks

### **1. Creating a New Feature**

```
I need to add [feature name] to my ShowUp project.

Current setup:
- Using FastAPI with SQLAlchemy
- Database models in app/models.py
- Main app in app/main.py

The feature should:
- [requirement 1]
- [requirement 2]
- [requirement 3]

Please provide:
1. Complete code with comments
2. Where to put the code in my project structure
3. Any new dependencies I need to install
```

**Example:**
```
I need to add a "send reminder" feature to my ShowUp project.

Current setup:
- Using FastAPI with SQLAlchemy
- Database models in app/models.py (Appointment, Patient, Reminder models exist)
- Main app in app/main.py

The feature should:
- Send SMS using Twilio
- Accept appointment_id as input
- Create a Reminder record in database
- Return success/failure status

Please provide:
1. Complete code with comments
2. Where to put the code in my project structure
3. Any new dependencies I need to install
```

### **2. Debugging an Error**

```
I'm getting this error:
[paste FULL error message, including stack trace]

In this code:
[paste the relevant code]

Context:
- I'm trying to [what you were doing]
- This happens when [when the error occurs]
- I've tried [what you've attempted]

What's wrong and how do I fix it?
```

### **3. Understanding Existing Code**

```
Please explain this code line by line:

[paste code]

Specifically, I don't understand:
- [specific part 1]
- [specific part 2]

Please explain in simple terms how it works.
```

### **4. Adding to Existing Code**

```
I have this working code:
[paste current code]

I want to add:
[describe new functionality]

Please show me:
1. The modified code with changes highlighted
2. What changed and why
3. Any potential issues to watch for
```

### **5. Writing Tests**

```
I need tests for this function:
[paste function code]

Please write pytest tests that check:
- Normal cases (happy path)
- Edge cases
- Error handling

Show me complete test code with comments.
```

### **6. Improving Code Quality**

```
Can you review this code and suggest improvements?
[paste code]

Specifically, look for:
- Bugs or errors
- Better ways to do things
- Security issues
- Performance problems

Explain each suggestion.
```

---

## 🛠️ Feature-Specific Prompts for ShowUp

### **ML Model Development**

```
I need to create a machine learning model to predict appointment no-shows.

Dataset has these features:
- patient_history (no-show rate)
- days_in_advance (how far ahead they booked)
- appointment_day_of_week
- appointment_time_of_day
- is_new_patient
- previous_no_shows

Target variable: did_noshow (True/False)

Please provide:
1. Code to load and prepare the data
2. Train a logistic regression model with scikit-learn
3. Evaluate the model (accuracy, precision, recall)
4. Save the trained model
5. Create a predict function that takes new appointment data

Include all imports and comments explaining each step.
```

### **API Endpoint Creation**

```
I need to create a FastAPI endpoint for [purpose].

Endpoint should:
- URL: POST /api/[endpoint-name]
- Accept: [list fields]
- Validate: [validation rules]
- Do: [what it should do]
- Return: [response format]

Current code structure:
- Using app/main.py for routes
- Database session via get_db() dependency
- Models defined in app/models.py

Please show me complete endpoint code with error handling.
```

### **Database Operations**

```
I need to [operation] in the database.

Model: [model name from app/models.py]
Operation: [create/read/update/delete]
Conditions: [any specific requirements]

Please show me:
1. The database query code
2. Error handling
3. How to use it in a FastAPI endpoint
```

### **Integration (Twilio, SendGrid, etc.)**

```
I need to integrate [service name] into my ShowUp project.

Purpose: [what you want to do with it]
API Key stored in: .env file as [ENV_VAR_NAME]

Please provide:
1. Installation command (pip install...)
2. Configuration code
3. Function to [specific task]
4. Error handling
5. Example usage

Include all imports and environment variable handling.
```

---

## 🎓 Learning While Building

### **Understanding Patterns**

When AI gives you code, ask follow-up questions:

**After getting a database query:**
```
Why did you use filter() instead of filter_by()?
When should I use each one?
```

**After getting async code:**
```
What does 'async' and 'await' do here?
When do I need to use them vs regular functions?
```

**After getting error handling:**
```
Explain the try/except block.
What other exceptions should I catch here?
```

### **Building Your Understanding**

For each major component, ask:
1. "How does this work?"
2. "What happens if [edge case]?"
3. "How would I modify this to [variation]?"
4. "What are common problems with this approach?"

---

## 🚧 When AI Gets It Wrong

AI isn't perfect! Here's how to handle issues:

### **Code Doesn't Run**

1. **Copy the FULL error message**
2. **Paste it back to AI** with: "I got this error when running your code: [error]"
3. **Include the code** that caused the error
4. AI will usually fix it immediately

### **Code Runs But Doesn't Work Right**

1. **Describe what happens** vs what should happen
2. **Show example input/output**
3. **Ask for debugging help:**
   ```
   The code runs without errors, but:
   - When I input [X], I get [Y]
   - But I expected [Z]
   
   Here's the code:
   [paste code]
   
   What's wrong?
   ```

### **Don't Understand the Solution**

Never copy code you don't understand!

Ask:
```
I don't understand this code:
[paste confusing part]

Can you:
1. Explain it in simpler terms
2. Show a simpler version
3. Give an analogy
4. Break it down step-by-step
```

---

## 💡 Advanced AI Techniques

### **Asking for Alternatives**

```
You showed me [approach].
What are other ways to do this?
What are the pros/cons of each?
```

### **Requesting Best Practices**

```
Is this code following Python best practices?
How would an experienced developer write this?
What could I improve?
```

### **Planning Before Coding**

```
Before writing code, can you:
1. Outline the approach
2. List the steps
3. Identify potential problems
4. Suggest the best way forward

Then we'll implement it.
```

### **Code Review**

```
Please review this code as if you were a senior developer:

[paste code]

Look for:
- Bugs
- Security issues
- Performance problems
- Better approaches
- Missing error handling
```

---

## 🎯 ShowUp Project Workflow

### **Adding a New Feature (Step-by-Step)**

**Step 1: Plan with AI**
```
I want to add [feature] to ShowUp.
What's the best approach?
What files will I need to create/modify?
What are the steps?
```

**Step 2: Get Code Structure**
```
Please create the code structure for [feature]:
- Database models (if needed)
- API endpoints
- Helper functions
Show me where each piece goes in my project.
```

**Step 3: Implement Step-by-Step**
```
Let's implement step 1: [first step]
[paste current code if modifying]
Show me the code with comments.
```

**Step 4: Test**
```
How do I test this feature?
Show me example API calls and expected responses.
```

**Step 5: Document**
```
Help me write documentation for this feature:
- What it does
- How to use it
- API endpoint details
- Example usage
```

---

## 🔄 Iterative Development Example

**You:** "I need to create an endpoint that accepts appointment data and stores it in the database."

**AI:** [provides code]

**You:** "This works! Now I want to also validate that the appointment_datetime is in the future."

**AI:** [provides updated code]

**You:** "Great! Now I want to automatically create a Patient record if the patient_code doesn't exist yet."

**AI:** [provides further updated code]

**You:** "Perfect! Now show me how to write tests for this endpoint."

**AI:** [provides test code]

This is how you build complex features - one step at a time!

---

## 📚 Resources

**For when AI can't help:**

- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **SQLAlchemy Docs:** https://docs.sqlalchemy.org/
- **scikit-learn Docs:** https://scikit-learn.org/
- **Python Docs:** https://docs.python.org/3/

**Community:**
- **Stack Overflow:** For specific errors
- **Reddit r/learnpython:** For questions
- **FastAPI Discord:** For FastAPI-specific help

---

## ✨ Remember

**You don't need to know everything!**

- AI fills in the knowledge gaps
- You learn by doing and asking
- Every feature you build teaches you more
- It's okay to ask "basic" questions
- Experienced developers use AI too!

**The goal:** Build a working project while learning along the way.

---

**Happy AI-assisted coding! 🚀🤖**
