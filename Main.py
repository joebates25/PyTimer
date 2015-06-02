__author__ = 'josephbates'

import time
import os
import random
import argparse
import sys

verbose = False

sound = "~/alarmsounds/siren.wav"

if verbose:
    print("Timer sound: " + sound)

def ring_timer_sec(seconds):
    if verbose:
        print("Ringing in " + str(seconds) + " seconds.")
        print("Beginning timer: ")
    index = 0
    for x in range(int(seconds)):
        if verbose:
            count = int(seconds) - index
            sys.stdout.write("\rCountdown: %d..." % count)
            sys.stdout.flush()
            index += 1
        time.sleep(1)

    if verbose:
        print("\nTimer complete.")


def constructSummary(interval_length, repeat):
    summary = "Timer will ring "
    if type(interval_length) == tuple:
        summary += "between " + \
                  str(interval_length[0]) + " and " + \
                  str(interval_length[1]) + " seconds "
    else:
        summary += str(interval_length) + " seconds "

    summary += "with "
    if type(repeat) == tuple:
        summary += "between " + str(repeat[0]) + " and " + str(repeat[1]) + " repetitions..."
    else:
        summary += str(repeat) + " repetitions..."
    return summary


def ring_timer_interval(interval_length, repeat = 1):
    if verbose:
        print(constructSummary(interval_length, repeat))
    if type(repeat) == tuple:
        repeat = random.randint(repeat[0], repeat[1])
        if verbose:
            print("Random repetitions selected: " + str(repeat))

    for x in range(repeat):
        if verbose:
            print("Beginning repetition " + str(x + 1) + " of " + str(repeat))
        if type(interval_length) is tuple:
            ring_timer_sec(random.randint(interval_length[0], interval_length[1]) * 1.0)
        else:
            ring_timer_sec(interval_length)



parser = argparse.ArgumentParser()
parser.add_argument("minutes", action="store", nargs="*")
parser.add_argument("-seconds", "-s", action="store_true", help="Set if input should be interpreted as seconds")
parser.add_argument("-repeat", "-r",  nargs="*", type=int, help="Specifies fixed (or random if 2 values given) number of repetitions")
parser.add_argument("-verbose", "-v", action="store_true", help="Set to have output printed")
parser.add_argument("-sound", action="store", nargs="?", help="Set new sound to be played")


parsed_args = parser.parse_args()
verbose = parsed_args.verbose

if parsed_args.sound is not None:
    if parsed_args.sound.endswith(".wav"):
        sound = "~/alarmsounds/" + parsed_args.sound
    else:
        sound = "~/alarmsounds/" + parsed_args.sound + ".wav"
if verbose:
    print("Sound playing: " + sound)

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

