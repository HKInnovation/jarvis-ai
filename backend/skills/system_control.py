import os
import subprocess

def open_app(app_name):
    apps = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "chrome": "chrome.exe",
    "vscode": "code",
    "file explorer": "explorer.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
    "spotify": "spotify.exe",
    "paint": "mspaint.exe",
    "task manager": "taskmgr.exe",
    "settings": "ms-settings:",
    "camera": "microsoft.windows.camera:",
    }
    app_name = app_name.lower().strip()
    for key, cmd in apps.items():
        if key in app_name:
            try:
                subprocess.Popen(cmd, shell=True)
                return f"Opening {key}."
            except Exception:
                return f"I couldn't open {key}."
    return f"I don't know how to open {app_name} yet."

def shutdown_pc():
    os.system("shutdown /s /t 5")
    return "Shutting down in 5 seconds."

def set_volume(level):
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level / 100, None)
        return f"Volume set to {level} percent."
    except Exception:
        return "I couldn't change the volume."