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

Script to login to Cisco device and grab the running config
"""

from CiscoAutomationFramework import connect_ssh
import argparse


parser = argparse.ArgumentParser(prog="get_running_config.py", description='Captures the running config from a Cisco device')
parser.add_argument("ipaddr", help="IP Address of device", type=str)
parser.add_argument("username", help="Username to login as", type=str)
parser.add_argument("password", help="Users Password", type=str)
parser.add_argument("enable_password", help="Enable Password", type=str)
args = parser.parse_args()

with connect_ssh(args.ipaddr, args.username, args.password, args.enable_password) as ssh:
    print(ssh.show_run())