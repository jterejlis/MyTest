import platform
import os
import psutil
from check_os import check_os

def check_system_info():
    system_info = {
        "os": check_os(),
        "version": platform.version(),
        "release": platform.release(),
        "architecture": platform.architecture()[0],
        "cpu_cores": os.cpu_count(),
        "memory": round(psutil.virtual_memory().total / (1024 ** 3), 2)  # in GB
    }
    return system_info

print(check_system_info())