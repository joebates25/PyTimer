#!/usr/local/bin/python3.3

import threading
import time
import os
import sys
import random
import argparse

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""

    class _GetchUnix:
        def __init__(self):
            import tty, sys

        def __call__(self):
            import sys, tty, termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch


    class _GetchWindows:
        def __init__(self):
            import msvcrt

        def __call__(self):
            import msvcrt
            return msvcrt.getch()


    def __init__(self):
        try:
            self.impl = self._GetchWindows()
        except ImportError:
            self.impl = self._GetchUnix()

    def __call__(self): return self.impl()


class Sound:
    _bee = 0

    def __init__(self):
        try:
            import winsound as win
            self._bee = 1
        except ImportError:
            self._bee = 0

    def beep(self, sound):
        if self._bee == 0:
            self._mac_os_sound(sound)
        else:
            self.windows_sound(sound)

    def _windows_sound(self, sound):
        self._w.PlaySound('%s.wav' % sound, self._w.SND_FILENAME)

    def _mac_os_sound(self, sound):
        import os
        #print("afplay " + str(sound).replace(".wav", "") + ".wav")
        os.system("afplay " + sound)


class Timer(threading.Thread):
    ALARM_SOUND_ENVIRONMENT_VARIABLE = "PyTimerAlarm"
    _running = True
    _finished = False
    _time = 5
    _verbose = True
    _pauseTime = 0
    _player = Sound()
    _reverse = False
    _audioSound = os.environ[ALARM_SOUND_ENVIRONMENT_VARIABLE]
    _execScript = []
    _rand = random.random()
    _infinite = False
    _manager = None
    _startTime = 0
    _endTime = 0
    _timeRemaining = 0
    _next_probability_repeat = 1

    def __init__(self, newTimer=None, manager=None, infinite = False, next_probability_repeat=1):
        '''
        Initilizes Timer. Sets manager to call to when timer is started as well as new Timer to call if such a timer
            exists
        :param newTimer: New Timer to be called
        :param manager: Manager to callback to
        :return: Initialized Timer
        '''
        super().__init__()
        self._manager = manager
        self._rand = random.random()
        self._newTimer = newTimer
        self._infinite = infinite
        self._next_probability_repeat = next_probability_repeat

    def run(self):
        '''

        :return: Runs timer. This is where the timer calls its manager
        '''
        self._manager.receive_Timer(self)
        self._startTime = time.time()
        self._endTime = self._startTime + self._time
        self.timeRemaining = self._endTime - self._startTime
        while True:
            if self._running:
                if self._pauseTime != 0:
                    self._endTime += time.time() - self._pauseTime
                    self._pauseTime = 0
                self.timeRemaining = self._endTime - time.time()
                if self.timeRemaining > 0:
                    self._message(self._seconds_to_time_string(self.timeRemaining), carraige=True)
                else:
                    self._finished = True
                    self._onFinished()
                    os._exit(0)

    def finished(self):
        '''
        :return: True if the timer is complete
        '''
        return self._finished

    def add_script(self, s):
        '''
        Sets script for timer to execute
        :param s: Script
        :return:
        '''
        self._execScript.append(s)

    def set_audio_sound(self, s):
        '''
        Sets sound for timer to play
        :param s: Sound
        :return:
        '''
        self._audioSound = s

    def set_reverse(self):
        return self._reverse

    def set_verbose(self, v):
        self._verbose = v

    def _message(self, m, carraige=False):
        '''
        Writes message to console
        :param m: Message to write
        :param carraige: Whether or not to prefix a carraige return
        :return:
        '''
        if self._verbose:
            if not carraige:
                print("\r" + m + (" " * 35))
            else:
                print("\r" + m, end="")

    def _execute_scripts(self):
        '''
        Executes Script
        :return:
        '''
        for s in self._execScript:
            print("Not yet implemented. Script ran... " + s)

    def _play_sound(self):
        if self._audioSound != "":
            self._player.beep(self._audioSound)

    def _onFinished(self):
        '''
        Determines and executes proper finishing action then executes next timer if such a timer exists
        :return:
        '''
        if self._execScript != []:
            self._execute_scripts()
        if self._audioSound != None:
            self._play_sound()
        if self._infinite:
            self._newTimer = Timer(infinite=True, manager=self._manager)
            self._newTimer.set_time(self._time)
            for script in self._execScript:
                self._newTimer.add_script(script)
            self._newTimer.set_audio_sound(self._audioSound)
            self._newTimer.set_verbose(self._verbose)
            self._newTimer.run()
        elif self._newTimer != None:
            self._newTimer.run()

    def toggle(self):
        '''
        Toggles timer on/off
        :return:
        '''
        if self._running:
            self._running = False
            self._pauseTime = time.time()
            self._message("Paused" + " " * 10, carraige=True)
        else:
            self._running = True


    def set_time(self, t):
        self._time = t

    def set_next_probability(self, p):
        self._next_probability_repeat = p

    def set_next_timer(self,t):
        self._newTimer = t

    def _seconds_to_time_string(self, s):
        '''
        Converts float seconds into string "hours:minutes:seconds:milliseconds"
        :param s: float: seconds
        :return: string: converted float to string
        '''
        hours = int(s / 3600)
        s -= (hours * 3600)
        minutes = int(s / 60)
        s -= (minutes * 60)
        seconds = int(s)
        s -= int(s)
        milliseconds = 0
        if s > 0:
            milliseconds = int(s * 1000)
        return "{0:02}:{1:02}:{2:02}:{3:04}".format(hours, minutes, seconds, milliseconds)

    def increment_time(self):
        self._endTime += 60

    def decrement_time(self):
        self._endTime -= 60

    def copy(self):
        t = Timer(manager=self._manager, infinite=self._infinite)
        t.set_time(self._time)
        t.set_verbose(self._verbose)
        t.set_audio_sound(self._audioSound)
        t.set_next_timer(self._newTimer)
        t.set_next_probability(self._next_probability_repeat)
        for script in self._execScript:
            t.add_script(script)
        return t


class ArgumentParser():
    '''
        Wrapper class written to disable error messages from being printed to the screen in the event of testing
    '''

    usage = "-----PyTimer-----------\n" \
            "Key Mappings:\n" \
            "t - toggle timer on/off\n" \
            "r - repeat the current timer after complete\n" \
            "i - increment current timer by 1 minute \n" \
            "d - decrement current timer by 1 minute\n" \
            "m - mute current timer\n" \
            "q - quit\n\n" \
            "To set an alarm sound file, set an env variable [PyTimerAlarm] (no square brackets) to the absolute file path"

    class ArgParseWrapper(argparse.ArgumentParser):
        def error(self, message):
            pass

    def __init__(self, hide_errors=False):
        self._parser = self._init_parsed_args(hide_errors)

    def _init_parsed_args(self, hide_errors):
        if hide_errors:
            parser = self.ArgParseWrapper(
                description=self.usage)
        else:
            parser = argparse.ArgumentParser(
                description=self.usage)
        parser.add_argument("minutes", action="store", nargs="*", type=float)
        parser.add_argument("-seconds", "-s", action="store_true", help="Set if input should be interpreted as seconds")
        parser.add_argument("-repeat", "-r", nargs="*", type=int,
                            help="Specifies fixed, random, or infinite number of repetitions")
        parser.add_argument("-verbose", "-v", action="store_false", help="Call to turn off printing")
        parser.add_argument("-sound", action="store", nargs="*",
                            help="Set new sound to be played. Set to 'None' for no sound.")
        parser.add_argument("-exec", "-e", action="store", nargs="*",
                            help="Scripts to be executed when timer is complete.")
        parser.add_argument("-hours", "-hh", action="store_true", help="Set if input should be interpreted as hours")

        # Feature to calculate next ring based on probability
        # Mathmatical options

        return parser

    def parse_arguments(self):
        args = self._parser.parse_args()
        return self._validate_args(args)

    def validate_string(self, s):
        return self._validate_args(self._parser.parse_args(s.split(" ")))[0]

    def _validate_args(self, args):
        is_valid = True
        arg_errors = []

        '''
            Validate minutes args
        '''
        if ((len(args.minutes) > 2)):
            is_valid = False
            arg_errors.append("Invalid number of parameters: minutes")
        elif (len(args.minutes) == 2):
            if (int(args.minutes[0]) > int(args.minutes[1])):
                is_valid = False
                arg_errors.append(
                    "Invalid order of parameters: minutes. {0} is greater than {1}".format(args.minutes[0],
                                                                                           args.minutes[1]))

        if (args.repeat is not None):
            if (len(args.repeat) > 2):
                is_valid = False
                arg_errors.append("Invalid number of parameters: -r")
            elif (len(args.repeat) == 2):
                if (args.repeat[0] > args.repeat[1]):
                    is_valid = False
                    arg_errors.append("Invalid order of parameters: -r")
                elif (args.repeat[0] == 0 and args.repeat[1] is not 0):
                    is_valid = False
                    arg_errors.append("Invalid parameters: -r")


        if args.exec is not None:
            if len(args.exec) == 0:
                is_valid = False
                arg_errors.append("Invalid number of parameters: -exec")

        if args.sound is not None:
            if len(args.sound) > 1:
                is_valid = False
                arg_errors.append("Invalid number of parameters: -sound")

        if args.seconds and args.hours:
            is_valid = False
            arg_errors.append("Invalid parameter selection: -hh and -s flags cannot both concurrently invoked")

        return is_valid, args, arg_errors


class TimerAssembler():
    '''
    This takes a set of parsed arguments and assembled a chain of timers based on the args
    '''

    @staticmethod
    def assembleTimers(parsed_args, manager):
        time_arg = parsed_args.minutes
        mainTimer = None
        time = 0
        inf = False
        repeat = 1
        if (parsed_args.repeat is not None):
            if len(parsed_args.repeat) == 1:
                repeat = int(parsed_args.repeat[0])
            elif len(parsed_args.repeat) == 2:
                repeat = random.randint(int(parsed_args.repeat[0]), int(parsed_args.repeat[1]))
            else:
                repeat = 1
                inf = True

        for x in range(repeat):
            if len(parsed_args.minutes) == 1:
                time = parsed_args.minutes[0]
            else:  # if len = 2
                time = random.uniform(parsed_args.minutes[0], parsed_args.minutes[1])

            if not parsed_args.seconds and not parsed_args.hours:
                time = time * 60
            elif parsed_args.hours:
                time = time * 3600

            if mainTimer is None:
                mainTimer = Timer(infinite=inf, manager=manager)
            else:
                newTimer = Timer(newTimer=mainTimer,  manager=manager)
                mainTimer = newTimer
            mainTimer.set_time(time)
            mainTimer.set_verbose(parsed_args.verbose)
            if parsed_args.exec != None:
                for script in parsed_args.exec:
                    mainTimer.add_script(script)
            if parsed_args.sound != None:
                if len(parsed_args.sound) > 0 and parsed_args.sound[0] != "None":
                    mainTimer.set_audio_sound(parsed_args.sound[0])
                else:
                    mainTimer.set_audio_sound("")


        return mainTimer


class TimerManager():
    '''
    This class takes a timer, runs it, and manages the keystrokes sent to the timer from the user
    -Keystroke processing is handled in process_char
    -Timers call receive_Timer to update timer manager that a new timer is starting
    '''

    _currentActiveTimer = None
    def set_initial_timer(self,t):
        self._currentActiveTimer = t

    def start_Timers(self):
        getch = _Getch()
        self._currentActiveTimer.start()
        while(True):
            char = getch()
            self._process_char(str(char).replace("b'", "").replace("'", ""))


    def receive_Timer(self, t):
        self._currentActiveTimer = t

    def _process_char(self, c):
        #Toggle Timer
        if c == 't':
            self._currentActiveTimer.toggle()
        #Decrement Timer by 1 Minute
        elif c == 'd':
            self._currentActiveTimer.decrement_time()
        #Increment Timer by 1 Minute
        elif c == 'i':
            self._currentActiveTimer.increment_time()
        #Run current timer again
        elif c == 'r':
            copy = self._currentActiveTimer.copy()
            self._currentActiveTimer.set_next_timer(copy)
        #Mute timer sound
        elif c == 'm':
            self._currentActiveTimer.set_audio_sound("")
        #quit
        elif c == 'q':
            os._exit(0)


if __name__ == "__main__":
    argParser = ArgumentParser()

    is_valid, parsed_args, errors = argParser.parse_arguments()
    if is_valid:
        manager = TimerManager()
        timer = TimerAssembler.assembleTimers(parsed_args=parsed_args, manager=manager)
        manager.set_initial_timer(timer)
        manager.start_Timers()
    else:
        for error in errors:
            print(error)
