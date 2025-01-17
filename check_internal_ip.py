import psutil
import socket
import os
import subprocess

def check_ipv4_configuration_unix():
    result = []

    # Iterate through network interfaces
    for interface, addrs in psutil.net_if_addrs().items():
        connection_info = {}
        connection_info['interface'] = interface

        # Determine if it's WiFi or Ethernet
        if "wlan" in interface or "Wi-Fi" in interface or "wlp" in interface:
            connection_info['type'] = "WiFi"
        elif "eth" in interface or "enp" in interface:
            connection_info['type'] = "Ethernet"
        else:
            connection_info['type'] = "Unknown"

        # Check IPv4 address
        for addr in addrs:
            if addr.family == socket.AF_INET:
                connection_info['ipv4'] = addr.address

                # Check if IP is static or dynamic
                dhcp_command = f'nmcli device show {interface} | grep IP4.DHCP4.GATEWAY'
                dhcp_output = os.popen(dhcp_command).read().strip()
                if dhcp_output:
                    connection_info['assignment'] = "Dynamic (DHCP)"
                else:
                    connection_info['assignment'] = "Static"

        if 'ipv4' in connection_info:
            result.append(connection_info)

    return result


def check_ipv4_configuration_windows():
    result = []

    for interface, addrs in psutil.net_if_addrs().items():
        connection_info = {}
        connection_info['interface'] = interface

        # Determine if it's WiFi or Ethernet
        if "Wi-Fi" in interface or "wlan" in interface:
            connection_info['type'] = "WiFi"
        elif "Ethernet" in interface or "eth" in interface:
            connection_info['type'] = "Ethernet"
        else:
            connection_info['type'] = "Unknown"

        # Check IPv4 address
        for addr in addrs:
            if addr.family == socket.AF_INET:
                connection_info['ipv4'] = addr.address

                # Check if IP is static or dynamic
                try:
                    output = subprocess.check_output(
                        f'netsh interface ip show config name="{interface}"',
                        shell=True,
                        text=True,
                        stderr=subprocess.DEVNULL
                    )
                    if "DHCP enabled: Yes" in output:
                        connection_info['assignment'] = "Dynamic (DHCP)"
                    else:
                        connection_info['assignment'] = "Static"
                except subprocess.CalledProcessError:
                    connection_info['assignment'] = "Unknown"

        if 'ipv4' in connection_info:
            result.append(connection_info)

    return result


def check_ipv4_configuration_macOS():
    ports_result = subprocess.run(
        ["networksetup", "-listallhardwareports"],
        capture_output=True,
        text=True,
        check=True
    )
    ports_output = ports_result.stdout.strip()
    interfaces = {}
    current_interface = None

    # Parse the output to map hardware ports to devices
    for line in ports_output.splitlines():
        if "Hardware Port" in line:
            current_interface = line.split(":")[1].strip()
        if "Device" in line and current_interface:
            device = line.split(":")[1].strip()
            interfaces[current_interface] = device

    # Check the status of each interface
    for interface, device in interfaces.items():
        ip_result = subprocess.run(
            ["ipconfig", "getifaddr", device],
            capture_output=True,
            text=True
        )
        ip = ip_result.stdout.strip()

        if ip:  # If IP exists, determine configuration
            dhcp_server_result = subprocess.run(
                ["ipconfig", "getoption", device, "dhcp_server_identifier"],
                capture_output=True,
                text=True
            )
            dhcp_lease_result = subprocess.run(
                ["ipconfig", "getoption", device, "lease_time"],
                capture_output=True,
                text=True
            )
            is_dhcp = dhcp_server_result.stdout.strip() or dhcp_lease_result.stdout.strip()
            dhcp_status = "Dynamic (DHCP)" if is_dhcp else "Static"
            return f"Interface: {interface}\nIP Address: {ip}\nConfiguration: {dhcp_status}"

    return "No active network interfaces found."

