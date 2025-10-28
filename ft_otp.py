from core.management import Management
import sys


def main():
    manager = Management(sys.argv[1:])
    manager.execute()


if __name__ == "__main__":
    main()

