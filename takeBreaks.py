# Created by Jone Skaara in order to remember to take breaks from work.
# Required Ubuntu dependencies:
# sudo apt install gnome-screensaver
# sudo apt install zenity
# The screen locking is works with gnome.

import datetime
import time
import os
import subprocess

# Parameters
max_active_minutes = 30      # Time you can work before being reminded to take a break.
min_break_duration = 5       # Time you have to be inactive for in order for it to count as a break. Reading a website for 2 minutes is not a break.
active_seconds_threshold = 5 # Time you have to be active for in order to register as activity. Bumping the desk should be ignored.
lock_screen_warnings = 6     # Number of 'take a break' notifications you get before the screen locks. Set 0 to lock screen immediately. Set -1 to disable screen locking.
debug = False                # Extra logging

# State
# Initialize variables to track mouse and keyboard activity
mouse_active_old = subprocess.check_output("xprintidle", shell=True)
mouse_active_old = (time.time() - int(mouse_active_old) / 1000) / 60

keyboard_active_old = subprocess.check_output("xprintidle", shell=True)
keyboard_active_old = (time.time() - int(keyboard_active_old) / 1000) / 60

active_minutes = 0 # How many minutes with activity since last break, does not need to be consecutive.
break_minutes = 0  # How many minutes you've been inactive for.

print("Started checking for mouse and keyboard activity.")
print("If you work for longer than " + str(max_active_minutes) + " minutes you'll be told to take a break.")
if lock_screen_warnings > 0: 
    print("If you keep working past break time you be reminded every minute for " + str(lock_screen_warnings - 1) + " minutes before the screen will lock.")
    print("The screen will keep locking every minute until you take a " + str(min_break_duration) + " minute break")


# Every minute, check for activity, increment active_minutes or break_minutes, then handle the change:
while True:
    # Sleep a minute
    time.sleep(60)
    
    # Get the mouse active time
    mouse_active = subprocess.check_output("xprintidle", shell=True)
    mouse_active = (time.time() - int(mouse_active) / 1000) / 60

    # Get the keyboard active time
    keyboard_active = subprocess.check_output("xprintidle", shell=True)
    keyboard_active = (time.time() - int(keyboard_active) / 1000) / 60

    now = datetime.datetime.now()

    delta = (mouse_active - mouse_active_old) + (keyboard_active - keyboard_active_old)
    if debug:
        print("delta=" + str(round(delta, 3)) + " active_minutes=" + str(active_minutes) + " break_minutes=" + str(break_minutes))

    if delta >= active_seconds_threshold / 60: # If there has been more than active_seconds_threshold seconds of activity last minute
        mouse_active_old = mouse_active
        keyboard_active_old = keyboard_active

        active_minutes = active_minutes + 1
        active_message = now.strftime('%H:%M') + " You are active #" + str(active_minutes)

        if break_minutes >= min_break_duration:
            message = "Welcome back! You had a " + str(break_minutes) + " minute break! :D"
            print(message)
            subprocess.call(['notify-send', message])
        break_minutes = 0
        if active_minutes >= max_active_minutes:
            subprocess.call(['notify-send', 'Take a break!'])
            active_message = active_message + " Take a break!"
            # Lock screen if you ignore the notification
            if lock_screen_warnings == 0:
                os.popen('gnome-screensaver-command --lock')
            elif lock_screen_warnings > 0:
                if active_minutes >= max_active_minutes + lock_screen_warnings - 1:
                    active_message = active_message + " Locking screen in 1 minute!"
                    os.popen('zenity --info --text "Take a break! Screen will be locked soon."')
                    if active_minutes >= max_active_minutes + lock_screen_warnings:
                        os.popen('gnome-screensaver-command --lock')
        print(active_message)
    else: 
        break_minutes = break_minutes + 1
        print(now.strftime('%H:%M') + " You are away #" + str(break_minutes))

    if break_minutes >= min_break_duration:
        active_minutes = 0