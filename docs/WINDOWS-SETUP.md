# Complete Windows Setup Guide for ShowUp

**Step-by-step guide for setting up the ShowUp project on Windows, designed for AI-assisted development.**

---

## 📋 Prerequisites Checklist

Before starting, you'll need to install:

- [ ] Python 3.11 or higher
- [ ] VS Code
- [ ] Git (optional but recommended)

---

## 🔧 Step 1: Install Python

### **Download and Install**

1. Go to https://www.python.org/downloads/
2. Download the latest Python 3.11+ installer for Windows
3. **IMPORTANT:** Check ✅ "Add Python to PATH" during installation
4. Click "Install Now"

### **Verify Installation**

Open Command Prompt (Win + R, type `cmd`, press Enter) and type:

```bash
python --version
```

You should see something like: `Python 3.11.5`

If you get an error, Python wasn't added to PATH. Reinstall and make sure to check that box!

---

## 💻 Step 2: Install VS Code

### **Download and Install**

1. Go to https://code.visualstudio.com/
2. Download the Windows installer
3. Run the installer with default settings
4. Launch VS Code

### **Install Essential Extensions**

In VS Code:
1. Click the Extensions icon (left sidebar, looks like squares)
2. Search for and install:
   - **Python** (by Microsoft)
   - **Pylance** (by Microsoft) - usually comes with Python extension
   - **GitHub Copilot** (optional, $10/month - VERY helpful)

---

## 📦 Step 3: Download the Project

### **Option A: Using Git (Recommended)**

```bash
# In Command Prompt or VS Code Terminal:
git clone https://github.com/jbulliner82/showup-appointment-predictor.git
cd showup-appointment-predictor
```

### **Option B: Download ZIP**

1. Go to the GitHub repository
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file to a folder like `C:\Projects\showup-appointment-predictor`
4. Open Command Prompt and navigate to that folder:
   ```bash
   cd C:\Projects\showup-appointment-predictor
   ```

---

## 🐍 Step 4: Set Up Python Virtual Environment

A virtual environment keeps this project's dependencies separate from other Python projects.

### **Create Virtual Environment**

```bash
# Make sure you're in the project's backend folder:
cd backend

# Create virtual environment (this creates a 'venv' folder):
python -m venv venv
```

### **Activate Virtual Environment**

**Every time you work on this project, you need to activate the virtual environment first!**

```bash
# Windows Command Prompt:
venv\Scripts\activate

# Windows PowerShell (if cmd doesn't work):
venv\Scripts\Activate.ps1
```

You'll know it's activated when you see `(venv)` at the beginning of your command line.

**To deactivate later:**
```bash
deactivate
```

---

## 📚 Step 5: Install Dependencies

With your virtual environment activated:

```bash
# Install all required Python packages:
pip install -r requirements.txt

# This will take a few minutes...
```

If you get errors, try:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## ⚙️ Step 6: Configure Environment Variables

### **Create .env File**

```bash
# Copy the example file:
copy .env.example .env
```

### **Edit .env File**

Open `.env` in VS Code or Notepad and fill in your API keys:

```env
# Database (leave as-is for now, SQLite is fine for development)
DATABASE_URL=sqlite:///./showup.db

# Twilio - Get free account at https://www.twilio.com/try-twilio
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+15551234567

# SendGrid - Get free account at https://sendgrid.com/
SENDGRID_API_KEY=your_sendgrid_api_key_here
SENDGRID_FROM_EMAIL=noreply@showup.app

# Application settings (leave as-is for now)
SECRET_KEY=change-this-to-something-random
DEBUG=True
ENVIRONMENT=development
```

**Don't have API keys yet?** That's okay! You can set up Twilio and SendGrid later. The app will run without them initially.

---

## 🗄️ Step 7: Initialize Database

```bash
# Still in the backend folder with venv activated:
python -c "from app.database import init_db; init_db()"
```

You should see:
```
Creating database tables...
✅ Database initialized successfully!
```

This creates a `showup.db` file in your backend folder.

---

## 🚀 Step 8: Run the Application

```bash
# Start the FastAPI server:
python -m uvicorn app.main:app --reload
```

You should see:
```
🚀 ShowUp API starting up...
📊 Environment: development
✅ API running at: http://localhost:8000
📚 API docs at: http://localhost:8000/docs
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### **Test It Works**

Open your browser and go to:
- http://localhost:8000 - Should show API health check
- http://localhost:8000/docs - Interactive API documentation

**Success!** Your backend is now running! 🎉

---

## 🎨 Step 9: Open in VS Code

```bash
# From your project root folder:
code .
```

This opens the entire project in VS Code.

### **Recommended VS Code Setup**

1. **Open Terminal** in VS Code: `View` → `Terminal` or `Ctrl + ` `
2. **Activate venv** in the terminal (same command as before)
3. **Select Python Interpreter**: 
   - Press `Ctrl + Shift + P`
   - Type "Python: Select Interpreter"
   - Choose the one that says `venv` in the path

Now VS Code will use the correct Python environment!

---

## 🤖 Step 10: Start Coding with AI

### **Using GitHub Copilot** (if installed)

Just start typing what you want, and Copilot will suggest code!

Example:
```python
# Type this comment:
# Create a function to calculate no-show risk based on patient history

# Copilot will suggest the function code!
```

### **Using Claude (me!) for Help**

When you need help, describe what you're trying to do:

**Good AI prompt:**
```
I need to add a new endpoint to app/main.py that:
- Accepts appointment data (POST request)
- Stores it in the database
- Returns the created appointment

Please show me the complete code with comments.
```

**What to include when asking for help:**
1. What you're trying to do
2. Any error messages (full text)
3. Relevant code
4. What you've already tried

---

## 🔄 Daily Workflow

Every time you start working on the project:

```bash
# 1. Navigate to backend folder
cd C:\Projects\showup-appointment-predictor\backend

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Start the development server
python -m uvicorn app.main:app --reload

# Leave this terminal running, open a new one for other commands
```

---

## ⚠️ Common Issues & Solutions

### **"Python not found" error**

**Problem:** Python isn't in your PATH

**Solution:**
1. Uninstall Python
2. Reinstall, **checking the "Add Python to PATH" box**
3. Restart your computer

### **"pip not found" error**

**Problem:** pip isn't installed correctly

**Solution:**
```bash
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

### **"Cannot activate virtual environment"**

**Problem:** PowerShell execution policy

**Solution:** Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy RemoteSigned
```

Then try activating again with `venv\Scripts\Activate.ps1`

### **"Module not found" errors when running**

**Problem:** Virtual environment not activated or dependencies not installed

**Solution:**
```bash
# Make sure venv is activated (you should see (venv) in prompt)
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### **Port already in use**

**Problem:** Another app is using port 8000

**Solution:** Use a different port:
```bash
python -m uvicorn app.main:app --reload --port 8001
```

---

## 📱 Next Steps

Once your backend is running:

1. **Test the API** - Visit http://localhost:8000/docs and try the endpoints
2. **Start building features** - Follow the development roadmap in README.md
3. **Use AI to help** - Ask for code examples when you get stuck
4. **Commit your code** - Save your progress with Git

---

## 🆘 Getting Help

**If you're stuck:**

1. **Read the error carefully** - It usually tells you exactly what's wrong
2. **Google the error** - Add "python" to your search
3. **Ask AI** - Copy/paste the error and your code
4. **Check the docs** - FastAPI docs are excellent: https://fastapi.tiangolo.com/

**For AI assistance, ask like this:**

```
I'm getting this error:
[paste error]

In this code:
[paste code]

Context: I'm trying to [what you're doing]

What's wrong and how do I fix it?
```

---

## 🎯 You're Ready!

Your development environment is now set up and ready to go!

**What you can do now:**
- ✅ Run the FastAPI backend
- ✅ Access the API documentation
- ✅ Start building features
- ✅ Use AI to help you code

**Next:** Check out the main README.md for the development roadmap and start building your first feature!

---

**Happy coding! 🚀**
