# Ultimate Eye Rest - 20-20-20 Rule Reminder

A Windows application that implements the **20-20-20 rule** for eye health: every 20 minutes, look at something 20 feet away for 20 seconds to reduce eye strain.

## Features

- **Smart Notifications**: Windows Toast notifications remind you to take eye breaks
- **Audio Alerts**: Optional audio notification with intelligent volume control
- **Monitor Detection**: Only triggers reminders when your monitor is active
- **Session Logging**: Tracks eye breaks and system state throughout the day
- **Multiple Implementations**: Available as Python script, Windows batch file, or VBS script

## Requirements

### Dependencies
- Python 3.8+
- `wmi` - Windows Management Instrumentation
- `scipy` - Audio file handling
- `sounddevice` - Audio playback
- `windows-toasts` - Windows notifications
- `pycaw` - Windows audio control
- `comtypes` - COM interface support
- `pywin32` - Windows COM scripting

### Installation

```bash
pip install wmi scipy sounddevice windows-toasts pycaw comtypes pywin32
```

## Usage

### Python Script
```bash
python 20_20_20.py
```

### Windows Batch File
```bash
20_20_20.bat
```

### VBScript (for Windows Task Scheduler automation)
```bash
cscript 20_20_20.vbs
```

## How It Works

1. **Startup Check**: Verifies if another instance is already running by checking the log file timestamp
   - If a log file is locked, exits immediately to prevent duplicates
   - This allows safe periodic scheduling (e.g., every 15 minutes via Task Scheduler)
2. **Initialization**: Loads audio file and initializes system audio interface
3. **Monitor Check**: Continuously monitors if your display is active
4. **Eye Break Timer**: When 20 minutes elapse with monitor on, triggers reminder
5. **Notification**: Sends Windows Toast notification: "Look away 20 ft"
6. **Audio Alert**: Plays Slack huddle sound (optional, respects system mute state)
7. **Daily Reset**: Log resets at midnight each day

## Files

- `20_20_20.py` - Main Python implementation
- `20_20_20.bat` - Windows batch wrapper
- `20_20_20.vbs` - VBScript for Task Scheduler integration
- `slack_huddle_invite.wav` - Audio notification file
- `log.txt` - Daily activity log

## Configuration

Audio notification files can be replaced with custom `.wav` files. Update the path in the script:
```python
audio_file = "C:\\path\\to\\your\\notification.wav"
```

### Windows Task Scheduler Setup

For automatic startup on login or screen events, configure Windows Task Scheduler:

1. Open Task Scheduler (`taskschd.msc`)
2. Create a new basic task:
   - **Name**: "Ultimate Eye Rest"
   - **Trigger**: Choose one or more:
     - "At log on" (runs when you log in)
     - "On workstation unlock" (runs when screen is unlocked)
     - "On a schedule" set to every 15 minutes
   - **Action**: Start a program
     - Program: `python.exe` or `C:\path\to\python.exe`
     - Arguments: `C:\path\to\20_20_20.py`
     - Start in: `C:\Users\<YourUsername>\Documents\ultimate_eye_rest`
3. **Important**: In "Advanced Settings", check:
   - ✓ "Run with highest privileges" (if needed for audio control)
   - ✓ "Run whether user is logged in or not" (optional, for background operation)

**Why 15 minutes?** The script exits if already running (checks log from last 18 minutes). Scheduling every 15 minutes ensures it will pick up eye break monitoring even after screen lock, sleep, or wake events without creating duplicates.

## Use Cases

- **Remote workers**: Maintain eye health during long screen time
- **Students**: Break up study sessions automatically
- **Office workers**: Reduce digital eye strain throughout the day
- **Developers**: Non-intrusive background reminders

## Logging

The application logs all activity to `log.txt` in the project directory:
- Monitor on/off events
- Volume state
- Audio device status

Logs reset daily at midnight.

## Notes

- Application runs in the background; no UI required
- **Duplicate Prevention**: Script automatically exits if another instance is running (within last 18 minutes), making it safe to trigger frequently via Task Scheduler
- Best used with Windows Task Scheduler set to run every 15 minutes on login, unlock, and on schedule
- Respects system mute and volume settings
- Pause reminders by turning off monitor or muting system audio
- Log file (`log.txt`) shows when instances attempted to run—check it if eye break reminders aren't appearing

## Troubleshooting

- **No reminders appearing?** Check `log.txt` to see if the script is running. If the last entry is an exit message, another instance may still be active.
- **Task Scheduler not triggering?** Ensure Python path is correct and use absolute paths. Test manually first: `python C:\path\to\20_20_20.py`
- **Audio not playing?** Verify `slack_huddle_invite.wav` exists and volume is not muted system-wide.
