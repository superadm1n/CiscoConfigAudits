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
"""

import argparse
from ciscoconfparse import CiscoConfParse
import sys
import orionsdk


class CLIApp(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parsed_args = None
        self.raw_config = None
        if not self.prog:
            self.prog = 'Base Name'
        if not self.description:
            self.description = 'Base Description'
        self.add_argument("--config_file", help="File to read Cisco configuration from.", type=str)
        self.add_argument("--print_hostname", help="Prints the hostname from the Cisco configuration.", action='store_true')

    def get_config(self):
        '''checks if the program was run in a pipeline and if so it will use the data from the pipe as the config file else it will
        set the config file location to the default config.txt'''
        if sys.stdin.isatty():
            print('[FATAL]\nYou must either use this script in a pipeline or specify a configuration file to read!')
            exit(1)
        else:
            return [x.strip('\n') for x in sys.stdin.readlines()]

    def setUp(self):
        '''Parses the arguments that have been supplied to the class, parses supplied cisco configuration
        and returns that object

        :return:
        '''
        args = self.parse_args()
        self.parsed_args = args
        # Sets defaults for command line arguments for cli arguments if none were given
        if not args.config_file:
            cisco_config = self.get_config()
        else:
            cisco_config = args.config_file
        self.raw_config = cisco_config
        try:
            cisco_cfg = CiscoConfParse(config=cisco_config)
            hostname = cisco_cfg.find_objects(r'^hostname')[0].text
        except:
            print('[FATAL]\nThere was an issue with the supplied Cisco configuration, unable to parse!')
            exit(1)

        if args.print_hostname:
            print(hostname)

        return cisco_cfg

def query_solarwinds(server, username, password, query):
    # logs into the server and executes query
    swis = orionsdk.SwisClient(server, username, password)
    return swis.query(query)