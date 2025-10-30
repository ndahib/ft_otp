# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    __init__.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ndahib <ndahib@student.1337.ma>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/10/29 14:11:25 by ndahib            #+#    #+#              #
#    Updated: 2025/10/29 14:11:25 by ndahib           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from ..constants import STEP, START_TIME, OUTPUT_DIGITS
import struct
import hmac
import hashlib
import time
from math import floor
import qrcode
import tkinter as tk
import os
from tkinter import messagebox
from ..constants import color
from PIL import ImageTk
from qrcode.image.pil import PilImage
from cryptography.fernet import Fernet
import sys
import base64


class FtOtp:
    def __init__(self):
        if os.path.isfile("ft_otp_encryption.key"):
            with open("ft_otp_encryption.key", "rb") as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open("ft_otp_encryption.key", "wb") as f:
                f.write(self.key)
        self.cipher_suite = Fernet(self.key)

    def encrypte_save_key(self, key):
        if os.path.isfile(key):
            with open(key, "r", encoding="utf-16") as f:
                key_hex = f.read().strip()
        else:
            key_hex = key
        try:
            key_hex = self.cipher_suite.encrypt(bytes.fromhex(key_hex))
            with open("ft_otp.key", "wb") as f:
                f.write(key_hex)

            print(f"{color.OKGREEN}Key was successfully saved in ft_otp.key. {color.ENDC}")
        except ValueError:
            print(f"{color.FAIL}{sys.argv[0]}: error: key must be 64 hexadecimal characters.. {color.ENDC}")

    def generate_hex(self):
        """
        Generate a random hexadecimal string of 32 bytes.
        """

        return os.urandom(32).hex()

    def _dynamic_truncate(self, hmac_digest: bytes) -> int:
        """
        Apply RFC dynamic truncation: use low nibble of last byte as offset,
        take 4 bytes from offset, mask MSB to get 31-bit integer.
        """
        offset = hmac_digest[-1] & 0x0F
        four = hmac_digest[offset : offset + 4]
        code_int = struct.unpack(">I", four)[0] & 0x7FFFFFFF
        return code_int

    def _read_shared_key_from_file(self):
        """
        Read the shared key from the file ft_otp.key.

        """
        with open("ft_otp.key", "rb") as f:
            return f.read().strip()

    def _decrypt_shared_key(self):
        """
        Decrypt the shared key from the file ft_otp.key.

        """
        encripted_shared_key = self._read_shared_key_from_file()
        try:
            return self.cipher_suite.decrypt(encripted_shared_key)
        except Exception as e:
            print(f"{color.FAIL}{sys.argv[0]}: error decryopting key: {e} {color.ENDC}")

    def totp(self):
        """
        Compute a TOTP code for the given shared key hexadecimal string.

        TOTP = Truncate(HMAC(secret, floor(currentTime / timestep))) % 10^digits.
        """

        key_bytes = self._decrypt_shared_key()
        if key_bytes is None or len(key_bytes) != 32:
            raise ValueError("Invalid key")

        T = int(time.time() / STEP)

        hmac_digest = hmac.new(key_bytes, struct.pack(">Q", T), hashlib.sha1).digest()

        code_int = self._dynamic_truncate(hmac_digest)
        otp = code_int % (10**OUTPUT_DIGITS)
        return str(otp).zfill(OUTPUT_DIGITS)

    def generate_qr_code(self, key_file, account="user@example.com", issuer="ft_otp", qr_file="ft_otp_qr.png"):
        """
        Generate a QR code containing the decrypted TOTP key for Google Authenticator.
        key_file: path to the encrypted key file (e.g. "ft_otp.key")
        """
        try:

            with open(key_file, "rb") as f:
                encrypted_key = f.read().strip()

            decrypted_key_bytes = self.cipher_suite.decrypt(encrypted_key)
            secret_b32 = base64.b32encode(decrypted_key_bytes).decode("utf-8").replace("=", "")

        except Exception as e:
            print(f"{color.FAIL}{sys.argv[0]}: error decrypting key: {e}{color.ENDC}")
            return None

        uri = (
            f"otpauth://totp/{issuer}:{account}"
            f"?secret={secret_b32}"
            f"&issuer={issuer}"
            f"&algorithm=SHA1"
            f"&digits={OUTPUT_DIGITS}"
            f"&period={STEP}"
        )

        qr = qrcode.QRCode(version=1, box_size=10, border=4, image_factory=PilImage)
        qr.add_data(uri)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qr_file)

        return img


class FtOtpGraphicalInterface:
    def __init__(self, ft_otp: FtOtp):
        self.ft_otp = ft_otp
        self.root = tk.Tk()
        self.root.title("ft_otp — HOTP Generator")
        self.root.geometry("500x550")
        self.root.resizable(False, False)

        tk.Label(self.root, text="ft_otp HOTP Generator", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Button(self.root, text="Generate New Key", command=self._generate_key, bg="#2e74de", fg="white", width=20).pack(pady=10)
        tk.Button(self.root, text="Generate OTP", command=self._generate_otp, bg="#1a7942", fg="white", width=20).pack(pady=10)

        self.otp_label = tk.Label(self.root, text="Your OTP will appear here", font=("Courier", 18))
        self.otp_label.pack(pady=20)

        self.qr_label = tk.Label(self.root)
        self.qr_label.pack(pady=10)

    def _generate_key(self):
        key = self.ft_otp.generate_hex()
        self.ft_otp.encrypte_save_key(key)
        messagebox.showinfo(f"{color.OKGREEN}", "Key successfully generated and saved as ft_otp.key")
        qr_img = self.ft_otp.generate_qr_code("ft_otp.key")
        if qr_img is None:
            messagebox.showerror("Error", "Failed to generate QR code.")
            return
        img = qr_img.resize((200, 200))
        img_tk = ImageTk.PhotoImage(img)
        self.qr_label.configure(image=img_tk)
        tk.PhotoImage = img_tk

    def _generate_otp(self):
        if not os.path.exists("ft_otp.key"):
            messagebox.showerror("Error", "No key file found. Generate a key first.")
            return

        otp = self.ft_otp.totp()
        self.otp_label.config(text=f"{otp}\n wait a few seconds to generate a new key", fg="black", font=("Arial", 16, "bold"))
