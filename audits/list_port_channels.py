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
        print('[FATAL]\nYou must either use this script in a pipeline or specify a configuration file to read!')
        exit(1)
    else:
        return [x.strip('\n') for x in sys.stdin.readlines()]


parser = argparse.ArgumentParser(prog="list_port_channels", description='Skel script to reference when creating other scripts.')
parser.add_argument("--config_file", help="File to read Cisco configuration from.", type=str)
parser.add_argument("--print_hostname", help="Prints the hostname from the Cisco configuration.", action='store_true')
args = parser.parse_args()

# Sets defaults for command line arguments for cli arguments if none were given
if not args.config_file:
    cisco_config = get_config()
else:
    cisco_config = args.config_file

try:
    cisco_cfg = CiscoConfParse(config=cisco_config)
    hostname = cisco_cfg.find_objects(r'^hostname')[0].text
except:
    print('[FATAL]\nThere was an issue with the supplied Cisco configuration, unable to parse!')
    exit(1)

if args.print_hostname:
    print(hostname)

# ==================================
def map_interfaces_to_ch_groups(cisco_cfg):
    '''Takes an parsed cisco config as input and returns a dictionary of all the port channels
    and the interfaces that belong to them'''
    correlated_channel_groups = {}
    for x in cisco_cfg.find_objects_w_child(r'^inter', r'channel-group'):
        ch_group = x.re_search_children(r'channel-group')[0].text.strip()
        if ch_group in correlated_channel_groups:
            correlated_channel_groups[ch_group].append(x.text)
        else:
            correlated_channel_groups[ch_group] = [x.text]
    return correlated_channel_groups

analyzed_results = map_interfaces_to_ch_groups(cisco_cfg)
for x in analyzed_results:
    print('{}: {}'.format(x, ', '.join(analyzed_results[x])))

