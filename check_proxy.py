import os
import winreg


def check_proxy_configuration_windows():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                        r"Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings") as key:
            proxy_enable, _ = winreg.QueryValueEx(key, "ProxyEnable")
            if proxy_enable:  # Sprawdź, czy proxy jest włączone
                proxy_server, _ = winreg.QueryValueEx(key, "ProxyServer")
                return f"Proxy Server: {proxy_server}"
            else:
                return "Proxy is disabled"

    except Exception as e:
        return f"Error retrieving proxy settings: {e}"



def check_proxy_configuration_unix():
    proxy_info = {
        "enabled": False,
        "address": None,
        "port": None
    }

    # Check environment variables for proxy settings
    http_proxy = os.environ.get('http_proxy') or os.environ.get('HTTP_PROXY')
    https_proxy = os.environ.get('https_proxy') or os.environ.get('HTTPS_PROXY')

    if http_proxy or https_proxy:
        proxy_info["enabled"] = True
        proxy_url = http_proxy or https_proxy  # Prefer HTTP proxy if available
        if "://" in proxy_url:
            proxy_url = proxy_url.split("://")[1]  # Remove the protocol (http:// or https://)

        if ":" in proxy_url:
            proxy_info["address"], proxy_info["port"] = proxy_url.split(":")
        else:
            proxy_info["address"] = proxy_url
            proxy_info["port"] = "80"  # Default port if not specified

    return proxy_info
