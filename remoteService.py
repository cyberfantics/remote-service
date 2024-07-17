# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 20:41:27 2024

@author: Mansoor
"""

import os
import sys
import winreg
import shutil
import logging
from argparse import ArgumentParser
import ctypes

def enableAdminShare(computerName):
    """
    Enables administrative shares on the specified computer by setting the 
    LocalAccountTokenFilterPolicy registry value to 1.
    """
    try:
        regpath = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
        reg = winreg.ConnectRegistry(computerName, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(reg, regpath, 0, access=winreg.KEY_WRITE)
        
        # Backup the registry key before modifying
        backup_value = winreg.QueryValueEx(key, "LocalAccountTokenFilterPolicy")[0] if "LocalAccountTokenFilterPolicy" in [winreg.EnumValue(key, i)[0] for i in range(winreg.QueryInfoKey(key)[1])] else None
        
        winreg.SetValueEx(key, "LocalAccountTokenFilterPolicy", 0, winreg.REG_DWORD, 1)
        winreg.CloseKey(key)
        
        logging.info(f"Admin share enabled on {computerName}. A reboot is required.")
        
        return backup_value
    except Exception as e:
        logging.error(f"Failed to enable admin share: {e}")
        return None

def accessAdminShare(computerName, executable):
    """
    Accesses the administrative share on the specified computer, copies the 
    given executable (Python script), runs it, and then removes the network connection.
    """
    try:
        remote = r"\\{}\c$".format(computerName)
        local = "Z:"
        localfile = os.path.join(os.getcwd(), executable)
        remotefile = os.path.join(local, executable)
        
        # Map network drive
        os.system(f"net use {local} {remote}")
        
        # Move the file
        shutil.copy2(localfile, remotefile)
        
        # Execute the remote file
        os.system(f"python {remotefile}")
        
        # Disconnect network drive
        os.system(f"net use {local} /delete")
        
        logging.info(f"Executed {executable} on {computerName}.")
    except Exception as e:
        logging.error(f"Failed to access admin share: {e}")

def is_admin():
    """
    Check if the script is run with administrative privileges.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main(computerName, executable):
    if not is_admin():
        logging.error("This script requires administrative privileges to run.")
        sys.exit(1)

    backup_value = enableAdminShare(computerName)
    accessAdminShare(computerName, executable)
    
    # Optionally handle reboot (uncomment the lines below if you want to prompt for reboot)
    # if backup_value is None or backup_value != 1:
    #     logging.info("Rebooting system to apply changes...")
    #     os.system("shutdown /r /t 0")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    parser = ArgumentParser(description="Enable admin shares and run scripts remotely.")
    parser.add_argument("computer_name", type=str, help="The name of the remote computer.")
    parser.add_argument("executable_name", type=str, help="The name of the executable script to run on the remote computer.")
    
    args = parser.parse_args()
    
    main(args.computer_name, args.executable_name)
