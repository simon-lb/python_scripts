# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 18:17:18 2021
@author: sgolan
"""

# **Hi User** !  This script performs the following:

# receives a list of linux servers, ssh to each one & retrieves a system info from each one of them and aggregates in one reporting file:
# Informatoin which will be retrieved : | hostname | System Time | num of CPUs | CPU models | NIC installed | drives installed |
# for running it, you have to provide a path for creating report, and a path where a hosts file is placed. 
# before running, make sure you have paramiko and argparse modules installed
# (pip3 install paramiko argparse)
# For running it, you'll have to provide a path to a hosts file, and the password for the root user. 
# Proper way of running this script:
# python system_info_light.py 'hosts_path.txt' 'admin'

import paramiko  # ssh library
import argparse  # argumets parsing library
import time
import os


# linux commands functions

def get_hostname(ssh):
    stdin, stdout, stderr = ssh.exec_command("hostname")  # execute the command hostname on the remote server
    cmd0 = stdout.readlines()  # return only the stdout
    cmd0 = "".join(cmd0)  # join output to make it clean and easy to read
    hostname = cmd0  # save value
    return hostname  # function to return the value


def get_cpu(ssh):
    stdin, stdout, stderr = ssh.exec_command("cat /proc/cpuinfo | grep 'model name' | sort -u")
    cmd1 = stdout.readlines()
    cmd1 = "".join(cmd1)
    cpu_model = cmd1
    return cpu_model


def get_cpu_count(ssh):
    stdin, stdout, stderr = ssh.exec_command("nproc")
    cmd2 = stdout.readlines()
    cmd2 = "".join(cmd2)
    cpu_num = cmd2
    return cpu_num


def get_nic(ssh):
    stdin, stdout, stderr = ssh.exec_command("lspci | grep -m 1 net ")
    cmd3 = stdout.readlines()
    cmd3 = "".join(cmd3)
    nic_name = cmd3
    return nic_name


def get_nvme_count(ssh):
    stdin, stdout, stderr = ssh.exec_command("lsblk | grep -o '^nvme' | wc -l")
    cmd4 = stdout.readlines()
    cmd4 = "".join(cmd4)
    nvme_count = cmd4
    return nvme_count


def get_time(ssh):
    stdin, stdout, stderr = ssh.exec_command("date")
    cmd5 = stdout.readlines()
    cmd5 = "".join(cmd5)
    date = cmd5
    return date


def main():
    # construct the argument parse and parse the arguments for:   hostspath | hostspassword
    parser = argparse.ArgumentParser()
    parser.add_argument("hostfile", help="Please Input the hosts file Path")
    parser.add_argument("hostspassword", help="Please Input the hosts password")
    args = parser.parse_args()
    # save hostfile as var
    hostfile = args.hostfile

    # display a friendly message to the user
    print("\n --> Location where System Report file will be created: " + str(os.getcwd()) + "\n" + '.' * 50 + "\n")
    time.sleep(3)
    print("\n --> Using hosts from provided hosts file: " + str(hostfile) + "\n" + '.' * 50 + "\n")
    time.sleep(3)

    # parse the hostfile from user, use it to open a file in read mode
    hosts_file = open(hostfile, 'r')

    # ssh connection crdentials

    port = 22
    username = "root"
    password = args.hostspassword

    # open a file in write mode, and keep it open while loop is running, to store all hosts data in same file
    with open("nodes_info.txt", 'w') as f:
        for host in hosts_file:
            host = host.strip()
            print("Checking Server: ", host)  # loop on each host in hosts file and print on which host code is running

            try:
                # create new ssh client
                print("Creating SSH client..")
                ssh = paramiko.SSHClient()
                # allow the Python script to SSH to a remote server with unknown SSH keys
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                print("Please wait, Connecting to remote server..")
                # connect the client to the server host:port with the credentials
                ssh.connect(host, port, username, password)

                print("Executing commands for host " + str(host) + " ==> ...Saving data to file...")

                # what will be written for each host to a created file
                f.write("SYSTEM INFO FOR HOST:\n" + str(get_hostname(ssh)) + "IP address: " + str(
                    host) + "\n" + "System Time: " + str(get_time(ssh)) + "\n\n" + "CPU Model: \n" +
                        str(get_cpu(ssh)) + "\n\n" + "Number of CPU's: \n" + str(get_cpu_count(ssh)) + "\n\n" +
                        "Installed NIC Driver:\n" + str(get_nic(ssh)) + "\n\n" +
                        "Total Number of NVME devices for node:\n" + str(get_nvme_count(ssh)) + "\n\n" "END OF REPORT FOR THIS HOST " + ' > '*30 + " NEXT HOST..." + "\n\n ")

                # print to console that file was created with file path
                print("System info for " + str(host) + " has been written to: " + str(f.name) + "\n")

                ssh.close()

            except:  # report to console unreachable hosts or other error
                print("ERROR!!: Could not establish connection with host or something else is wrong with host:  " + str(
                    host) + "\n")

    # close opened files
    hosts_file.close()


if __name__ == "__main__":
    main()
