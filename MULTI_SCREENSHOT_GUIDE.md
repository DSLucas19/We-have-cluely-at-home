# Multi-Screenshot Feature - Quick Guide

## Overview
You can now send **multiple screenshots** to Gemini at once! This is great for analyzing multi-page documents, comparing screens, or providing more context.

## Hotkeys

| Action | Default Hotkey | Description |
|--------|----------------|-------------|
| **Capture & Queue** | `Ctrl+Shift+Alt+C` | Takes a screenshot and adds it to the queue (silent) |
| **Analyze All** | `Ctrl+Shift+Alt+A` | Sends ALL queued images to Gemini. If queue is empty, takes single screenshot. |

## How to Use

1. **Queue Images**: 
   - Press `Ctrl+Shift+Alt+C` to capture your first screen.
   - Change your screen/scroll down.
   - Press `Ctrl+Shift+Alt+C` again for the next screen.
   - *Repeat as many times as needed.*

2. **Analyze**:
   - Press `Ctrl+Shift+Alt+A` (Main Hotkey).
   - The AI will receive ALL queued images + your system prompt.
   - The queue is automatically cleared after analysis.

## Configuration

You can customize the **Capture Queue Hotkey** in:
- **Settings Window**: Right-click tray icon -> Settings
- **config.json**: `"capture_hotkey": "your+hotkey"`

## Visual Feedback
- You'll see a notification for each queued image: *"Screenshot Queued (Total: X)"*
- The logs will show *"Attached X images to request"*

---

**🚀 Tip**: The AI interprets the images in the order you captured them.
