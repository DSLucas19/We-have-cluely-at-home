# AI Assistant - Background Screenshot Analysis Application

A Windows system tray application that captures screenshots via global hotkeys, analyzes them using Gemini AI in thinking mode, and automatically pastes solutions.

## Features

- 🔥 **Global Hotkey**: Trigger screenshot capture with a customizable key combination (default: `Ctrl+Shift+Alt+A`)
- 📸 **Silent Screenshot**: Captures screen without switching windows or interrupting workflow
- 🤖 **Gemini AI Integration**: Uses Gemini 3 Flash, the latest generation model with PhD-level reasoning
- 📋 **Auto-Paste**: Automatically pastes AI response at cursor position
- 🎯 **System Tray**: Always-running background service with easy enable/disable
- ⚙️ **Configurable**: Full settings UI for customization
- 🚀 **Startup Support**: Optional auto-launch on Windows startup

## Installation

1. **Install Python 3.8+** (if not already installed)

2. **Install dependencies**:
   ```bash
   cd ai_assistant
   pip install -r requirements.txt
   ```

3. **Get Gemini API Key**:
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Create a free API key
   - Keep it handy for configuration

## Configuration

1. **First Run**: 
   ```bash
   python main.py
   ```

2. **Configure API Key**:
   - Right-click the system tray icon
   - Click "Settings..."
   - Enter your Gemini API key
   - Customize system prompt if desired
   - Click "Save"

3. **Restart** the application for changes to take effect

## Usage

1. **Start the application**: `python main.py`
2. **The system tray icon** will appear (brain/chip icon)
3. **Press your hotkey** (default: `Ctrl+Shift+Alt+A`) anywhere on your system
4. **Wait** for the AI to analyze the screenshot (~2-5 seconds)
5. **Response is pasted** automatically at your cursor position!

### System Tray Menu

- **✓/✗ AI Assistant**: Shows current status (enabled/disabled)
- **Hotkey**: Displays current hotkey combination
- **Enable/Disable Assistant**: Toggle functionality on/off
- **Settings...**: Open configuration window
- **Exit**: Close the application

## Configuration Options

### Settings Window

- **Hotkey Configuration**: Set custom key combination
- **Gemini API Key**: Your Google AI API key
- **System Prompt**: Customize how the AI responds
- **Auto-paste response**: Toggle automatic pasting (vs clipboard-only)
- **Launch on Windows startup**: Auto-start with Windows
- **Restore clipboard after paste**: Preserve original clipboard content
- **Paste delay**: Milliseconds to wait before pasting

### Config File (`config.json`)

```json
{
  "hotkey": "ctrl+shift+alt+a",
  "gemini": {
    "api_key": "YOUR_API_KEY_HERE",
    "model": "gemini-3.0-flash",
    "system_prompt": "Analyze this screenshot and provide a solution..."
  },
  "auto_paste": {
    "enabled": true,
    "delay_ms": 500,
    "restore_clipboard": false
  },
  "screenshot": {
    "mode": "full_screen",
    "save_to_disk": false
  },
  "startup": {
    "launch_on_boot": false
  },
  "logging": {
    "level": "INFO",
    "save_logs": true
  }
}
```

## Project Structure

```
ai_assistant/
├── main.py                    # Entry point
├── config_manager.py          # Configuration management
├── logger.py                  # Logging system
├── screenshot_capture.py      # Screenshot functionality
├── gemini_integration.py      # AI integration
├── auto_paste.py              # Auto-paste mechanism
├── hotkey_listener.py         # Global hotkey handler
├── system_tray.py             # System tray integration
├── startup_manager.py         # Windows startup management
├── settings_window.py         # Settings GUI
├── requirements.txt           # Dependencies
├── config.json               # Configuration file
├── assets/
│   ├── icon.png              # System tray icon (enabled)
│   └── icon_disabled.png     # System tray icon (disabled)
└── logs/
    └── ai_assistant.log      # Application logs
```

## Use Cases

- **Coding Assistance**: Capture error messages and get instant solutions
- **Math Problems**: Screenshot equations and get step-by-step solutions
- **Language Translation**: Capture text and get translations
- **General Questions**: Screenshot any content for AI analysis
- **Code Review**: Capture code snippets for suggestions

## Tips

- Use a unique hotkey combination to avoid conflicts
- Set a descriptive system prompt for better results
- Enable "Launch on startup" for always-available assistance
- Check logs directory for debugging issues
- Test the API connection in settings before first use

## Troubleshooting

### Hotkey not working
- Check if another application is using the same key combination
- Try a different hotkey in Settings
- Restart the application after changing settings

### API errors
- Verify your API key is correct
- Check internet connection
- Ensure you haven't exceeded rate limits
- Test connection in Settings window

### Auto-paste not working
- Increase paste delay in Settings
- Disable and use clipboard-only mode
- Check if target application blocks automated input

### System tray icon not appearing
- Check Task Manager for running process
- Look in hidden icons area (click ^ in system tray)
- Restart the application

## Security & Privacy

⚠️ **Important Considerations**:

- Screenshots may contain sensitive information - they are sent to Gemini API
- API key is stored in plain text in `config.json` (keep file secure)
- Auto-paste may be detected by anti-cheat or proctoring software
- Logs may contain screenshot metadata

## License

This project is for personal use. Ensure compliance with Gemini API terms of service.

## Support

For issues or questions:
1. Check logs in `logs/ai_assistant.log`
2. Review configuration in `config.json`
3. Test individual components in Settings window
