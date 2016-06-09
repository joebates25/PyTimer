__author__ = 'josephbates'

import argparse
from PyTimer.Timer import  ArgumentParser

def test_working_strings(parser):
    error_flag = False
    for test_arg_string in open("arg_test_strings_pos.txt").readlines():
        if not test_arg_string.startswith("#"):
            test_arg_string = test_arg_string.replace("\n", "")
            try:
                assert parser.validate_string(test_arg_string) is True
            except:
                print("Assertion Error for string (should pass): " + test_arg_string)
                error_flag = True
    return error_flag



def test_failing_strings(parser):
    error_flag = False
    for test_arg_string in open("arg_test_strings_neg.txt").readlines():
        if not test_arg_string.startswith("#"):
            test_arg_string = test_arg_string.replace("\n", "")
            try:
                assert parser.validate_string(test_arg_string) is False
            except Exception as e:
                print("Assertion Error for string (should fail): " + test_arg_string)
                error_flag = True
    return error_flag

def main():
    parser = ArgumentParser(hide_errors=True)
    error_flag = False
    error_flag = test_working_strings(parser)
    error_flag = test_failing_strings(parser) if not error_flag else error_flag

    if not error_flag:
        print("All tests successful!")




if __name__ == '__main__':
    main()
