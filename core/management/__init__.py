import sys
from argparse import ArgumentParser
from ..constants import color
import os
import tkinter as tk
from tkinter import messagebox
from ..ft_otp import totp, generate_qr_code


class Management:
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.program_name = self.argv[0]

    def _shared_key(self, key):
        if os.path.isfile(key):
            with open(key, "r") as f:
                key = f.read().strip()
        try:
            bytes.fromhex(key)
            with open("ft_otp.key", "w", encoding="utf-16") as f:
                f.write(key)
            print(f"{color.OKGREEN}Key was successfully saved in ft_otp.key. {color.ENDC}")
        except ValueError:
            print(f"{color.FAIL}{sys.argv[0]}: error: key must be 64 hexadecimal characters..{color.ENDC}")

    def _parse_commande_line(self):
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = "help"
        parser = ArgumentParser(
            usage="Usage: %s command [options]" % self.program_name, prog=self.program_name, description="A simple TOTP generator."
        )
        parser.add_argument(
            "-g",
            "--generate",
            help="The program receives as argument a hexadecimal key of at least 64 characters. The program stores this key safely in a file called ft_otp.key, which is encrypted.",
            type=str,
        )
        parser.add_argument(
            "-k",
            "--key",
            help="generate a new temporary password based on the key given as argument and prints it on the standard output.",
            type=str,
        )
        
        pqr = parser.add_parser("provision", help="print otpauth URI and optionally a QR")
        pqr.add_argument("key", help="hexadecimal key ")
        pqr.add_argument("account", help="account name (e.g., alice@example.com)")
        pqr.add_argument("--issuer", help="Issuer (service name)")
        pqr.add_argument("--digits", type=int, default=6)
        pqr.add_argument("--algo", choices=["SHA1", "SHA256", "SHA512"], default="SHA1")
        pqr.add_argument("--period", type=int, default=30)
        pqr.add_argument("--qr-file", help="filename to write QR PNG (requires 'qrcode' package)")
        args = parser.parse_args()
        if subcommand == "help":
            parser.print_help()
            sys.exit(0)
        return args

    def execute(self):
        args = self._parse_commande_line()

        if args.generate:
            self._shared_key(args.generate)
        elif args.key:
            print(totp())
        elif args.generate_qr:
            generate_qr_code()




# class FtOtpApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("ft_otp — HOTP Generator")
#         self.root.geometry("500x550")
#         self.root.resizable(False, False)

#         tk.Label(root, text="ft_otp HOTP Generator", font=("Arial", 16, "bold")).pack(pady=10)

#         # Buttons
#         tk.Button(root, text="Generate New Key", command=self.generate_key, bg="#2e86de", fg="white", width=20).pack(pady=10)
#         tk.Button(root, text="Generate OTP", command=self.generate_otp, bg="#27ae60", fg="white", width=20).pack(pady=10)

#         # OTP display
#         self.otp_label = tk.Label(root, text="Your OTP will appear here", font=("Courier", 18))
#         self.otp_label.pack(pady=20)

#         # QR code display
#         self.qr_label = tk.Label(root)
#         self.qr_label.pack(pady=10)

#     def generate_key(self):
#         key = genereate_hex
#         messagebox.showinfo("Success", "Key successfully generated and saved as ft_otp.key")

#         # Generate QR code
#         qr_path = generate_qr_code(key_hex)
#         img = Image.open(qr_path).resize((200, 200))
#         img_tk = ImageTk.PhotoImage(img)
#         self.qr_label.configure(image=img_tk)
#         self.qr_label.image = img_tk

#     def generate_otp(self):
#         if not os.path.exists("ft_otp.key"):
#             messagebox.showerror("Error", "No key file found. Generate a key first.")
#             return

#         try:
#             key_hex = decrypt_key()
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to read key: {e}")
#             return

#         # Use a simple counter (could be time-based or stored persistently)
#         counter = int.from_bytes(os.urandom(4), 'big') % 100000
#         otp = hotp(key_hex, counter)
#         self.otp_label.config(text=otp, fg="black", font=("Courier", 26, "bold"))