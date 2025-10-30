# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    __init__.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ndahib <ndahib@student.1337.ma>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/10/29 14:10:53 by ndahib            #+#    #+#              #
#    Updated: 2025/10/29 14:10:53 by ndahib           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
from argparse import ArgumentParser
from ..constants import color, OPTIONS, HEADER
from ..ft_otp import FtOtpGraphicalInterface, FtOtp
import shlex


class Management:
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.program_name = self.argv[0]
        self.ft_otp = FtOtp()

    def _parse_commande_line(self):
        parser = ArgumentParser(
            usage="Usage: %s command [options]" % self.program_name, prog=self.program_name, description="A simple TOTP generator."
        )
        sub_parser = parser.add_subparsers(dest="qr")
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

        pqr = sub_parser.add_parser("qr", help="generate a QR code using the given key")
        pqr.add_argument("key", help="hexadecimal key")
        pqr.add_argument("account", help="account name (e.g., alice@example.com)")
        pqr.add_argument("--issuer", help="Issuer (service name)", nargs="?", default="ft_otp")
        pqr.add_argument("--qr-file", help="filename to write QR PNG (requires 'qrcode' package)", nargs="?", default="ft_otp_qr.png")

        args = parser.parse_args()
        if len(sys.argv) == 1 or sys.argv[1] in ("-h", "--help", "help"):
            parser.print_help()
            sys.exit(0)
        return args

    def main_menu(self):
        if sys.argv.__len__() != 2:
            print(f"{color.FAIL}Invalid number of arguments. Type '{OPTIONS.HELP}' for help.{color.ENDC}")
        print(f"{color.HEADER}{HEADER}{color.ENDC}")
        print(f"{color.OKCYAN}Choose an option:{color.ENDC}\n" f"  {OPTIONS.CLI}\n" f"  {OPTIONS.GUI}\n" f"  {OPTIONS.EXIT}\n" f"  {OPTIONS.HELP}\n")

        while True:
            user_choice = input(f"{color.OKCYAN}>> {color.ENDC}").strip().lower()

            if user_choice == OPTIONS.CLI:
                self.run_cli_mode()

            elif user_choice == OPTIONS.GUI:
                try:
                    ft_otp_app = FtOtpGraphicalInterface(self.ft_otp)
                    ft_otp_app.root.mainloop()
                except KeyboardInterrupt:
                    print(f"{color.WARNING}Exiting...{color.ENDC}")
                    sys.exit(0)
                except Exception as e:
                    print(f"{color.FAIL}Error: {e}{color.ENDC}")

            elif user_choice == OPTIONS.EXIT:
                print(f"{color.WARNING}Exiting...{color.ENDC}")
                sys.exit(0)

            elif user_choice == OPTIONS.HELP:
                print(
                    f"{color.OKCYAN}Available options:{color.ENDC}\n"
                    f"  {OPTIONS.CLI}  - Run in command-line mode\n"
                    f"  {OPTIONS.GUI}  - Launch the graphical interface\n"
                    f"  {OPTIONS.EXIT} - Exit the program\n"
                    f"  {OPTIONS.HELP} - Show this help message\n"
                )

            else:
                print(f"{color.FAIL}Invalid option. Type '{OPTIONS.HELP}' for help.{color.ENDC}")

    def run_cli_mode(self):
        """Interactive CLI mode that reuses _parse_commande_line()."""

        print(f"{color.OKGREEN}Entering CLI mode... (type 'back' to return to menu){color.ENDC}\n")

        while True:
            cmd = input(f"{color.OKBLUE}ft_otp> {color.ENDC}").strip()

            if cmd.lower() in ("exit", "back", "quit"):
                print(f"{color.WARNING}Returning to main menu...{color.ENDC}\n")
                break

            if not cmd:
                continue

            try:
                args_list = shlex.split(cmd)
                sys.argv = [self.program_name] + args_list

                args = self._parse_commande_line()

                if args.generate:
                    self.ft_otp.encrypte_save_key(args.generate)
                elif hasattr(args, "qr") and hasattr(args, "key") and hasattr(args, "account"):
                    print(f"{color.OKCYAN}Generating QR code...{color.ENDC}")
                    self.ft_otp.generate_qr_code(args.key, args.account, args.issuer, args.qr_file)
                    print(f"{color.OKCYAN}QR code saved as {args.qr_file}{color.ENDC}")
                elif args.key:
                    print(f"{color.OKCYAN}Generating OTP for key...{color.ENDC}")
                    print(self.ft_otp.totp())

            except SystemExit:
                pass
            except Exception as e:
                print(f"{color.FAIL}Error: {e}{color.ENDC}")

    def execute(self):
        self.main_menu()
