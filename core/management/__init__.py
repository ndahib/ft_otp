import sys
from argparse import ArgumentParser
from ..constants import color
import os

from ..ft_otp import totp


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
