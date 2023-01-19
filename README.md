# TakeBreaks
A simple python script that reminds you to take breaks after a certain amount of time spent active at your PC.  
Made for Ubuntu using sanity to send notifications and gnome-screensaver to lock screen. However, it could probably be changed pretty easily for Windows.
## Install
Dependencies:
```bash
sudo apt install gnome-screensaver # Lock screen
sudo apt install zenity # System notifications
```
Start script:
```bash
python3 takeBreaks.py
```

```
Started checking for mouse and keyboard activity.
If you work for longer than 30 minutes you'll be told to take a break.
If you keep working past break time you be reminded every minute for 5 minutes before the screen will lock.
The screen will keep locking every minute until you take a 5 minute break
12:25 You are active #1
12:26 You are active #2
12:27 You are active #3
...
12:53 You are active #29
12:54 You are away #1
12:55 You are active #30 Take a break!
12:56 You are active #31 Take a break!
12:57 You are active #32 Take a break!
12:58 You are active #33 Take a break!
12:59 You are active #34 Take a break!
13:00 You are active #35 Take a break! Locking screen in 1 minute!
```

## Configuration
At the top of the script are some parameters that can be changed to your liking:
```
# Parameters
max_active_minutes = 30      # Time you can work before being reminded to take a break.
min_break_duration = 5       # Time you have to be inactive for in order for it to count as a break. Reading a website for 2 minutes is not a break.
active_seconds_threshold = 5 # Time you have to be active for in order to register as activity. Bumping the desk should be ignored.
lock_screen_warnings = 6     # Number of 'take a break' notifications you get before the screen locks. Set 0 to lock screen immediately. Set -1 to disable screen locking.
debug = False                # Extra logging
```
By default, if you touch your mouse or keyboard for less than 5 seconds (active_seconds_threshold) in total each minute you're considered inactive.