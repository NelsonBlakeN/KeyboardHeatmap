#!/usr/bin/env python3
'''Create a heatmap of the keys used over a period of time'''

def on_press(_key):
    '''What to do when a key is pressed'''
    if isinstance(_key, KeyCode):
        key = _key.char
        ALL_TIME["total"] += 1
        ALL_TIME["keys"][key] += 1
    else:
        key = str(Key(_key.value)).split('.')[1]    # Get key name from key
        ALL_TIME["total"] += 1
        ALL_TIME["keys"][key] += 1

def exit_handler():
    '''Write to file any time the program ends'''
    with open(DATAFILE, "w") as write_file:
        # Convert defaultdict back to normal dict
        ALL_TIME["keys"] = dict(ALL_TIME["keys"])
        write_file.write(json.dumps(ALL_TIME, sort_keys=True, indent=4, separators=(',', ':')))

try:
    import atexit
    import json
    from collections import defaultdict
    print("Importing keyboar listener...", end='')
    from pynput.keyboard import Key, KeyCode, Listener
    print("complete.")

    DATAFILE = '/home/blake/Dropbox/Projects/KeyboardHeatmap/all_time.json'

    # Create static dict
    with open(DATAFILE) as file:
        ALL_TIME = json.load(file)

    # Create defaultdict from current keys dict
    KEYS = defaultdict(int, ALL_TIME["keys"])
    ALL_TIME["keys"] = KEYS

    atexit.register(exit_handler)

except RuntimeError as _e:
    print("Setup failed: {}".format(_e))

try:
    print("Starting listener")
    with Listener(
            on_press=on_press) as listener:
        listener.join()
finally:
    exit_handler()
