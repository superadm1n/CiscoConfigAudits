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


Script to list the monitoring sessions configured on the Cisco device
"""
import os
import sys
script_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_path)
import base

def check_list_for_session(list_of_dicts, session_id):
    '''
    Checks if a session is already listed in a dictionary

    :param list_of_dicts: {'id': 1, 'source': 'addr', 'destination': 'addr'}, etc]
    :param session_number: Session ID you are looking for
    :return: True/False
    '''
    if len([item for item in list_of_dicts if item["id"] == session_id]) == 0:
        return False
    else:
        return True

def parse_monitor_session_text(monitor_sessions):
    organized_sessions = []
    for x in monitor_sessions:
        ses_id = x.text.split()[2]
        source_dest = x.text.split()[3]
        interface = x.text.split()[-1]
        if check_list_for_session(organized_sessions, ses_id) is True:
            for y in organized_sessions:
                if y['id'] == ses_id:
                    y[source_dest] = interface
        else:
            organized_sessions.append({'id': ses_id, source_dest: interface})
    return organized_sessions

t = base.CLIApp()
cisco_cfg = t.setUp()

# Gets config lines for the port monitor sessions
monitor_sessions = cisco_cfg.find_objects(r'^monitor session')
# organizes raw config text into dictionary
sessions = parse_monitor_session_text(monitor_sessions)
# organizes the dictionary into a list of lists that can be printed out in columns
printable_list = [[x['id'], x['source'], x['destination']] for x in sessions]
# Adds a header for the list
printable_list.insert(0, ['Session #', 'Source Port', 'Destination Port'])

# prints the data to the user
col_width = max(len(word) for row in printable_list for word in row) + 2  # padding
for row in printable_list:
    print("".join(word.ljust(col_width) for word in row))
