# AI Assistant - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
cd f:\App\Anti-gravity\AIHELPME\ai_assistant
pip install -r requirements.txt
```

### Step 2: Get Your API Key
1. Visit: https://aistudio.google.com/
2. Sign in with Google account
3. Click "Get API Key"
4. Copy your key

### Step 3: Run & Configure
```bash
python main.py
```

1. System tray icon will appear
2. Right-click icon → **Settings**
3. Paste your API key
4. Click **Save**
5. Restart the application

## ✨ Using the Application

### Trigger AI Analysis
Press: **Ctrl+Shift+Alt+A** (configurable)

That's it! The app will:
1. Capture your screen silently
2. Send to Gemini AI
3. Auto-paste the solution

### System Tray Menu
- **Enable/Disable**: Toggle functionality on/off
- **Settings**: Configure hotkey, API key, prompts
- **Exit**: Close the application

## ⚙️ Common Settings

### Change Hotkey
Settings → Type new combination → Save

### Customize AI Behavior
Settings → System Prompt → Edit → Save

### Launch on Startup
Settings → ☑ Launch on Windows startup → Save

## 📝 Example Use Cases

| Scenario | Action |
|----------|--------|
| **Error message** | Press hotkey → Get solution pasted |
| **Math problem** | Press hotkey → Get step-by-step solution |
| **Code question** | Press hotkey → Get explanation |
| **Translation** | Press hotkey → Get translated text |

## 🔧 Troubleshooting

### Hotkey not working?
- Try a different key combination in Settings
- Restart the application
- Check if another app is using that hotkey

### API errors?
- Verify API key is correct
- Check internet connection
- Test connection in Settings window

### Nothing happens when pressing hotkey?
- Check system tray icon (enabled vs disabled)
- Look for the brain/chip icon in system tray
- Enable the assistant from the menu

## 📄 More Help

- Full documentation: See `README.md`
- Configuration reference: See `config.json`
- Logs: Check `logs/ai_assistant.log`
- Walkthrough: See artifact walkthrough.md

---

**Made with ❤️ for seamless AI assistance**
