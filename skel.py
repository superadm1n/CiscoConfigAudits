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


This is a skeleton script that will by default accept a config file for a cisco config or accept config from
stdin via a pipeline. To add to this script simply append to the bottom of this file and/or add arguments to the parser section
"""
from ciscoconfparse import CiscoConfParse
import argparse
import os
import sys

# gets the absolute path on the file system of this file
script_path = os.path.dirname(os.path.abspath(__file__))


def get_config():
    '''checks if the program was run in a pipeline and if so it will use the data from the pipe as the config file else it will
    set the config file location to the default config.txt'''
    if sys.stdin.isatty():
        return os.path.join(script_path, 'config.txt')
    else:
        return [x.strip('\n') for x in sys.stdin.readlines()]


parser = argparse.ArgumentParser("active_interfaces_wo_descriptions")
parser.add_argument("--config_file", help="Cisco configuration file to read from (Default: config.txt)", type=str)
args = parser.parse_args()

# Sets defaults for command line arguments for cli arguments if none were given
if not args.config_file:
    cisco_config = get_config()
else:
    cisco_config = args.config_file

try:
    cisco_cfg = CiscoConfParse(config=cisco_config)
    print(cisco_cfg.find_objects(r'^hostname')[0].text)
except:
    print('[FATAL]\nThere was an issue with the supplied Cisco configuration, unable to parse!')
    exit(1)
