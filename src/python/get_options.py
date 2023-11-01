"""argparse tutorial: https://docs.python.org/3/howto/argparse.html"""
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("square", help="display a square of a given number",
                        type=int)

    args = parser.parse_args()
    print(args.square ** 2)


if __name__ == "__main__":
    main()
