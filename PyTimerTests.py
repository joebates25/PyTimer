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





def test_working_strings(parser):
    error_flag = False
    for test_arg_string in open("arg_test_strings_pos.txt").readlines():
        if not test_arg_string.startswith("#"):
            try:
                if (test_arg_string.replace("\n", "") == ""):
                    assert validate_args(parser.parse_args(""))[0] is True
                else:
                    assert validate_args(parser.parse_args(test_arg_string.replace("\n", "").split(" ")))[0] is True
            except:
                print("Assertion Error for string (should pass): " + test_arg_string)
                error_flag = True
    return error_flag





def test_failing_strings(parser):
    error_flag = False
    for test_arg_string in open("arg_test_strings_neg.txt").readlines():
        if not test_arg_string.startswith("#"):
            try:
                assert validate_args(parser.parse_args(test_arg_string.replace("\n", "").split(" ")))[0] is False
            except:
                print("Assertion Error for string (should fail): " + test_arg_string)
                error_flag = True
    return error_flag

def main():
    parser = init_parse_args()
    error_flag = False;
    #error_flag = test_working_strings(parser)
    error_flag = test_failing_strings(parser)

    if not error_flag:
        print("All tests successful!")




if __name__ == '__main__':
    main()
