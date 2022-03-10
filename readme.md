Created on Fri Jul  2 18:17:18 2021
@author: sgolan

# Hi User !  This script is performs the following:

- receives a list of linux servers, ssh to each one & retrieves a system info from each one of them and aggregates in one reporting file:
- Informatoin which will be retrieved : | hostname | System Time | num of CPUs | CPU models | NIC installed | drives installed |
- before running, make sure you have paramiko and argparse modules installed
- (pip3 install paramiko argparse)
- For running it, you'll have to provide a path to a hosts file, and the password for the root user. 
- Proper way of running this script:

#### `python3 system_info_light.py 'hosts_path.txt' 'admin'` 
