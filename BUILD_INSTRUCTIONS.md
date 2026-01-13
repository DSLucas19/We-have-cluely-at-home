# Building AI Assistant Executable

This guide explains how to package the AI Assistant into a standalone `.exe` file for Windows.

## Prerequisites

1. **Python 3.8+** installed
2. All dependencies from `requirements.txt` installed
3. PyInstaller (will be auto-installed by build script)

## Quick Build

### Option 1: Using Build Script (Recommended)

Simply run the build script:

```batch
build.bat
```

This will:
- Install PyInstaller if needed
- Clean previous builds
- Build the executable
- Show the output location

### Option 2: Using Spec File

```batch
pip install pyinstaller
pyinstaller AI_Assistant.spec
```

### Option 3: Manual Command

```batch
pyinstaller --name="AI_Assistant" --onefile --windowed main.py
```

## Output

The executable will be created at:
```
dist\AI_Assistant.exe
```

## Distribution

To distribute the application:

1. **Copy the executable**:
   ```
   dist\AI_Assistant.exe
   ```

2. **Create a deployment folder** with:
   ```
   AI_Assistant/
   ├── AI_Assistant.exe
   └── config.json (user must add their API key)
   ```

3. **User Instructions**:
   - Users need to add their Gemini API key to `config.json`
   - First run will create default `config.json` if missing
   - Logs will be saved in `logs/` directory

## Configuration

Users should create a `config.json` file in the same directory as the `.exe`:

```json
{
  "hotkey": "ctrl+shift+alt+a",
  "capture_hotkey": "ctrl+shift+alt+c",
  "gemini": {
    "api_keys": ["YOUR_API_KEY_HERE"],
    "current_key_index": 0,
    "auto_rotate_on_quota_error": true,
    "model": "gemini-3-flash-preview",
    "system_prompt": "You are a helpful assistant. Just print the direct answer, no comments"
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

## Troubleshooting

### Build Fails

**Error**: `ModuleNotFoundError`
- **Solution**: Install missing module with `pip install <module>`

**Error**: `No module named 'google.genai'`
- **Solution**: Run `pip install google-genai`

### Executable Won't Run

**Issue**: Missing DLL errors
- **Solution**: Install Visual C++ Redistributable from Microsoft

**Issue**: Antivirus blocking
- **Solution**: Add exception for `AI_Assistant.exe`

**Issue**: Executable starts but doesn't respond
- **Solution**: Check `logs/ai_assistant.log` for errors
- Ensure `config.json` exists with valid API key

### Size Optimization

The default build creates a ~150-200MB executable due to all dependencies. To reduce size:

1. Use `--exclude-module` for unused packages
2. Use UPX compression (enabled by default)
3. Consider creating an installer instead of single-file exe

## Advanced Options

### Add Icon

1. Create/download an `.ico` file
2. Update `AI_Assistant.spec`:
   ```python
   icon='path/to/icon.ico'
   ```
3. Rebuild with `pyinstaller AI_Assistant.spec`

### Enable Console (for debugging)

In `AI_Assistant.spec`, change:
```python
console=True  # Shows console window with logs
```

### Multi-file Distribution

For faster startup, use `--onedir` instead of `--onefile`:
```batch
pyinstaller --onedir --windowed main.py
```

This creates a folder with multiple files instead of a single exe.

## Testing the Build

1. Navigate to `dist/`
2. Create `config.json` with your API key
3. Run `AI_Assistant.exe`
4. Check system tray for the icon
5. Test hotkeys and functionality

## Notes

- The `.exe` is portable - copy it anywhere
- First run creates default config if missing
- Logs are saved in `logs/` directory
- No installation required - just run the exe
- Windows Defender may scan on first run (normal)

## Support

If you encounter issues building:
1. Check Python version: `python --version`
2. Verify all requirements: `pip install -r requirements.txt`
3. Check build log in the console
4. Try rebuilding with `--debug` flag for more info
