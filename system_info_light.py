# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 18:17:18 2021

@author: sgolan
"""


# **Hi User** !  This script performs the following:

# receives a list of servers & retrieves a system info from each one of them and aggregates in one reporting file:
# Informatoin which will be retrieved : | hostname | System Time | num of CPUs | CPU models | NIC installed | drives installed |
# for running it, you have to provide a path for creating report, and a path where a hosts file is placed. 
# before running, make sure you have paramiko and argparse modules installed
#
# Proper way of running this script:
# python system_info_light.py "C:\\Users\\sgolan\\Desktop\\hosts_system_info_report.txt" "C:\\Users\\sgolan\\Desktop\\hosts_path.txt"

import paramiko # ssh library
import argparse # argumets parsing library
import time



#linux commands functions

def get_hostname(ssh):
    stdin, stdout, stderr = ssh.exec_command("hostname") #execute the command hostname on the remote server
    cmd0 = stdout.readlines() #return only the stdout
    cmd0 = "".join(cmd0)   #join output to make it clean and easy to read
    hostname = cmd0 #save value
    return hostname #function to return the value

def get_cpu(ssh):
    stdin, stdout, stderr = ssh.exec_command("cat /proc/cpuinfo | grep 'model name' | sort -u") # #execute the command to get cpu model on the remote server
    cmd1 = stdout.readlines() #return only the stdout
    cmd1 = "".join(cmd1) #join output to make it clean and easy to read
    cpu_model = cmd1 #save value
    return cpu_model  #function to return the value

def get_cpu_count(ssh): 
    stdin, stdout, stderr = ssh.exec_command("nproc") #execute the command to get num of cpu's on the remote server
    cmd2 = stdout.readlines() #return only the stdout
    cmd2 = "".join(cmd2) #join output to make it clean and easy to read
    cpu_num = cmd2 #save value
    return cpu_num #function to return the value

def get_nic(ssh):
    stdin, stdout, stderr = ssh.exec_command("lspci | grep -m 1 net ") #execute the command to get NIC model on the remote server
    cmd3 = stdout.readlines() #return only the stdout
    cmd3 = "".join(cmd3) #join output to make it clean and easy to read
    nic_name = cmd3 #save value
    return nic_name #function to return the value

def get_drivers(ssh):
    stdin, stdout, stderr = ssh.exec_command("lsmod") #execute the command to get drivers on the remote server
    cmd4 = stdout.readlines() #return only the stdout
    cmd4 = "".join(cmd4) #join output to make it clean and easy to read
    lsdrivers = cmd4 #save value
    return lsdrivers #function to return the value

def get_time(ssh):
    stdin, stdout, stderr = ssh.exec_command("date") #execute the command to get drivers on the remote server
    cmd5 = stdout.readlines() #return only the stdout
    cmd5 = "".join(cmd5) #join output to make it clean and easy to read
    date = cmd5 #save value
    return date #function to return the value

def main():

    # construct the argument parse and parse the arguments for reportpath and hostspath
    parser = argparse.ArgumentParser()
    parser.add_argument("reportpath", help = "Please Input the Report Path")
    parser.add_argument("hostspath", help = "Please Input the hosts file Path")
    args = parser.parse_args()
    # save 2 paths provided to use it later
    reportpath = args.reportpath
    hostspath = args.hostspath
    
    # display a friendly message to the user
    print("\n --> System Report will be created under: " +str(reportpath) + "\n..........................................................\n")
    time.sleep(3)
    print("\n --> Using hosts from provided hosts file: " + str(hostspath)+ "\n...........................................................\n")
    time.sleep(3)
    
    #parse the hostsfile from user, use it to open a file in read mode
    hosts_file = open(hostspath, 'r')
    
    #ssh connection crdentials
    
    port = 22
    username = "root"
    password = "customer"
    
    
    #loop on each host in hosts file and print on which host code is running 
    with open(reportpath, 'w') as f:
        for host in hosts_file:
                host = host.strip()
                print("Checking Server: ", host)
                
                try:
                    #create new ssh client
                    print ("Creating SSH client..")
                    ssh = paramiko.SSHClient()
                    #allow the Python script to SSH to a remote server with unknown SSH keys
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
                    print ("Please wait, Connecting to remote server..")
                    #connect the client to the server host:port with the credentials
                    ssh.connect(host, port, username, password)
        
                    print("Executing commands for host " + str(host) + " ==> ...Saving data to file...")
        
                    # what will be written for each host to a created file
    
    
                    #with open(reportpath, 'w') as f:
                    f.write("SYSTEM INFO FOR HOST:\n" + str(get_hostname(ssh)) + "IP address: " + str(host) + "\n" + "System Time: " + str(get_time(ssh)) + "\n\n" + "CPU Model: \n" +
                                      str(get_cpu(ssh)) + "\n\n" + "Number of CPU's: \n" + str(get_cpu_count(ssh)) + "\n\n" +
                                      "Installed NIC Driver:\n" + str(get_nic(ssh)) + "\n\n" +
                                      "Installed Drivers:\n" + str(get_drivers(ssh)) + "\n\n" + "END OF REPORT FOR THIS HOST>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>NEXT HOST...." +"\n\n")
                        
                    
                    #print to console that file was created with file path
                    print("System info for " + str(host) + " has been written to: " + str(f.name) + "\n")
                    
                    ssh.close()
                    
                except: #report to console unreacheable hosts or other error
                    print("ERROR: Could not establish connection with host or something else is wrong with host:  " + str(host) + "\n")
    
    
    
    #close opened files    
    hosts_file.close()


if __name__ == "__main__":
    main()

