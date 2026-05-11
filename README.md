# navi
A minimalist, socket-based reconnaissance toolkit inspired by Serial Experiments Lain. Built for the Wired, it features advanced port pulsing, ghost DNS mapping, and anti-spoofing logic. "No matter where you are, everyone is always connected." 🌐 Purist Python, zero heavy dependencies. #Cybersecurity #Lain

# 🌐 Navi OS - Protocol: LAIN

[![License: MIT](https://img.shields.io/badge/License-MIT-magenta.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.13+](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/)

> "No matter where you are, everyone is always connected."

**Navi OS** is a minimalist, high-performance reconnaissance toolkit built for the Wired. Unlike bloated scanners, Navi operates directly on the socket layer, using purist Python to map digital identities, bypass firewall deceptions, and interrogate remote pulses.

---

## ⚡ Core Features

### 📡 Pulse Interrogation (`pulse.py`)
Advanced port scanning engine with built-in **Maze Detection**.
- **Active Handshaking:** Uses 8+ specific payloads to force "silent" services to reveal their identity.
- **Ghost Port Filtering:** Automatically detects and ignores *Port Spoofing* and *Honey-pots* (TAR PITs).
- **Latency Buffering:** Calibrated for international targets and Tor exit nodes.

### 🔍 Fingerprinting & Vulnerability Leak (`fingerprint.py`)
- **Banner Analysis:** Precise identification of software versions (Nginx, SSH, Apache, etc.).
- **Wired Leaks:** Cross-references detected versions with known exploit impacts (Integer Overflows, Sandbox Escapes).

### 🕸️ Ghost DNS & Recursive Diving (`ghost_dns.py` / `recursion.py`)
- **Subdomain Discovery:** Maps the hidden infrastructure of a target.
- **Deep Recursion:** Automatically pivots through discovered sub-identities to find forgotten entry points.

### 🛡️ Cloaking & Stealth
- **Tor Integration:** Native support for SOCKS5 proxies to mask your exit point in the Wired.
- **Phantom Headers:** Custom HTTP probing to bypass basic WAF filters.

---

## 🚀 Installation

1. **Clone the consciousness:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/navi-lain.git](https://github.com/YOUR_USERNAME/navi-lain.git)
   cd navi-lain

```

2. **Prepare the environment:**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```



---

## 🛠️ Usage

Simply initialize the main protocol:

```bash
python lain.py

```

Follow the glitch-styled prompts to enter your target. For a full spectrum scan, ensure you are synchronized with the Wired.

---

## 📂 Project Structure

* `/modules`: The core logic (Pulse, DNS, SMB, SSL, OSINT).
* `/style`: ANSI glitch effects and ASCII banners.
* `/wordlists`: Active handshakes and DNS dictionary.
* `/data`: Persistent knowledge base for target tracking.

---

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## ⚠️ Disclaimer

*Navi OS is a tool for educational purposes and authorized security auditing only. Remember: in the Wired, every action leaves a trace. Use it wisely.*

**"Present day, present time. Hahaha!"**
