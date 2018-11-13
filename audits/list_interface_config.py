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


Script that lists the configuration for a specified interface
"""
import os
import sys
script_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_path)
import base

def parse_input(input):
    """Seperates the interface input from the user into the name and number ex.
    Gi1/0/1 becomes ('Gi', '1/0/1') or GigabitEthernet1/0/1 becomes ('GigabitEthernet', '1/0/1')"""
    interface_name = ''
    interface_number = ''
    x = 0
    for letter in input:
        if letter.isdigit():
            interface_number = input[x:]
            break
        else:
            interface_name += letter
        x += 1
    return interface_name, interface_number

app = base.CLIApp()
app.add_argument('interface', help='Interface to view the configuration of ex. gi1/0/1 or GigabitEthernet1/0/1', type=str)
cisco_cfg = app.setUp()

# parses the user input interface argument to be able to search
interface = parse_input(app.parsed_args.interface)

# grabs the interface config and prints it out to the user
interface_config = cisco_cfg.find_all_children(r'^interface.*{}.*{}$'.format(interface[0], interface[1]))
for line in interface_config:
    print(line)