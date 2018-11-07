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
import os
import sys
script_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_path)
import base

t = base.Base()
cisco_cfg = t.setUp()


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

def clean_port_channel_text(text):
    return ' '.join(text.split(' ')[:2]).replace('channel-group', 'port channel')


analyzed_results = map_interfaces_to_ch_groups(cisco_cfg)
for x in analyzed_results:
    print('{}: {}'.format(clean_port_channel_text(x), ', '.join(analyzed_results[x])))

