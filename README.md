## Wi‑Fi security audit

> **Important — read before using**
>
> This script automates capturing WPA/WPA2 handshakes and converting them for offline cracking with Hashcat. **Do not use this tool against networks you do not own or for which you do not have explicit authorization.** Unauthorized interception or access to network traffic is illegal. Use this script only for legitimate security testing (your own networks or lab environments) or with a signed authorization.
> 

This Python script orchestrates wireless auditing tools (**aircrack-ng** suite, **hcxpcapngtool**, **hashcat**) to perform WPA/WPA2 handshake capture, conversion, and offline cracking. It provides a structured workflow with logging and automated steps for security assessments:

* Weak Wi‑Fi passwords remain a common risk.
* Demonstrating handshake capture shows how attackers exploit them.
* Running such audits highlights the need for strong passphrases, WPA3 adoption, and regular testing.

### Features

* Enable and restore monitor mode automatically.
* Scan and capture WPA/WPA2 handshakes.
* Extract client MACs from CSV output.
* Optionally send deauth frames to trigger handshakes.
* Verify captures with `aircrack-ng`.
* Convert to `.hc22000` format for Hashcat.
* Run offline cracking attempts with a wordlist.
* Log all actions to `log.txt`.

### Requirements

* Python 3.6+
* `aircrack-ng`
* `hashcat`
* `hcxpcapngtool`

The script checks for these tools at start.

### Installation (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y aircrack-ng hashcat
# For hcxpcapngtool:
# git clone https://github.com/ZerBea/hcxtools.git && cd hcxtools && make && sudo make install
```

Root privileges are required.

### Usage

* Check dependencies.
* Switch interface to monitor mode.
* Scan and choose target.
* Capture traffic for chosen BSSID/channel.
* Optionally deauth clients to force handshake.
* Verify handshake presence.
* Convert to `.hc22000` and run Hashcat with wordlist.
* Restore interface to managed mode.

For safer, passive use:

* Capture traffic only.
* Skip deauth and cracking.
* Convert for analysis or validation.

Actions and results are written to `log.txt` with timestamps.

### Safety, legal & ethical notes

* Only audit authorized networks.
* Deauth attacks disrupt clients; use carefully.
* Keep proof of authorization when testing.
