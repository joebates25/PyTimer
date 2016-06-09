#!/usr/local/bin/python3.3

import threading
import time
import os
import sys
import random
import argparse


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
        print("afplay " + str(sound).replace(".wav", "") + ".wav")
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
    _audioSound = ""##os.environ[ALARM_SOUND_ENVIRONMENT_VARIABLE]
    _execScript = []
    _rand = random.random()




    def __init__(self, newTimer = None, manager = None):
        '''
        Initilizes Timer. Sets manager to call to when timer is started as well as new Timer to call if such a timer
            exists
        :param newTimer: New Timer to be called
        :param manager: Manager to callback to
        :return: Initialized Timer
        '''
        super().__init__()
        self._newTimer = newTimer
        self._manager = manager
        self._rand = random.random()



    def run(self):
        '''

        :return: Runs timer. This is where the timer calls its manager
        '''

        startTime = time.time()
        endTime = startTime + self._time
        timeRemaining = endTime - startTime
        while True:
            if self._running:
                if self._pauseTime != 0:
                    endTime += time.time() - self._pauseTime
                    self._pauseTime = 0
                timeRemaining = endTime - time.time()
                if timeRemaining > 0:
                    self._message(self._seconds_to_time_string(timeRemaining), carraige=True)
                    # time.sleep(.1)
                else:
                    self._finished = True
                    self._onFinished()
                    self._message("Done", False)
                    sys.exit()


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

    def _message(self, m, carraige = False):
        '''
        Writes message to console
        :param m: Message to write
        :param carraige: Whether or not to prefix a carraige return
        :return:
        '''
        if self._verbose:
            if not carraige:
                print("\n" + m)
            else:
                print("\r" + m, end ="")


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
        if self._newTimer != None:
            self._newTimer.run()


    def toggle(self):
        '''
        Toggles timer on/off
        :return:
        '''
        if self._running:
            self._running = False
            self._pauseTime = time.time()
        else:
            self._running = True

    def set_time(self, t):
        self._time = t

    def _seconds_to_time_string(self, s):
        '''
        Converts float seconds into string "hours:minutes:seconds:milliseconds"
        :param s: float: seconds
        :return: string: converted float to string
        '''
        hours = int(s / 3600)
        s = s - (hours * 3600)
        minutes = int(s / 60)
        s = s - (minutes * 60)
        seconds = int(s)
        s = s - int(s)
        milliseconds = 0
        if s > 0:
            milliseconds = int(s * 1000)
        return "{0:02}:{1:02}:{2:02}:{3:04}".format(hours, minutes, seconds, milliseconds)



class ArgumentParser():

    '''
        Wrapper class written to disable error messages from being printed to the screen in the event of testing
    '''
    class ArgParseWrapper(argparse.ArgumentParser):
        def error(self, message):
            pass

    def __init__(self, hide_errors = False):
        self._parser = self._init_parsed_args(hide_errors)

    def _init_parsed_args(self, hide_errors):
        if hide_errors:
            parser = self.ArgParseWrapper(description="To set an alarm sound file, set an env variable PyTimerAlarm to the absolute file path")
        else:
            parser = argparse.ArgumentParser(
                description="To set an alarm sound file, set an env variable PyTimerAlarm to the absolute file path")
        parser.add_argument("minutes", action="store", nargs="*", type=float)
        parser.add_argument("-seconds", "-s", action="store_true", help="Set if input should be interpreted as seconds")
        parser.add_argument("-repeat", "-r",  nargs="*", type=int, help="Specifies fixed, random, or infinite number of repetitions")
        parser.add_argument("-verbose", "-v", action="store_false", help="Call to turn off printing")
        parser.add_argument("-sound", action="store", nargs="*", help="Set new sound to be played. Set to 'None' for no sound.")
        parser.add_argument("-exec", "-e", action="store", nargs="*", help="Scripts to be executed when timer is complete.")
        parser.add_argument("-hours", "-hh", action="store_true", help="Set if input should be interpreted as hours")
        #parser.add_argument("-stop", action="store_true", help="Starts stopwatch")
        #Possible future options
        #parser.add_argument("-par", action="store_true", help="Executes scripts in seperate thread")
        #parser.add_argument("-pomo", "-p", action="store_true", help="Starts pomodoro timer.")
        #parser.add_argument("-spar", action="store_true", help="Rings sound conncurrently with next timer")

        #parser.add_argument("-t", "-time", action="store", help="Set timer start time- units depending on other flags")
        #parser.add_argument("-seq", action="store_true", help="Interpret time argument as sequence of times")
        #parser.add_argument("-ro", action="store_true", help="Calculate time repeat only one timer and use for all interations of timer")
        #Feature to calculate next ring based on probability
        #Mathmatical options



        return parser

    def parse_arguments(self):
        args = self._parser.parse_args()
        return self._validate_args(args)

    def validate_string(self, s):
        return self._validate_args(self._parser.parse_args(s.split(" ")))[0]


    def _validate_args(self,args):
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
                arg_errors.append("Invalid order of parameters: minutes. {0} is greater than {1}".format(args.minutes[0], args.minutes[1]))



        if (args.repeat is not None):
            if (len(args.repeat) == 0 or len(args.repeat) > 2):
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

    def assembleTimers(self, parsed_args=None):
        time_arg = parsed_args.minutes
        mainTimer = None
        time = 0
        repeat = 1
        if (parsed_args.repeat is not None):
            if len(parsed_args.repeat) == 1:
                repeat = int(parsed_args.repeat[0])
            else:
                repeat = random.randint(int(parsed_args.repeat[0]),int(parsed_args.repeat[1]))

        for x in range(repeat):
            if len(parsed_args.minutes) == 1:
                time = parsed_args.minutes[0]
            else: #if len = 2
                time = random.uniform(parsed_args.minutes[0],parsed_args.minutes[1])


            if not parsed_args.seconds and not parsed_args.hours:
                time = time * 60
            elif parsed_args.hours:
                time = time * 3600

            if mainTimer is None:
                mainTimer = Timer()
            else:
                newTimer = Timer(newTimer=mainTimer)
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

if __name__ == "__main__":
    assembler = TimerAssembler()
    argParser = ArgumentParser()

    is_valid, parsed_args, errors = argParser.parse_arguments()
    if is_valid:
        timer = assembler.assembleTimers(parsed_args)
        timer.start()
    else:
        for error in errors:
            print(error)
