# CiscoConfigAudits
Each of the files in this repository is a script that will preform a specific audit on the configuration 
from a Cisco device. These scripts are written in python and at this point leverage the CiscoConfParse 
library as a dependancy.


All of the scripts in this repository are created with the Unix philosophy in mind to do one thing 
and do it well, and work together well with other programs.


## Examples
List number of access ports on a switch:
```bash
cat config.txt | python list_access_ports.py | wc -l
```

Check if telnet is configured to listen on a Cisco device:
```bash
cat config.txt | python check_for_telnet.py
```

List out configured local users on a Cisco device
```bash
python list_local_users --config_file config.txt
```