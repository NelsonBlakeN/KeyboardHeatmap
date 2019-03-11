#!/usr/bin/env python3
'''Create a heatmap of the keys used over a period of time'''
import json
from collections import defaultdict
from pynput.keyboard import Key, KeyCode, Listener

# Create static dict
with open('/home/blake/Dropbox/Projects/KeyboardHeatmap/all_time.json') as file:
    ALL_TIME = json.load(file)

# Create defaultdict from current keys dict
KEYS = defaultdict(int, ALL_TIME["keys"])
ALL_TIME["keys"] = KEYS

def on_press(_key):
    '''What to do when a key is pressed'''
    if isinstance(_key, KeyCode):
        key = _key.char
        ALL_TIME["total"] += 1
        ALL_TIME["keys"][key] += 1
    else:
        key = str(Key(_key.value)).split('.')[1]
        ALL_TIME["total"] += 1
        ALL_TIME["keys"][key] += 1

try:
    with Listener(
            on_press=on_press) as listener:
        listener.join()
finally:
    with open('/home/blake/Dropbox/Projects/KeyboardHeatmap/all_time.json', "w") as file:
        # Convert defaultdict back to normal dict
        ALL_TIME["keys"] = dict(ALL_TIME["keys"])
        file.write(json.dumps(ALL_TIME, sort_keys=True, indent=4, separators=(',', ':')))
