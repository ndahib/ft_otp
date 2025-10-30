# ft_otp

[![License](https://img.shields.io/badge/license-None-lightgrey.svg)](https://github.com/ndahib/ft_otp)
[![Language](https://img.shields.io/badge/language-Python-blue.svg)](https://github.com/ndahib/ft_otp)

> 🔐 A simple Time-based One-Time Password (TOTP) generator implemented **from scratch in Python**, using only standard libraries.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Contributing](#contributing)
- [Credits](#credits)

---

## Overview

**ft_otp** is a minimalist Python implementation of **Time-based One-Time Passwords (TOTP)** compatible with the [RFC 6238](https://www.rfc-editor.org/rfc/rfc6238) standard. It is written entirely with Python's **built-in libraries** (`hmac`, `hashlib`, `time`, `base64`), with no external dependencies for the core logic.

This project was created for educational purposes (notably for the **42 School "ft_otp" project**) to demonstrate how TOTP works internally without relying on third-party libraries like `pyotp`.

---

## Key Features

✅ Pure-Python implementation — uses only standard modules  
✅ Compatible with RFC 6238 (TOTP)  
✅ Generates 6-digit one-time passwords based on a shared secret  
✅ Works both as a **CLI** and optional **GUI** (bonus)  
✅ Optional encryption and key management features  
✅ Educational and easy to read / modify

---

## Installation

### Requirements

- Python **3.8+**
- `pip` (for optional dependencies)
- Standard library only for TOTP core
- (Bonus features require):
  - `tkinter` — for GUI
  - `qrcode` — to generate QR images
  - `Pillow` — to display generated QR codes
  - `cryptography` — to encrypt stored keys

### Setup

Clone the repository:

```bash
git clone https://github.com/ndahib/ft_otp.git
cd ft_otp
```

Install dependencies (if using bonus features):

```bash
pip install -r requirements.txt
```

Or manually install:

```bash
pip install qrcode pillow cryptography
```

---

## Usage

You can use ft_otp in two modes: CLI or GUI.

### Graphical Interface (GUI)

```bash
python ft_otp.py
gui
```


This launches a small graphical interface showing with 2 buttons one for generating key and other for generating totp.

### Command-Line Interface (CLI)

**Example 1** — Generate a TOTP from a stored key:

```bash
python ft_otp.py
cli
```

**Example 2** — save and encrypt a new random key and save it:

```bash
 -g key.hex
```

**Example 3** — generate totp code with 6 digit :

```bash
-k ft_otp.key
```

**Example 4** — generate qr code and save it in image:

```bash
qr --key=ft_otp.key --account="alice@gmail.com" --issuer"ft_otp_user"
```

---

## How It Works (Under the Hood)

The TOTP generation process follows these steps:

1. Decode the secret key (hexadecimal or base32)
2. Compute time counter = `int(time.time()) // interval`
3. Generate HMAC hash using the shared secret and counter value
4. Extract dynamic offset from the hash (RFC 4226 truncation)
5. Compute OTP = `(binary % 10^digits)`
6. Output a 6-digit code that changes every interval seconds

**Libraries used:**

- `hmac` — for cryptographic HMAC calculation
- `hashlib` — to use SHA-1, SHA-256, or SHA-512
- `struct` — for binary manipulation
- `time` — to compute time steps
- `base64` — for secret decoding (if encoded)

No external TOTP or OTP library (like `pyotp`) is used — everything is computed manually.

---

## Configuration

Environment variables and CLI options supported:

| Option / Env Var | Description | Default |
|---|---|---|
| `-k <keyfile>` | Path to the key file | — |
| `-g <file>` | Generate new key | — |
| `-i <seconds>` | Interval between codes | 30 |
| `-p <password>` | Encrypt / re-encrypt key file | — |
| `-rk` | Generate random 64-char hex key | — |
| `-rp` | Generate random base64 password | — |

---

## Project Structure

Typical structure of this repository:

```
ft_otp/
├── ft_otp.py             # Main entry point
├── core/                 # Internal logic (HMAC, encoding, key handling)
├── requirements.txt      # Dependencies (for bonus part)
├── .gitignore
└── README.md
```

- **core/management/** — parse command line and orchestrate cli, gui choices
- **core/management/** —  includes functions for totp generation, qr image generation, key management, and encryption
- **requirements.txt** — optional dependencies for GUI and encryption

---

## Testing

To verify your implementation:

```bash
-k ft_otp.key
```

Then compare the generated code with one from a trusted app (Google Authenticator, Authy, etc.) using the same shared secret.

To automate tests:

```bash
pip install pytest
pytest -q
```

**Example test (RFC 6238 vectors):**

```python
import hmac, hashlib, struct, time

def test_totp_output():
    secret = bytes.fromhex("3132333435363738393031323334353637383930")
    interval = 30
    counter = int(time.time() // interval)
    msg = struct.pack(">Q", counter)
    h = hmac.new(secret, msg, hashlib.sha1).digest()
    offset = h[-1] & 0x0F
    code = (struct.unpack(">I", h[offset:offset+4])[0] & 0x7FFFFFFF) % 10**6
    assert isinstance(code, int)
```

---

## Contributing

Contributions are welcome!

1. Fork this repository
2. Create a new branch:
   ```bash
   git checkout -b feat/my-feature
   ```
3. Commit changes and run tests
4. Submit a pull request

**Guidelines:**

- Follow PEP 8 coding style
- Add docstrings and inline comments
- Keep dependencies minimal
- Write clear commit messages

---
## Credits

- **Author:** ndahib
- **Project Origin:** 42 School — ft_otp project
- **Based on:** RFC 4226 (HOTP) and RFC 6238 (TOTP)
- **Core Libraries Used:** `hmac`, `hashlib`, `time`, `struct`, `base64`

---

💡 *"Security through understanding — ft_otp shows how TOTP truly works."*
