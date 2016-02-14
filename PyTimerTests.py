__author__ = 'josephbates'

import argparse
from Main import validate_args



def init_parse_args():
    parser = argparse.ArgumentParser(description="To set an alarm sound file, set an env variable PyTimerAlarm to the absolute file path")

    parser.add_argument("minutes", action="store", nargs="*")
    parser.add_argument("-seconds", "-s", action="store_true", help="Set if input should be interpreted as seconds")
    parser.add_argument("-repeat", "-r",  nargs="*", type=int, help="Specifies fixed (or random if 2 values given) number of repetitions")
    parser.add_argument("-verbose", "-v", action="store_true", help="Call to turn off printing")
    parser.add_argument("-sound", action="store", nargs="?", help="Set new sound to be played. Set to 'None' for no sound.")
    parser.add_argument("-exec", "-e", action="store", nargs="*", help="Set new sound to be played")
    parser.add_argument("-stop", action="store_true", help="Starts stopwatch")
    parser.add_argument("-stand", action="store", nargs=1, help="Starts stopwatch")
    return parser



def main():
    parser = init_parse_args()

    for test_arg_string in open("arg_test_strings.txt").readlines():
        if not test_arg_string.startswith("#"):
            try:
                assert validate_args(parser.parse_args(test_arg_string.replace("\n", "").split(" ")))[0] is True
            except:
                print("Assertion Error for string: " + test_arg_string)






if __name__ == '__main__':
    main()
