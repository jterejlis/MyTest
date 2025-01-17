import sys
import argparse
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QTextEdit
from check_os import check_os
from check_hostname import check_hostname
from check_external_IP import check_external_IP
from check_internal_ip import check_ipv4_configuration_unix, check_ipv4_configuration_windows, check_ipv4_configuration_macOS
from check_proxy import check_proxy_configuration_windows, check_proxy_configuration_unix
from check_bios import check_bios_version
from check_systeminfo import check_system_info


class InfoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Info")

        # Layout
        layout = QVBoxLayout()

        # Text box for output
        self.text_box = QTextEdit()
        self.text_box.setReadOnly(True)
        layout.addWidget(self.text_box)

        # Buttons
        btn_hostname = QPushButton("Get Hostname")
        btn_hostname.clicked.connect(self.display_hostname)
        layout.addWidget(btn_hostname)

        btn_ip = QPushButton("Get IP Address")
        btn_ip.clicked.connect(self.display_ip)
        layout.addWidget(btn_ip)

        btn_proxy = QPushButton("Get Proxy Configuration")
        btn_proxy.clicked.connect(self.display_proxy)
        layout.addWidget(btn_proxy)

        btn_bios = QPushButton("Get BIOS Version")
        btn_bios.clicked.connect(self.display_bios)
        layout.addWidget(btn_bios)

        btn_system = QPushButton("Get System Information")
        btn_system.clicked.connect(self.display_system_info)
        layout.addWidget(btn_system)

        self.setLayout(layout)

    def display_hostname(self):
        self.text_box.setText(check_hostname())

    def display_ip(self):
        if check_os() == "Windows":
            self.text_box.setText(
                "External IP:" + check_external_IP() + "\n" + "InternalIP:" + str(check_ipv4_configuration_windows()))
        elif check_os() == "Linux":
            self.text_box.setText(
                "External IP:" + check_external_IP() + "\n" + "InternalIP:" + str(check_ipv4_configuration_unix()))
        elif check_os() == "MacOS":
            self.text_box.setText(
                "External IP:" + check_external_IP() + "\n" + "InternalIP:" + str(check_ipv4_configuration_macOS()))

    def display_proxy(self):
        if check_os() == "Windows":
            self.text_box.setText(str(check_proxy_configuration_windows()))
        elif check_os() == "Linux" or "MacOS":
            self.text_box.setText(str(check_proxy_configuration_unix()))

    def display_bios(self):
        self.text_box.setText(check_bios_version())

    def display_system_info(self):
        self.text_box.setText(str(check_system_info()))

parser = argparse.ArgumentParser(description="System Information Tool")
parser.add_argument("--hostname", action="store_true", help="Get the hostname")
parser.add_argument("--ip", action="store_true", help="Get the IP address")
parser.add_argument("--proxy", action="store_true", help="Get proxy settings")
parser.add_argument("--bios", action="store_true", help="Get BIOS version")
parser.add_argument("--system", action="store_true", help="Get system information")

args = parser.parse_args()

if args.hostname:
        print("Hostname:")
        print(check_hostname())


if args.ip:
    print("IP Address:")
    if check_os() == "Windows":
        print(
            "External IP:" + check_external_IP() + "\n" + "InternalIP:" + str(check_ipv4_configuration_windows()))
    elif check_os() == "Linux":
        print(
            "External IP:" + check_external_IP() + "\n" + "InternalIP:" + str(check_ipv4_configuration_unix()))
    elif check_os() == "MacOS":
       print(
        "External IP:" + check_external_IP() + "\n" + "InternalIP:" + str(check_ipv4_configuration_macOS()))


if args.proxy:
    print("Proxy Configuration:")
    if check_os() == "Windows":
        print(str(check_proxy_configuration_windows()))
    elif check_os() == "Linux" or "MacOS":
        print(str(check_proxy_configuration_unix()))


    if args.bios:
        print("BIOS Version:")
        print(check_bios_version())


    if args.system:
        print("System Information:")
        print(str(check_system_info()))

    # Jeśli brak argumentów, wyświetl pomoc
    if not any(vars(args).values()):
        parser.print_help()

app = QApplication([])
window = InfoApp()
window.show()
app.exec()

