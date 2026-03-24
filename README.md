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

1. **Initialization**: Loads audio file and initializes system audio interface
2. **Monitor Check**: Continuously monitors if your display is active
3. **Eye Break Timer**: When 20 minutes elapse with monitor on, triggers reminder
4. **Notification**: Sends Windows Toast notification: "Look away 20 ft"
5. **Audio Alert**: Plays Slack huddle sound (optional, respects system mute state)
6. **Volume Adaptation**: Adjusts notification volume based on system volume and Bluetooth connection
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
- Best used with Windows Task Scheduler for automatic startup
- Respects system mute and volume settings
- Pause reminders by turning off monitor or muting system audio
