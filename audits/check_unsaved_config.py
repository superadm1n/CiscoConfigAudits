"""
MIT License

Copyright (c) 2018 Kyle Kowalczyk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Script that check if the running config has not been saved
"""
from datetime import datetime


def extract_date_from_config_string(configString):
    """Takes a string of a date as written in a Cisco configuration file and extracts the usable parts of it"""
    splitString = configString.split(' at ')[1].split(' by ')[0]
    dateEnd = ' '.join(splitString.split(' ')[2:])
    dateStart = ''.join(splitString.split(' ')[0])
    return ' '.join([dateStart, dateEnd])

def convert_timestring_to_datetime(timeString):
    """Takes a clean version of a config date from a cisco config file and converts it to a datetime object"""
    return datetime.strptime(timeString, '%H:%M:%S %a %b %d %Y')

def check_if_config_is_out_of_date():
    last_config_change = extract_date_from_config_string(cisco_cfg.find_objects(r'^!.* Last configuration change')[0].text)
    last_config_save = extract_date_from_config_string(cisco_cfg.find_objects(r'^!.* last updated')[0].text)
    if convert_timestring_to_datetime(last_config_change) > convert_timestring_to_datetime(last_config_save):
        return False
    else:
        return True


if __name__ == '__main__':
    import os
    import sys
    script_path = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(script_path)
    import base

    t = base.CLIApp()
    cisco_cfg = t.setUp()
    if check_if_config_is_out_of_date() is True:
        print('Configuration is saved!')
    else:
        print('Configuration is out of date!')
        exit(2)
