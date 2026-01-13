# API Key Rotation Feature - Quick Guide

## Overview
The AI Assistant now supports **multiple API keys** with **automatic rotation** when one key hits quota limits.

## Adding Multiple API Keys

### Via Settings UI
1. Run `python main.py`
2. Right-click system tray icon → **Settings**
3. Click **Add Key** button
4. Enter your API key
5. Repeat for each key you want to add
6. Click **Save**

### Via config.json
Edit `config.json` directly:
```json
{
  "gemini": {
    "api_keys": [
      "AIzaSy...key1",
      "AIzaSy...key2",
      "AIzaSy...key3"
    ],
    "current_key_index": 0,
    "auto_rotate_on_quota_error": true
  }
}
```

## How It Works

1. **Normal Operation**: Uses the current active key (index: 0 by default)
2. **Quota Error Detected**: When a request fails due to quota/rate limits
3. **Automatic Rotation**: Switches to the next key in the list
4. **Retry**: Retries the request with the new key
5. **Cycles Through**: If all keys fail, returns error

## Features

✅ **Automatic Detection**: Recognizes quota errors automatically  
✅ **Seamless Switching**: No interruption to your workflow  
✅ **Unlimited Keys**: Add as many API keys as you need  
✅ **Smart Retry**: Only retries once per key to avoid loops  
✅ **Toggle On/Off**: Can disable auto-rotation in settings  

## Configuration Options

| Setting | Description | Default |
|---------|-------------|---------|
| `api_keys` | Array of API keys | `[]` |
| `current_key_index` | Index of current active key | `0` |
| `auto_rotate_on_quota_error` | Enable/disable rotation | `true` |

## Managing Keys

### Add a Key
Settings → Click "Add Key" → Enter API key → Save

### Remove a Key
Settings → Select key in list → Click "Remove" → Save

### Test a Key
Settings → Select key in list → Click "Test"

## Quota Error Examples

The system detects these error types:
- `429 Too Many Requests`
- `quota exceeded`
- `rate limit`
- `resource exhausted`

## Best Practices

1. **Multiple Free Keys**: Create multiple free Gmail accounts for more quota
2. **Monitor Usage**: Check [AI Studio](https://aistudio.google.com/) for quota status
3. **Test Keys**: Use the "Test" button to verify keys work
4. **Keep Backups**: Save keys securely outside the app

## Example Workflow

```
Request 1 → Key #1 → Success ✅
Request 2 → Key #1 → Success ✅
Request 3 → Key #1 → Quota Error ❌
  ↓ Auto-rotate
Request 3 (retry) → Key #2 → Success ✅
Request 4 → Key #2 → Success ✅
```

## Logs

Check `logs/ai_assistant.log` to see rotation events:
```
WARNING - Quota error detected: 429 Too Many Requests
INFO - Successfully rotated to next API key (index: 1)
INFO - Retrying with rotated API key...
```

---

**🎉 Never worry about quota limits again!**
