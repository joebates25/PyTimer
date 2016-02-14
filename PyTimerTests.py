__author__ = 'josephbates'

import argparse
from Main import validate_args, init_parse_args

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
    error_flag = test_working_strings(parser)
    error_flag = test_failing_strings(parser)

    if not error_flag:
        print("All tests successful!")




if __name__ == '__main__':
    main()
