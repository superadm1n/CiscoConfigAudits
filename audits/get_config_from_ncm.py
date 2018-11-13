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


This script will gather the configuration of a specified device stored in Solarwinds NCM server
"""

import argparse
import orionsdk
import requests

app = argparse.ArgumentParser()
app.add_argument('swserver', help="Hostname or IP Address of Solarwinds Server", type=str)
app.add_argument('username', help="Username to login to the Solarwinds Server", type=str)
app.add_argument('password', help="Password for User", type=str)
app.add_argument('nodename', help="Hostname of the device you want to get the configuration from", type=str)
app.add_argument("--print_hostname", help="Prints the hostname from the Cisco configuration.", action='store_true')
app.add_argument("--print_dltime", help="Prints the download time of the configuration.", action='store_true')
app.add_argument("--verify_ssl", help="Validate the SSL Cert of the Solarwinds server and warn if its not signed by a trusted authority.", action='store_true')
args = app.parse_args()

# Disables SSL validation of Solarwinds server unless explicitly specified by a CLI argument
if not args.verify_ssl:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

query = '''SELECT TOP 1 NODES.AgentIP as IP, NODES.SysName, NODES.NodeCaption, ARCHIVE.ConfigTitle, ARCHIVE.DownloadTime, 
ARCHIVE.AttemptedDownloadTime, ARCHIVE.ModifiedTime, ARCHIVE.ConfigType, ARCHIVE.Config
FROM NCM.ConfigArchive as ARCHIVE
JOIN NCM.Nodes as NODES on NODES.NodeID = ARCHIVE.NodeID
WHERE NODES.NodeCaption LIKE '%{}%'
AND ARCHIVE.ConfigType = 'Running'
ORDER BY ARCHIVE.DownloadTime DESC'''.format(args.nodename)

# logs into the server and executes query
swis = orionsdk.SwisClient(args.swserver, args.username, args.password)
query_results = swis.query(query)

# grabs data from query results
config = query_results['results'][0]['Config'].replace('\r\n', '\n')
hostname = query_results['results'][0]['NodeCaption']
download_time = query_results['results'][0]['DownloadTime']

# prints the config
print(config)

# if specified prints the hostname
if args.print_hostname:
    print(hostname)

# if specified prints the download time
if args.print_dltime:
    print(download_time.replace('T', ' '))
