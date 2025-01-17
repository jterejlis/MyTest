import subprocess
from check_os import check_os

def check_bios_version():
    """
    Function to retrieve the BIOS version on the system.
    Works on both Windows and Unix-based systems.
    """
    try:
        if check_os() == 'Windows':  # Windows
            result = subprocess.run(
                ["wmic", "bios", "get", "smbiosbiosversion"],
                capture_output=True,
                text=True,
                check=True
            )
            lines = result.stdout.splitlines()
            bios_version = lines[1].strip() if len(lines) > 1 else "Unknown"
        elif check_os() == "MacOS":
            result = subprocess.run(
                ["ioreg", "-l"],
                capture_output=True,
                text=True,
                check=True
            )
            output = result.stdout
            for line in output.splitlines():
                if "bios-version" in line.lower():
                    return line.split("=")[-1].strip().strip('"')
            return "BIOS version not found"
        else:  # Unix-based systems
            result = subprocess.run(
                ["dmidecode", "-s", "bios-version"],
                capture_output=True,
                text=True,
                check=True
            )
            bios_version = result.stdout.strip()
        return bios_version
    except FileNotFoundError:
        return "Command not found. Ensure WMIC (Windows) or dmidecode (Linux) is installed."
    except Exception as e:
        return f"Error retrieving BIOS version: {e}"
