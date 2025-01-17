from sys import platform


def check_os():
    if platform == "linux2":
        return "Linux"
    elif platform in ("win32", "cygwin", "msys"):
        return "Windows"
    elif platform == "darwin":
        return "MacOS"
    elif platform == "os2":
        return 'OS/2'




