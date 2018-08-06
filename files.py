import json
import os
from pathlib import Path
from variables import *
from datetime import datetime


def Load():
    tasks, settings = list(), DEFAULT_SETTINGS

    if Path(TASKS).is_file():
        try:
            with open(TASKS, 'r') as infile:
                tasks = json.loads(infile.read())
        except Exception as e:
            pass
        for x in range(len(tasks)):
            if tasks[x][3] is not 0:
                tasks[x][4] = datetime.strptime(tasks[x][4], '%Y-%m-%d %H:%M:%S')
            tasks[x][5] = datetime.strptime(tasks[x][5], '%Y-%m-%d %H:%M:%S')  # this one can be outside as it doesn't depend on the datesetting

    else:
        pass

    if Path(SETTINGS).is_file():
        with open(SETTINGS, 'r') as infile:
            settings.update(json.loads(infile.read()))
    else:
        pass
    return (tasks, settings)


def Save(tasks, settings):
    with open(TASKS, 'w') as outfile:
        json.dump(tasks, outfile, sort_keys=True, default=str)
    with open(SETTINGS, 'w') as outfile:
        json.dump(settings, outfile, indent=4, default=str)
