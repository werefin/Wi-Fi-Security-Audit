## Wi‑Fi security audit

> **Important — read before using**
>
> This script automates capturing WPA/WPA2 handshakes and converting them for offline cracking with Hashcat. **Do not use this tool against networks you do not own or for which you do not have explicit authorization.** Unauthorized interception or access to network traffic is illegal in many jurisdictions. Use this script only for legitimate security testing (your own networks or lab environments) or with a signed authorization.
> 

This Python script orchestrates wireless auditing tools (aircrack-ng suite, hcxpcapngtool, hashcat) to perform WPA/WPA2 handshake capture, conversion, and offline cracking. It provides a structured workflow with logging and automated steps for security assessments.

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

### Installation

```bash
sudo apt update
sudo apt install -y  aircrack-ng hashcat
# For hcxpcapngtool:
# git clone https://github.com/ZerBea/hcxtools.git && cd hcxtools && make && sudo make install
```

Root privileges are required.

## Usage

Workflow:

1. Check dependencies.
2. Switch interface to monitor mode.
3. Scan and choose target.
4. Capture traffic for chosen BSSID/channel.
5. Optionally deauth clients to force handshake.
6. Verify handshake presence.
7. Convert to `.hc22000` and run Hashcat with wordlist.
8. Restore interface to managed mode.

## Defensive / Capture‑Only Mode

For safer, passive use:

* Capture traffic only.
* Skip deauth and cracking.
* Convert for analysis or validation.

## Files produced

* `log.txt`
* `capture-01.cap` / `capture-01.csv`
* `capture.hc22000`

## Logging and Output

Actions and results are written to `log.txt` with timestamps.

## Troubleshooting & Notes

* Ensure tools are installed and in `PATH`.
* Run with `sudo` if permissions fail.
* Network services may need manual restart.
* No handshake? Allow more time or ensure client activity.
* Hashcat may need driver support.

## Improvements & Contributions

Ideas:

* Add non‑interactive CLI flags.
* Implement `--capture-only` mode.
* Improve CSV parsing.
* Enhance logging format.

## Changelog

* **2025-09-21** — Simplified README; added concise “Why this matters” section.

## Safety, Legal & Ethical Notes

* Only audit authorized networks.
* Deauth attacks disrupt clients; use carefully.
* Keep proof of authorization when testing.

---

*Last updated: `2025-09-21`*
