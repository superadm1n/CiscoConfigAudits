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


This script returns all of the interfaces that do not have a description tied to an interface that is not admin down
"""
import os
import sys
script_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_path)
import base

t = base.CLIApp(description='Lists all interfaces that are not admin down and are missing a description')
cisco_cfg = t.setUp()

def int_no_desc(parsed_config):
    '''Returns a list of config objects that do not have a description or shutdown as children'''
    rValue = []
    for obj in parsed_config.find_objects_wo_child(parentspec=r'^interf', childspec=r'desc'):
        if obj.has_child_with(r'shutdown$'):
            pass
        else:
            rValue.append(obj)
    return rValue

# Finds interfaces without a description and prints them if they are also missing a shutdown command
for interface in int_no_desc(cisco_cfg):
    print(interface.text)
