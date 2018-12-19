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


Script to remove monitor session from a device as specified by user
"""
import argparse
from getpass import getpass
from CiscoAutomationFramework import connect_ssh

app = argparse.ArgumentParser()
app.add_argument('CiscoIP', help='IP Address of cisco device to remove config from', type=str)
app.add_argument('SessionID', help='Monitor Session ID', type=str)
app.add_argument('-u', '--username', help='Username to authenticate with', type=str)
app.add_argument('-p', '--password', help='Password to authenticate with', type=str)
app.add_argument('-ep', '--enablepassword', help='Enable password to use', type=str)
args = app.parse_args()

if not args.username:
    username = input('Enter username to authenticate with: ')
else:
    username = args.username

if not args.password:
    password = getpass('Enter Password: ')
else:
    password = args.password

if not args.enablepassword:
    enable_password = getpass('Enter enable password: ')
else:
    enable_password = args.enablepassword


print('[-] Logging in', end='\r')
try:
    ssh = connect_ssh(args.CiscoIP, username, password, enable_password)
except:
    print('Unable to Log into device!')
    exit(1)
print('[+] Successfully logged in!')

print('[-] Gathering Current Configuration', end='\r')
running_config = ssh.show_run()
print('[+] Configuration gathered successfully!')

print('The following lines of config will be removed:')
commands = []
for x in running_config.splitlines():
    if 'monitor session {}'.format(args.SessionID) in x:
        print(x)
        commands.append('no {}'.format(x))

answer = input('Are you sure you want to remove the lines of config listed above? [y/n] ')
if answer[0].upper() == 'Y':
    print('[-] Entering Config T', end='\r')
    ssh.config_t()
    print('[+] In Config T!             ')
    for x in commands:
        print(ssh.ssh.send_command_expect_same_prompt(x))
else:
     print('Not issuing commands!')

