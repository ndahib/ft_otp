from core.management import Management
import sys


def main():
    manager = Management(sys.argv[1:])
    manager.execute()


if __name__ == "__main__":
    main()
# RFC test
# if __name__ == "__main__":
#     test_key = "3132333435363738393031323334353637383930"
#     test_times = [59, 1111111109, 1111111111, 1234567890, 2000000000, 20000000000]
#     for t in test_times:
#         print(t, "=>", totp_for_time(test_key, t))
