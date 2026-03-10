# 🛡️ PriVi-Elite V3: Advanced SSH Auditor
**APT-Simulated Credential Auditor & Post-Exploitation Tool | PriViSecurity**



PriVi-Elite V3 is a high-sophistication SSH security auditor designed for professional penetration testing and forensic education. It mimics Advanced Persistent Threat (APT) behaviors through stealth mechanics and automated persistence.

## 💎 Elite Features
* **Interactive Launcher:** Configure targets and intensity profiles without editing code.
* **Intelligent Modes:**
    * **Aggressive:** Multi-threaded dictionary attack for rapid results.
    * **Stealth:** Implements random jitter (delays) to evade IDPS and SOC alerting.
    * **Forensic:** Passive banner grabbing to identify SSH service versions.
* **Post-Exploitation Engine:** Automatically injects an SSH Public Key into the target's `authorized_keys` for permanent backdoor access.
* **SOC Dashboard:** Real-time log stream and progress visualization powered by the `Rich` library.



## 🚀 Installation & Usage
1. **Clone/Download** the repository.
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt


# PriVi-Elite-V3-SSH-Auditor
Advanced APT-simulated SSH auditor for forensic research. Features multi-threaded dictionary attacks, stealth jitter to bypass SOC detection, and automated key-injection persistence. Built for the PriViSecurity Lab.
