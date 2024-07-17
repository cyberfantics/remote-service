# Remote Service Utility

## Overview

The Remote Service Utility is a Python script designed by Syed Mansoor ul Hassan Bukhari to enable administrative shares on a remote Windows computer, execute a specified script remotely, and manage network connections. This script leverages Python's **`winreg`** and **`os`** modules to interact with the Windows registry and manage network connections.

## Features

- **Enable Admin Share**: Modifies the registry on the remote computer to enable administrative shares.
- **Access Admin Share**: Copies a specified executable script to the administrative share (`C$` by default), executes it remotely, and then removes the network connection.
- **Administrative Privileges Check**: Ensures the script is run with administrative privileges (`IsUserAnAdmin()` function).
- **Logging**: Uses Python's `logging` module to record events and errors.

## Usage

### Prerequisites

- Python 3.x installed on the local machine.
- Administrative privileges on the local machine and remote computer.

### Setup

1. Clone the repository:
```bash
  git clone https://github.com/cyberfantics/remote-service.git
  cd remote-service
```
2. Run:
```bash
    python remote_service.py <remote_computer_name> <executable_script_name>
```

**Replace <remote_computer_name> with the name or IP address of the remote computer and <executable_script_name> with the name of the Python script to be executed remotely.**

## Notes
- Ensure both the local and remote machines are on the same network and accessible.
- Administrative privileges are required to modify the registry and manage network connections.

## Example
```bash
  python remote_service.py RemotePC my_script.py
```

