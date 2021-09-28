import sys

from .version import IPPoolAbout as About


def main():
    argv = sys.argv
    print("IP Address Pool main()")
    print("%s" % About())
    if argv:
        print("args:")
        for arg in argv:
            print(arg)
    else:
        print("No args provided")


if __name__ == "__main__":
    exit(main())
