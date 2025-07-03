import wmi
import time
from datetime import datetime
#from playsound import playsound
from scipy.io import wavfile
import sounddevice as sd
import numpy as np

#from winrt.windows.devices.enumeration import DeviceInformation, DeviceClass
import win32com.client
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

from windows_toasts import Toast, WindowsToaster

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
min_db = volume.GetVolumeRange()[0]
max_db = volume.GetVolumeRange()[1]
audio_file = "C:\\Users\\natal\\Documents\\ultimate_eye_rest\\slack_huddle_invite.wav"
modified_audio_file = "C:\\Users\\natal\\Documents\\ultimate_eye_rest\\modified_audio_temp.wav"
MAX_INT16 = 32767

audio_rate, audio = wavfile.read(audio_file)
import sys
print(sys.executable)

def send_notification(title, msg):
    toaster = WindowsToaster('Python')
    newToast = Toast()
    newToast.text_fields = [title, msg]
    toaster.show_toast(newToast)

'''def send_notification(title, message):
    log("toaster start")
    toaster = ToastNotifier()
    toaster.show_toast(title, message, duration=10)  # Duration in seconds'''

def get_system_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    is_muted = volume.GetMute()
    return volume.GetMasterVolumeLevelScalar() if not is_muted else 0

def volume_db_to_frac(vol):
    return (vol - min_db) / (max_db - min_db)

def volume_frac_to_db(vol):
    return int(vol * (max_db - min_db) + min_db)

def restart_log():
    log('restarting log')
    with open("C:\\Users\\natal\\Documents\\ultimate_eye_rest\\log.txt", 'w'):
        pass
    
def log(s):
    with open("C:\\Users\\natal\\Documents\\ultimate_eye_rest\\log.txt", 'a') as file:
        file.write(s+'\n')
    print(s)

def is_bluetooth_connected():
    """Check if any Bluetooth audio device is actively connected."""
    wmi = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    conn = wmi.ConnectServer(".", "root\\CIMV2")

    query = """
    SELECT * FROM Win32_PnPEntity 
    WHERE PNPClass='AudioEndpoint' AND Name LIKE '%Bluetooth%'
    """
    devices = conn.ExecQuery(query)
    
    for device in devices:
        print(f"Bluetooth audio device detected: {device.Name}")
        return True
    
    return False

def play_audio(audio_file):
    # Read the audio file (this example uses a .wav file)
    samplerate, data = wavfile.read(audio_file)
    
    # Play the audio using sounddevice
    sd.play(data, samplerate)
    sd.wait()  # Wait for the audio to finish playing

'''def play_audio_on_regular_speakers(audio_file):
    """Set default audio output to regular speakers and play audio."""
    # List audio devices
    devices = AudioUtilities.GetAllDevices()
    # Normally, you'd choose a specific device here, like "Speakers"
    for device in devices:
        print(f"Device found: {device.FriendlyName}")
    playsound(audio_file)'''


def play_volume(audio):
    volume = 0.46 if is_bluetooth_connected() else 0.1

    audio = audio * volume / get_system_volume()
    audio = np.clip(audio, -MAX_INT16-1, MAX_INT16).astype(np.int16)
    wavfile.write(modified_audio_file, audio_rate, audio)
    play_audio(modified_audio_file)

def is_monitor_on():
    try:
        c = wmi.WMI(namespace='root\\wmi')
        monitors = c.WmiMonitorBasicDisplayParams()
    except Exception as e:
        log(f"Error: {e}")
        return False
    
    awake = False
    for monitor in monitors:
        if monitor.Active:
            awake = True
    return awake

def notify_eye_break(state):
    if state == "start":
        notification_str = "Look away 20 ft"
    else:
        notification_str = "Done looking"
    if get_system_volume() > 0:
        play_volume(audio)
        notification_str += '\n\nVolume is off'
    send_notification("20 20 20", notification_str)

if __name__ == "__main__":
    awake = True
    day = datetime.now().day
    i = 0
    restart_log()
    while True:
        if day != datetime.now().day:
            restart_log()
            day = datetime.now().day
            awake = True
            i = 0

        if is_monitor_on():
            awake = True
            log('monitor is on') 
            
            if get_system_volume() > 0:
                log('volume is on')
            else:
                log('volume is off')

            log(str(datetime.now())+'\n')

        while is_monitor_on() and day == datetime.now().day:
            for i in range(17):
                log('mins '+str(i))
                time.sleep(60)
                if not is_monitor_on():
                    break
            log('mins'+str(i+1))

            try:
                notify_eye_break("start")
                time.sleep(21)
                notify_eye_break("stop")
            except Exception as e:
                log(str(e))
                raise e
            
        if not is_monitor_on():
            if awake:
                log('monitor is off')
                log(str(datetime.now())+'\n')
            elif (i + 1) % (6 * 60) == 0:
                log(".")

            awake = False
            i += 1
            time.sleep(10)

