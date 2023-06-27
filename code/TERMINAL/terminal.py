import os
import time

def clear_terminal():
    if os.name == 'posix':  # Para sistemas operativos tipo Unix (Linux, macOS)
        os.system('clear')
    elif os.name == 'nt':  # Para sistemas operativos tipo Windows
        os.system('cls')

def print_intro():
    clear_terminal()

    intro_text = "Battery  Cycler  Calibration"
    intro_ascii = """
    
  ____        _   _                      _____           _               _____      _ _ _               _   _             
 |  _ \      | | | |                    / ____|         | |             / ____|    | (_) |             | | (_)            
 | |_) | __ _| |_| |_ ___ _ __ _   _   | |    _   _  ___| | ___ _ __   | |     __ _| |_| |__  _ __ __ _| |_ _  ___  _ __  
 |  _ < / _` | __| __/ _ \ '__| | | |  | |   | | | |/ __| |/ _ \ '__|  | |    / _` | | | '_ \| '__/ _` | __| |/ _ \| '_ \ 
 | |_) | (_| | |_| ||  __/ |  | |_| |  | |___| |_| | (__| |  __/ |     | |___| (_| | | | |_) | | | (_| | |_| | (_) | | | |
 |____/ \__,_|\__|\__\___|_|   \__, |   \_____\__, |\___|_|\___|_|      \_____\__,_|_|_|_.__/|_|  \__,_|\__|_|\___/|_| |_|
                                __/ |          __/ |                                                                      
                               |___/          |___/                                                                       

                                                  Version 1.0
                                         Calibration for Battery Cycler                               
    """

    lines = intro_ascii.split("\n")
    padding = " " * 50

    for i in range(len(lines)):
        clear_terminal()
        print(padding + "\n".join(lines[:i]))
        time.sleep(0.1)
    time.sleep(3)
    clear_terminal()
    print(padding + intro_text)

def printProgressBar(iteration, total):
    fill = '█'
    decimals = 1
    prefix = 'Progress:'
    suffix = 'Complete'
    length = 50
    """
    Call in a loop to create terminal progress bar
    params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = "\r")
    # Print New Line on Complete
    if iteration == total: 
        print()