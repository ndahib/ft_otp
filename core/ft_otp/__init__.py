from ..constants import STEP, START_TIME, OUTPUT_DIGITS
import struct
import hmac
import hashlib
import time
from math import floor
import qrcode


def dynamic_truncate(hmac_digest: bytes) -> int:
    """
    Apply RFC dynamic truncation: use low nibble of last byte as offset,
    take 4 bytes from offset, mask MSB to get 31-bit integer.
    """
    offset = hmac_digest[-1] & 0x0F
    four = hmac_digest[offset : offset + 4]
    code_int = struct.unpack(">I", four)[0] & 0x7FFFFFFF
    return code_int


def read_shared_key_from_file():
    with open("ft_otp.key", "rb") as f:
        raw = f.read().strip()

    # Handle UTF-16 BOM (0xff 0xfe or 0xfe 0xff)
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        raw = raw.decode("utf-16")
    else:
        raw = raw.decode("utf-8")

    return raw.strip()


def totp():
    """
    Compute a TOTP code for the given shared key hexadecimal string.

    TOTP = Truncate(HMAC(secret, floor(currentTime / timestep))) % 10^digits.
    """
    shared_key = read_shared_key_from_file()
    key_bytes = bytes.fromhex(shared_key)

    T = floor((time.time() - START_TIME) / STEP)

    hmac_digest = hmac.new(key_bytes, struct.pack(">Q", T), hashlib.sha1).digest()

    code_int = dynamic_truncate(hmac_digest)
    otp = code_int % (10**OUTPUT_DIGITS)
    return str(otp).zfill(OUTPUT_DIGITS)

def generate_qr_code(key, user_label):
    """
    Generate qr code containing the key, the user can just scan it with Google Authenticator, and it will automatically configure their app with  TOTP seed.
    Return: Image png or qr code
    """

    uri = f"otpauth://hotp/ft_otp:{user_label}?secret={key}&issuer=ft_otp&counter=0"

    img = qrcode.make(uri)
    img.save("ft_otp_qr.png")
