import sys


def greeting_msg(name):
    return "Hello %s !" % name


def main(args):
    print(greeting_msg(args[0]))
    print("Janome is a Japanese morphological analysis engine written by pure Python.")


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
