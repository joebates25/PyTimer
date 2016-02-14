__author__ = 'josephbates'

import time
import os
import random
import argparse
import sys


def init_parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("minutes", action="store", nargs="*")
    parser.add_argument("-seconds", "-s", action="store_true", help="Set if input should be interpreted as seconds")
    parser.add_argument("-repeat", "-r",  nargs="*", type=int, help="Specifies fixed (or random if 2 values given) number of repetitions")
    parser.add_argument("-verbose", "-v", action="store_true", help="Call to turn off printing")
    parser.add_argument("-sound", action="store", nargs="?", help="Set new sound to be played. Set to 'None' for no sound.")
    parser.add_argument("-exec", "-e", action="store", nargs="*", help="Set new sound to be played")
    parser.add_argument("-stop", action="store_true", help="Starts stopwatch")
    parser.add_argument("-stand", action="store", nargs=1, help="Starts stopwatch")


    return parser.parse_args()


verbose = True
parsed_args = init_parse_args()
ALARM_SOUND_ENVIRONMENT_VARIABLE = "PyTimerAlarm"


#Converts seconds value to formatted hour:date:second string
#Ex. 4432 seconds -> "01:13:52"
def seconds_to_time_string(s):
    minutes = 0
    seconds = 0
    hours = 0
    time = s
    hours = int(time / 3600)
    time = time - (hours * 3600)

    minutes = int(time / 60)
    time = time - (minutes * 60)
    seconds = time

    return "%02d" % (hours,) + ":" + "%02d" % (minutes,) + ":" + "%02d" % (seconds,)






def print_verbose(s):
    if verbose:
        print(s)


def standby(seconds):
    index = 0
    for x in range(int(seconds)):
        if verbose:
            count = int(seconds) - index
            sys.stdout.write("\rStandby:..." + seconds_to_time_string(count))
            sys.stdout.flush()
            index += 1
        time.sleep(1)

#Check OS Env for sound path
def getSoundFilePath():
    return os.environ[ALARM_SOUND_ENVIRONMENT_VARIABLE]


def ring_timer_sec(seconds):
    print_verbose("Ringing in " + seconds_to_time_string(seconds))
    print_verbose("Beginning timer: ")
    index = 0
    for x in range(int(seconds)):
        if verbose:
            count = int(seconds) - index
            sys.stdout.write("\rCountdown:..." + seconds_to_time_string(count))
            sys.stdout.flush()
            index += 1
        time.sleep(1)

    print_verbose("\nTimer complete.")
    if (parsed_args.sound != "None" and parsed_args.sound != "n"):
        os.system("afplay " + sound)
    if parsed_args.exec is not None:
        os.system("./" + str(parsed_args.exec[0]))

def timer_sec(seconds):
    print_verbose("Complete in " + seconds_to_time_string(seconds))
    print_verbose("Beginning timer: ")
    index = 0
    for x in range(int(seconds)):
        if verbose:
            count = int(seconds) - index
            sys.stdout.write("\rCountdown:..." + seconds_to_time_string(count))
            sys.stdout.flush()
            index += 1
        time.sleep(1)
    print_verbose("\nTimer complete.")
    if parsed_args.exec:
        execute_scripts()
    else:
        ring_alarm()



#TODO: Add checking for sound file override in parsed args
def ring_alarm():
    path = getSoundFilePath()
    if path != "":
        if os.path.exists(path):
            os.system("afplay " + path)
        else:
            print_verbose("The file " + path + " cannot be found. Please verify it exists.")

def execute_scripts():
    if parsed_args.exec is not None:
       for script in parsed_args.exec:
           if os.path.exists(script):
               os.system("./" + str(script))
           else:
                print_verbose("The shell script " + script + " could not be found. Please verify it exists.")


def constructSummary(interval_length, repeat):
    summary = "Timer will ring "
    if type(interval_length) == tuple:
        summary += "between " + \
                   seconds_to_time_string(interval_length[0]) + " and " + \
                   seconds_to_time_string(interval_length[1])
    else:
        summary += seconds_to_time_string(interval_length)

    summary += " with "
    if type(repeat) == tuple:
        summary += "between " + str(repeat[0]) + " and " + str(repeat[1]) + " repetitions..."
    else:
        summary += str(repeat) + " repetitions..."
    return summary


def ring_timer_interval(interval_length, repeat = 1):
    print_verbose(constructSummary(interval_length, repeat))
    if type(repeat) == tuple:
        repeat = random.randint(repeat[0], repeat[1])
        print_verbose("Random repetitions selected: " + str(repeat))

    for x in range(repeat):
        print_verbose("Beginning repetition " + str(x + 1) + " of " + str(repeat))
        if type(interval_length) is tuple:
            timer_sec(random.randint(interval_length[0], interval_length[1]) * 1.0)
        else:
            timer_sec(interval_length)

def list_to_string(l):
    st = ""
    for x in l:
        st += x[0]
    return st


def stopwatch():
    time_counted = 0
    while True:
        sys.stdout.write("\rTime:..." + seconds_to_time_string(time_counted))
        sys.stdout.flush()
        time.sleep(1)
        time_counted += 1





def main():


    sound = "~/alarmsounds/siren.wav"

    print_verbose("Timer sound: " + sound)


    if len(sys.argv) == 1 or parsed_args.stop:
        stopwatch()
    else:

        verbose = not parsed_args.verbose



        if parsed_args.sound is not None:
            if parsed_args.sound.endswith(".wav"):
                sound = "~/alarmsounds/" + parsed_args.sound
            else:
                sound = "~/alarmsounds/" + parsed_args.sound + ".wav"
        print_verbose("Sound playing: " + sound)

        #TODO: Add verbose status about script to be run
        seconds = 60

        if parsed_args.seconds:
            seconds = 1

        if len(parsed_args.minutes) == 1:
            minutes = int(parsed_args.minutes[0]) * seconds
        else:
            minutes = (int(parsed_args.minutes[0]) * seconds, int(parsed_args.minutes[1]) * seconds)

        if parsed_args.repeat is not None:
            if len(parsed_args.repeat) == 1:
                repeat = int(parsed_args.repeat[0])
            else:
                repeat = (int(parsed_args.repeat[0]), int(parsed_args.repeat[1]))
        else:
            repeat = 1

        ring_timer_interval(minutes, repeat)



if __name__ == "__main__":
    main()