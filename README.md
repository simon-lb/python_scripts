# flygiraffe
My code portfolio
# **Hi User** !  This script performs the following:

# receives a list of servers & retrieves a system info from each one of them and aggregates in one reporting file:
# Informatoin which will be retrieved : | hostname | System Time | num of CPUs | CPU models | NIC installed | drives installed |
# for running it, you have to provide a path for creating report, and a path where a hosts file is placed. 
# before running, make sure you have paramiko and argparse modules installed
#
# Proper way of running this script:
# python system_info_light.py "C:\\Users\\sgolan\\Desktop\\hosts_system_info_report.txt" "C:\\Users\\sgolan\\Desktop\\hosts_path.txt"
