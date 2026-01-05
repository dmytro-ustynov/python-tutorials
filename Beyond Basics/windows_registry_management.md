# Managing Windows Registry with Python

## Table of Contents
1. [Introduction](#introduction)
2. [Understanding the Windows Registry](#understanding-the-windows-registry)
3. [The winreg Module](#the-winreg-module)
4. [Reading from the Registry](#reading-from-the-registry)
5. [Writing to the Registry](#writing-to-the-registry)
6. [Practical Examples](#practical-examples)
7. [Best Practices and Safety](#best-practices-and-safety)

## Introduction

The Windows Registry is a hierarchical database that stores configuration settings and options for the Windows operating system and installed applications. Python provides the `winreg` module (built into the standard library) to interact with the Windows Registry programmatically.

**Important**: Registry modifications can affect system stability. Always:
- Create backups before making changes
- Test in a non-production environment
- Run with appropriate permissions
- Understand what you're modifying

## Understanding the Windows Registry

### Registry Structure

The registry is organized into a tree structure with the following components:

**Root Keys (Hives):**
- `HKEY_CLASSES_ROOT` (HKCR) - File associations and COM objects
- `HKEY_CURRENT_USER` (HKCU) - Current user settings
- `HKEY_LOCAL_MACHINE` (HKLM) - System-wide settings
- `HKEY_USERS` (HKU) - All user profiles
- `HKEY_CURRENT_CONFIG` (HKCC) - Current hardware profile

**Keys and Subkeys:** Similar to folders in a file system

**Values:** Data stored in keys, with different types:
- `REG_SZ` - String value
- `REG_DWORD` - 32-bit number
- `REG_QWORD` - 64-bit number
- `REG_BINARY` - Binary data
- `REG_MULTI_SZ` - Multiple strings
- `REG_EXPAND_SZ` - Expandable string (with environment variables)

## The winreg Module

### Basic Imports

```python
import winreg
import ctypes
import sys
```

### Checking Administrator Privileges

Many registry operations require administrator rights:

```python
def is_admin():
    """Check if script is running with admin privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("This script requires administrator privileges!")
    sys.exit(1)
```

## Reading from the Registry

### Opening a Registry Key

```python
import winreg

# Open a key for reading
key = winreg.OpenKey(
    winreg.HKEY_CURRENT_USER,           # Root key
    r"Software\Microsoft\Windows",       # Subkey path
    0,                                   # Reserved (always 0)
    winreg.KEY_READ                      # Access rights
)
```

### Reading a Specific Value

```python
def read_registry_value(root_key, subkey_path, value_name):
    """Read a specific value from the registry"""
    try:
        key = winreg.OpenKey(root_key, subkey_path, 0, winreg.KEY_READ)
        value, reg_type = winreg.QueryValueEx(key, value_name)
        winreg.CloseKey(key)
        
        return value, reg_type
    except FileNotFoundError:
        print(f"Key or value not found: {subkey_path}\\{value_name}")
        return None, None
    except PermissionError:
        print("Permission denied. Try running as administrator.")
        return None, None
```

### Enumerating All Values in a Key

```python
def enumerate_values(root_key, subkey_path):
    """List all values in a registry key"""
    try:
        key = winreg.OpenKey(root_key, subkey_path, 0, winreg.KEY_READ)
        
        # Get number of values
        num_values = winreg.QueryInfoKey(key)[1]
        
        print(f"Found {num_values} values in {subkey_path}:\n")
        
        for i in range(num_values):
            try:
                value_name, value_data, value_type = winreg.EnumValue(key, i)
                
                # Convert type code to readable name
                type_names = {
                    winreg.REG_SZ: "String",
                    winreg.REG_DWORD: "DWORD",
                    winreg.REG_BINARY: "Binary",
                    winreg.REG_MULTI_SZ: "Multi-String",
                    winreg.REG_EXPAND_SZ: "Expandable String"
                }
                type_name = type_names.get(value_type, f"Unknown ({value_type})")
                
                print(f"  {value_name}: {value_data} ({type_name})")
            except OSError:
                break
        
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Error: {e}")
```

### Enumerating Subkeys

```python
def enumerate_subkeys(root_key, subkey_path):
    """List all subkeys in a registry key"""
    try:
        key = winreg.OpenKey(root_key, subkey_path, 0, winreg.KEY_READ)
        
        # Get number of subkeys
        num_subkeys = winreg.QueryInfoKey(key)[0]
        
        print(f"Found {num_subkeys} subkeys in {subkey_path}:\n")
        
        for i in range(num_subkeys):
            try:
                subkey_name = winreg.EnumKey(key, i)
                print(f"  {subkey_name}")
            except OSError:
                break
        
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Error: {e}")
```

## Writing to the Registry

### Creating a Key and Setting Values

```python
def create_key_and_values():
    """Create a new registry key and set various value types"""
    try:
        # Create or open the key
        key = winreg.CreateKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\MyPythonApp"
        )
        
        # Set a string value
        winreg.SetValueEx(key, "AppName", 0, winreg.REG_SZ, "My Python Application")
        
        # Set a DWORD (integer) value
        winreg.SetValueEx(key, "Version", 0, winreg.REG_DWORD, 100)
        
        # Set a binary value
        binary_data = bytes([0x01, 0x02, 0x03, 0x04])
        winreg.SetValueEx(key, "BinaryData", 0, winreg.REG_BINARY, binary_data)
        
        # Set multiple strings
        multi_string = ["Option1", "Option2", "Option3"]
        winreg.SetValueEx(key, "Options", 0, winreg.REG_MULTI_SZ, multi_string)
        
        winreg.CloseKey(key)
        print("Registry key and values created successfully!")
        
    except PermissionError:
        print("Permission denied. Administrator privileges may be required.")
    except Exception as e:
        print(f"Error: {e}")
```

### Modifying Existing Values

```python
def modify_registry_value(root_key, subkey_path, value_name, new_value, value_type):
    """Modify an existing registry value"""
    try:
        key = winreg.OpenKey(root_key, subkey_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, value_name, 0, value_type, new_value)
        winreg.CloseKey(key)
        
        print(f"Successfully modified {value_name} to {new_value}")
        return True
    except Exception as e:
        print(f"Error modifying value: {e}")
        return False
```

### Deleting Values and Keys

```python
def delete_registry_value(root_key, subkey_path, value_name):
    """Delete a specific value from a registry key"""
    try:
        key = winreg.OpenKey(root_key, subkey_path, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, value_name)
        winreg.CloseKey(key)
        print(f"Successfully deleted value: {value_name}")
        return True
    except FileNotFoundError:
        print(f"Value not found: {value_name}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def delete_registry_key(root_key, subkey_path):
    """Delete a registry key (must be empty or use recursive delete)"""
    try:
        winreg.DeleteKey(root_key, subkey_path)
        print(f"Successfully deleted key: {subkey_path}")
        return True
    except OSError as e:
        if "access is denied" in str(e).lower():
            print("Permission denied. Run as administrator.")
        else:
            print(f"Error: Key might not be empty or doesn't exist. {e}")
        return False
```

### Recursive Key Deletion

```python
def delete_key_recursive(root_key, subkey_path):
    """Recursively delete a registry key and all its subkeys"""
    try:
        key = winreg.OpenKey(root_key, subkey_path, 0, winreg.KEY_READ)
        
        # Get all subkeys
        subkeys = []
        try:
            i = 0
            while True:
                subkeys.append(winreg.EnumKey(key, i))
                i += 1
        except OSError:
            pass
        
        winreg.CloseKey(key)
        
        # Recursively delete all subkeys
        for subkey in subkeys:
            delete_key_recursive(root_key, f"{subkey_path}\\{subkey}")
        
        # Now delete the key itself
        winreg.DeleteKey(root_key, subkey_path)
        print(f"Deleted: {subkey_path}")
        
    except Exception as e:
        print(f"Error deleting {subkey_path}: {e}")
```

## Practical Examples

### Example 1: Enable/Disable USB Storage Devices

This example shows how to control USB storage device access on Windows:

```python
import winreg
import ctypes
import sys

def is_admin():
    """Check if script has admin privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def set_usb_storage(enable=True):
    """Enable or disable USB storage devices"""
    reg_path = r"SYSTEM\CurrentControlSet\Services\USBSTOR"
    
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            reg_path,
            0,
            winreg.KEY_SET_VALUE
        )
        
        # 3 = Enable (Manual start), 4 = Disable
        value = 3 if enable else 4
        winreg.SetValueEx(key, "Start", 0, winreg.REG_DWORD, value)
        winreg.CloseKey(key)
        
        status = "enabled" if enable else "disabled"
        print(f"USB storage {status} successfully!")
        print("Note: Restart may be required for changes to take effect.")
        return True
        
    except PermissionError:
        print("Error: Administrator privileges required!")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_usb_storage_status():
    """Check current USB storage status"""
    reg_path = r"SYSTEM\CurrentControlSet\Services\USBSTOR"
    
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            reg_path,
            0,
            winreg.KEY_READ
        )
        
        value, _ = winreg.QueryValueEx(key, "Start")
        winreg.CloseKey(key)
        
        return "enabled" if value == 3 else "disabled"
    except Exception as e:
        print(f"Error: {e}")
        return None

# Usage
if __name__ == "__main__":
    if not is_admin():
        print("Please run as administrator!")
        sys.exit(1)
    
    print("Current status:", get_usb_storage_status())
    set_usb_storage(enable=False)  # Disable USB storage
```

### Example 2: Manage Application Settings

Store and retrieve application configuration:

```python
import winreg

class RegistryConfig:
    """Manage application settings in the registry"""
    
    def __init__(self, app_name):
        self.app_name = app_name
        self.reg_path = rf"Software\{app_name}"
        self.root_key = winreg.HKEY_CURRENT_USER
    
    def save_setting(self, key, value):
        """Save a setting to the registry"""
        try:
            reg_key = winreg.CreateKey(self.root_key, self.reg_path)
            
            # Determine value type
            if isinstance(value, int):
                winreg.SetValueEx(reg_key, key, 0, winreg.REG_DWORD, value)
            elif isinstance(value, str):
                winreg.SetValueEx(reg_key, key, 0, winreg.REG_SZ, value)
            elif isinstance(value, list):
                winreg.SetValueEx(reg_key, key, 0, winreg.REG_MULTI_SZ, value)
            else:
                raise ValueError(f"Unsupported value type: {type(value)}")
            
            winreg.CloseKey(reg_key)
            return True
        except Exception as e:
            print(f"Error saving setting: {e}")
            return False
    
    def get_setting(self, key, default=None):
        """Retrieve a setting from the registry"""
        try:
            reg_key = winreg.OpenKey(self.root_key, self.reg_path, 0, winreg.KEY_READ)
            value, _ = winreg.QueryValueEx(reg_key, key)
            winreg.CloseKey(reg_key)
            return value
        except FileNotFoundError:
            return default
        except Exception as e:
            print(f"Error reading setting: {e}")
            return default
    
    def delete_setting(self, key):
        """Delete a setting from the registry"""
        try:
            reg_key = winreg.OpenKey(self.root_key, self.reg_path, 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(reg_key, key)
            winreg.CloseKey(reg_key)
            return True
        except Exception as e:
            print(f"Error deleting setting: {e}")
            return False

# Usage example
config = RegistryConfig("MyAwesomeApp")

# Save settings
config.save_setting("WindowWidth", 1024)
config.save_setting("WindowHeight", 768)
config.save_setting("Theme", "dark")
config.save_setting("RecentFiles", ["file1.txt", "file2.txt", "file3.txt"])

# Retrieve settings
width = config.get_setting("WindowWidth", default=800)
theme = config.get_setting("Theme", default="light")
recent = config.get_setting("RecentFiles", default=[])

print(f"Width: {width}, Theme: {theme}, Recent: {recent}")
```

### Example 3: Backup and Restore Registry Keys

Create backups before making changes:

```python
import winreg
import json
from datetime import datetime

def backup_registry_key(root_key, subkey_path, backup_file):
    """Backup a registry key to a JSON file"""
    backup_data = {
        "timestamp": datetime.now().isoformat(),
        "root_key": str(root_key),
        "subkey_path": subkey_path,
        "values": {},
        "subkeys": []
    }
    
    try:
        key = winreg.OpenKey(root_key, subkey_path, 0, winreg.KEY_READ)
        
        # Backup values
        try:
            i = 0
            while True:
                name, value, value_type = winreg.EnumValue(key, i)
                # Convert binary data to hex string for JSON serialization
                if value_type == winreg.REG_BINARY:
                    value = value.hex()
                
                backup_data["values"][name] = {
                    "value": value,
                    "type": value_type
                }
                i += 1
        except OSError:
            pass
        
        # List subkeys
        try:
            i = 0
            while True:
                subkey_name = winreg.EnumKey(key, i)
                backup_data["subkeys"].append(subkey_name)
                i += 1
        except OSError:
            pass
        
        winreg.CloseKey(key)
        
        # Save to file
        with open(backup_file, 'w') as f:
            json.dump(backup_data, f, indent=2)
        
        print(f"Backup saved to {backup_file}")
        return True
        
    except Exception as e:
        print(f"Error backing up registry: {e}")
        return False

def restore_registry_key(root_key, backup_file):
    """Restore a registry key from backup"""
    try:
        with open(backup_file, 'r') as f:
            backup_data = json.load(f)
        
        subkey_path = backup_data["subkey_path"]
        key = winreg.CreateKey(root_key, subkey_path)
        
        # Restore values
        for name, data in backup_data["values"].items():
            value = data["value"]
            value_type = data["type"]
            
            # Convert hex string back to binary
            if value_type == winreg.REG_BINARY:
                value = bytes.fromhex(value)
            
            winreg.SetValueEx(key, name, 0, value_type, value)
        
        winreg.CloseKey(key)
        print(f"Registry restored from {backup_file}")
        return True
        
    except Exception as e:
        print(f"Error restoring registry: {e}")
        return False

# Usage
backup_registry_key(
    winreg.HKEY_CURRENT_USER,
    r"Software\MyApp",
    "myapp_backup.json"
)
```

### Example 4: Read System Information

Extract useful system information from the registry:

```python
import winreg

def get_windows_version():
    """Get Windows version information"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Windows NT\CurrentVersion",
            0,
            winreg.KEY_READ
        )
        
        product_name, _ = winreg.QueryValueEx(key, "ProductName")
        build_number, _ = winreg.QueryValueEx(key, "CurrentBuildNumber")
        
        try:
            display_version, _ = winreg.QueryValueEx(key, "DisplayVersion")
        except:
            display_version = "N/A"
        
        winreg.CloseKey(key)
        
        return {
            "ProductName": product_name,
            "BuildNumber": build_number,
            "DisplayVersion": display_version
        }
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_installed_programs():
    """Get list of installed programs"""
    programs = []
    
    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
    ]
    
    for reg_path in reg_paths:
        try:
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                reg_path,
                0,
                winreg.KEY_READ
            )
            
            i = 0
            while True:
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    
                    try:
                        name, _ = winreg.QueryValueEx(subkey, "DisplayName")
                        version, _ = winreg.QueryValueEx(subkey, "DisplayVersion")
                        programs.append({"name": name, "version": version})
                    except:
                        pass
                    
                    winreg.CloseKey(subkey)
                    i += 1
                except OSError:
                    break
            
            winreg.CloseKey(key)
        except Exception as e:
            continue
    
    return programs

# Usage
print("Windows Version:")
version_info = get_windows_version()
if version_info:
    for key, value in version_info.items():
        print(f"  {key}: {value}")

print("\nInstalled Programs (first 10):")
programs = get_installed_programs()
for program in programs[:10]:
    print(f"  {program['name']} - {program['version']}")
```

### Example 5: Monitor Registry Changes

Simple registry change detection:

```python
import winreg
import time

def get_registry_snapshot(root_key, subkey_path):
    """Get current state of registry key"""
    snapshot = {}
    
    try:
        key = winreg.OpenKey(root_key, subkey_path, 0, winreg.KEY_READ)
        
        i = 0
        while True:
            try:
                name, value, _ = winreg.EnumValue(key, i)
                snapshot[name] = value
                i += 1
            except OSError:
                break
        
        winreg.CloseKey(key)
    except Exception as e:
        print(f"Error: {e}")
    
    return snapshot

def monitor_registry_changes(root_key, subkey_path, interval=5):
    """Monitor registry key for changes"""
    print(f"Monitoring {subkey_path}...")
    print("Press Ctrl+C to stop\n")
    
    previous_snapshot = get_registry_snapshot(root_key, subkey_path)
    
    try:
        while True:
            time.sleep(interval)
            current_snapshot = get_registry_snapshot(root_key, subkey_path)
            
            # Check for changes
            for name, value in current_snapshot.items():
                if name not in previous_snapshot:
                    print(f"[NEW] {name} = {value}")
                elif previous_snapshot[name] != value:
                    print(f"[CHANGED] {name}")
                    print(f"  Old: {previous_snapshot[name]}")
                    print(f"  New: {value}")
            
            # Check for deleted values
            for name in previous_snapshot:
                if name not in current_snapshot:
                    print(f"[DELETED] {name} = {previous_snapshot[name]}")
            
            previous_snapshot = current_snapshot
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

# Usage
monitor_registry_changes(
    winreg.HKEY_CURRENT_USER,
    r"Software\Microsoft\Windows\CurrentVersion\Run",
    interval=5
)
```

### Example 6: Switch Between Normal and Safe Mode (Command Line)

This example demonstrates how to boot Windows into Safe Mode with Command Prompt only or return to normal mode:

```python
import winreg
import ctypes
import sys
import subprocess

def is_admin():
    """Check if script has admin privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_current_boot_mode():
    """Check current boot configuration"""
    reg_path = r"SYSTEM\CurrentControlSet\Control\SafeBoot\Option"
    
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            reg_path,
            0,
            winreg.KEY_READ
        )
        
        # If this key exists, we're in Safe Mode
        option_value, _ = winreg.QueryValueEx(key, "OptionValue")
        winreg.CloseKey(key)
        
        if option_value == 1:
            return "Safe Mode (Minimal)"
        elif option_value == 2:
            return "Safe Mode (Network)"
        else:
            return "Safe Mode (Unknown)"
            
    except FileNotFoundError:
        # Key doesn't exist - we're in normal mode
        return "Normal Mode"
    except Exception as e:
        return f"Unknown (Error: {e})"

def set_safeboot_minimal():
    """Configure next boot to Safe Mode with Command Prompt"""
    try:
        # Use bcdedit to set safe mode
        # This is safer than direct registry manipulation for boot config
        result = subprocess.run(
            ['bcdedit', '/set', '{current}', 'safeboot', 'minimal'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            # Also set to boot to command prompt
            subprocess.run(
                ['bcdedit', '/set', '{current}', 'safebootalternateshell', 'yes'],
                capture_output=True,
                text=True
            )
            print("✓ System configured for Safe Mode with Command Prompt")
            print("  The system will boot to Safe Mode on next restart.")
            return True
        else:
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error configuring safe boot: {e}")
        return False

def set_normal_boot():
    """Configure next boot to Normal Mode"""
    try:
        # Remove safe boot setting
        result = subprocess.run(
            ['bcdedit', '/deletevalue', '{current}', 'safeboot'],
            capture_output=True,
            text=True
        )
        
        # Remove alternate shell setting
        subprocess.run(
            ['bcdedit', '/deletevalue', '{current}', 'safebootalternateshell'],
            capture_output=True,
            text=True
        )
        
        print("✓ System configured for Normal Mode")
        print("  The system will boot normally on next restart.")
        return True
        
    except Exception as e:
        print(f"Error configuring normal boot: {e}")
        return False

def restart_computer(countdown=10):
    """Restart the computer with countdown"""
    print(f"\n⚠ System will restart in {countdown} seconds...")
    print("Press Ctrl+C to cancel\n")
    
    try:
        import time
        for i in range(countdown, 0, -1):
            print(f"Restarting in {i} seconds...", end='\r')
            time.sleep(1)
        
        print("\nRestarting now...                    ")
        subprocess.run(['shutdown', '/r', '/t', '0'])
        
    except KeyboardInterrupt:
        print("\n\nRestart cancelled by user.")
        return False
    
    return True

def main():
    """Main program for boot mode management"""
    if not is_admin():
        print("=" * 60)
        print("ERROR: Administrator privileges required!")
        print("=" * 60)
        print("\nThis script must be run as administrator to modify boot settings.")
        print("Please right-click and select 'Run as administrator'")
        sys.exit(1)
    
    print("=" * 60)
    print("Windows Boot Mode Manager")
    print("=" * 60)
    
    # Show current boot mode
    current_mode = get_current_boot_mode()
    print(f"\nCurrent Boot Mode: {current_mode}")
    
    print("\nOptions:")
    print("1. Switch to Safe Mode with Command Prompt (next boot)")
    print("2. Switch to Normal Mode (next boot)")
    print("3. Check current boot mode only")
    print("4. Exit without changes")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        print("\n" + "=" * 60)
        print("CONFIGURING SAFE MODE WITH COMMAND PROMPT")
        print("=" * 60)
        
        if set_safeboot_minimal():
            print("\n⚠ IMPORTANT NOTES:")
            print("  • Safe Mode will load minimal drivers only")
            print("  • You'll boot to Command Prompt interface")
            print("  • Network drivers will NOT be loaded")
            print("  • Run this script again in Safe Mode to return to normal")
            
            restart_choice = input("\nRestart now? (y/n): ").strip().lower()
            if restart_choice == 'y':
                restart_computer()
            else:
                print("\nBoot configuration changed. Restart manually when ready.")
    
    elif choice == "2":
        print("\n" + "=" * 60)
        print("CONFIGURING NORMAL BOOT MODE")
        print("=" * 60)
        
        if set_normal_boot():
            restart_choice = input("\nRestart now? (y/n): ").strip().lower()
            if restart_choice == 'y':
                restart_computer()
            else:
                print("\nBoot configuration changed. Restart manually when ready.")
    
    elif choice == "3":
        print(f"\nCurrent mode: {current_mode}")
        print("No changes made.")
    
    elif choice == "4":
        print("\nExiting without changes.")
    
    else:
        print("\n❌ Invalid choice!")

if __name__ == "__main__":
    main()
```

**Alternative Method: Direct Registry Manipulation**

While `bcdedit` is safer, here's how to do it via direct registry manipulation:

```python
def set_safeboot_registry_method():
    """Set Safe Mode using direct registry manipulation (alternative method)"""
    try:
        # Create/Open SafeBoot key
        safeboot_key = winreg.CreateKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\SafeBoot"
        )
        
        # Set minimal safe boot
        winreg.SetValueEx(safeboot_key, "OptionValue", 0, winreg.REG_DWORD, 1)
        
        # Create Option subkey
        option_key = winreg.CreateKey(safeboot_key, "Option")
        winreg.SetValueEx(option_key, "OptionValue", 0, winreg.REG_DWORD, 1)
        
        winreg.CloseKey(option_key)
        winreg.CloseKey(safeboot_key)
        
        # Enable command prompt (alternate shell)
        system_key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\SafeBoot",
            0,
            winreg.KEY_SET_VALUE
        )
        
        winreg.SetValueEx(
            system_key,
            "AlternateShell",
            0,
            winreg.REG_SZ,
            "cmd.exe"
        )
        
        winreg.CloseKey(system_key)
        
        print("Safe Mode configured via registry")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def remove_safeboot_registry_method():
    """Remove Safe Mode using registry manipulation"""
    try:
        # Delete SafeBoot key
        winreg.DeleteKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\SafeBoot\Option"
        )
        
        # Open SafeBoot key and remove values
        safeboot_key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\SafeBoot",
            0,
            winreg.KEY_SET_VALUE
        )
        
        try:
            winreg.DeleteValue(safeboot_key, "OptionValue")
        except:
            pass
        
        try:
            winreg.DeleteValue(safeboot_key, "AlternateShell")
        except:
            pass
        
        winreg.CloseKey(safeboot_key)
        
        print("Normal boot mode configured via registry")
        return True
        
    except Exception as e:
        print(f"Note: {e}")
        # Not necessarily an error - keys might not exist
        return True
```

**Usage Scenario: System Recovery**

This is particularly useful for:

```python
def emergency_recovery_mode():
    """Quick switch to safe mode for troubleshooting"""
    print("Emergency Recovery Mode")
    print("-" * 40)
    
    if not is_admin():
        print("Need admin rights!")
        return
    
    print("This will:")
    print("1. Boot to Safe Mode with Command Prompt")
    print("2. Restart the computer")
    print("3. You can run diagnostics and repairs")
    print("4. Run this script again to return to normal")
    
    confirm = input("\nProceed? (yes/no): ").strip().lower()
    
    if confirm == 'yes':
        if set_safeboot_minimal():
            print("\n✓ Recovery mode will start on next boot")
            restart_computer(countdown=15)
    else:
        print("Cancelled.")

# Usage
# emergency_recovery_mode()
```

**Important Notes:**

1. **bcdedit Method (Recommended)**:
   - Safer and more reliable
   - Properly handles boot configuration
   - Less likely to cause boot issues

2. **Registry Method (Use with Caution)**:
   - Direct manipulation of boot settings
   - Requires deep understanding of boot process
   - Can cause boot failures if done incorrectly

3. **Safe Mode Command Prompt**:
   - Loads minimal drivers only
   - No GUI, command line interface only
   - Useful for troubleshooting when GUI won't load
   - Run the script again in Safe Mode to return to normal

4. **Recovery**:
   - If stuck in Safe Mode, boot from Windows installation media
   - Use command prompt: `bcdedit /deletevalue {current} safeboot`
   - Or run this script from Safe Mode to switch back

⚠️ **WARNING**: Incorrect boot configuration can prevent Windows from starting. Always ensure you have a recovery method available (installation media, recovery partition, etc.) before modifying boot settings.

## Best Practices and Safety

### 1. Always Check Permissions

```python
import ctypes

def require_admin():
    """Ensure script is running with admin privileges"""
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("This operation requires administrator privileges!")
        print("Please run the script as administrator.")
        sys.exit(1)
```

### 2. Use Context Managers

```python
from contextlib import contextmanager

@contextmanager
def open_registry_key(root_key, subkey_path, access=winreg.KEY_READ):
    """Context manager for registry keys"""
    key = None
    try:
        key = winreg.OpenKey(root_key, subkey_path, 0, access)
        yield key
    finally:
        if key:
            winreg.CloseKey(key)

# Usage
with open_registry_key(winreg.HKEY_CURRENT_USER, r"Software\MyApp") as key:
    value, _ = winreg.QueryValueEx(key, "Setting")
    print(value)
```

### 3. Create Backups Before Modifications

```python
def safe_registry_modification(root_key, subkey_path, modifications_func):
    """Safely modify registry with automatic backup"""
    import tempfile
    import os
    
    # Create backup
    backup_file = os.path.join(tempfile.gettempdir(), "registry_backup.json")
    
    if backup_registry_key(root_key, subkey_path, backup_file):
        try:
            # Perform modifications
            modifications_func()
            print("Modifications completed successfully!")
        except Exception as e:
            print(f"Error during modification: {e}")
            print("Restoring from backup...")
            restore_registry_key(root_key, backup_file)
    else:
        print("Backup failed! Aborting modifications.")
```

### 4. Handle Errors Gracefully

```python
def safe_read_value(root_key, subkey_path, value_name, default=None):
    """Safely read a registry value with error handling"""
    try:
        key = winreg.OpenKey(root_key, subkey_path, 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, value_name)
        winreg.CloseKey(key)
        return value
    except FileNotFoundError:
        return default
    except PermissionError:
        print(f"Permission denied accessing {subkey_path}")
        return default
    except Exception as e:
        print(f"Unexpected error: {e}")
        return default
```

### 5. Validate Input Data

```python
def validate_registry_value(value, expected_type):
    """Validate value before writing to registry"""
    if expected_type == winreg.REG_DWORD:
        if not isinstance(value, int):
            raise ValueError("DWORD values must be integers")
        if value < 0 or value > 0xFFFFFFFF:
            raise ValueError("DWORD must be between 0 and 4294967295")
    
    elif expected_type == winreg.REG_SZ:
        if not isinstance(value, str):
            raise ValueError("REG_SZ values must be strings")
    
    elif expected_type == winreg.REG_MULTI_SZ:
        if not isinstance(value, list):
            raise ValueError("REG_MULTI_SZ values must be lists")
        if not all(isinstance(item, str) for item in value):
            raise ValueError("REG_MULTI_SZ must contain only strings")
    
    return True
```

### 6. Use Descriptive Error Messages

```python
def write_registry_value_safe(root_key, subkey_path, value_name, value, value_type):
    """Write registry value with detailed error reporting"""
    try:
        # Validate input
        validate_registry_value(value, value_type)
        
        # Attempt to write
        key = winreg.OpenKey(root_key, subkey_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, value_name, 0, value_type, value)
        winreg.CloseKey(key)
        
        print(f"Successfully wrote '{value_name}' = {value}")
        return True
        
    except ValueError as e:
        print(f"Validation error: {e}")
        return False
    except PermissionError:
        print(f"Permission denied. Administrator rights may be required.")
        print(f"Attempted to write to: {subkey_path}\\{value_name}")
        return False
    except FileNotFoundError:
        print(f"Registry path not found: {subkey_path}")
        print("The key may need to be created first.")
        return False
    except Exception as e:
        print(f"Unexpected error writing to registry:")
        print(f"  Path: {subkey_path}")
        print(f"  Value: {value_name}")
        print(f"  Error: {e}")
        return False
```

### Important Safety Guidelines

1. **Test in Safe Environment**: Always test registry modifications in a VM or test system first

2. **Backup Critical Keys**: Before modifying system keys, create a System Restore point or registry backup

3. **Use HKEY_CURRENT_USER When Possible**: Modifications to HKCU are less risky than HKLM

4. **Avoid Critical System Keys**: Never modify keys you don't understand, especially in:
   - `HKLM\SYSTEM`
   - `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run`
   - Boot configuration keys

5. **Check Before Deleting**: Deleting the wrong registry key can make Windows unbootable

6. **Document Your Changes**: Keep a log of what was modified and why

7. **Handle 32-bit vs 64-bit**: On 64-bit Windows, be aware of registry redirection:

```python
# Access 64-bit registry view
key = winreg.OpenKey(
    winreg.HKEY_LOCAL_MACHINE,
    r"SOFTWARE\MyApp",
    0,
    winreg.KEY_READ | winreg.KEY_WOW64_64KEY
)

# Access 32-bit registry view
key = winreg.OpenKey(
    winreg.HKEY_LOCAL_MACHINE,
    r"SOFTWARE\MyApp",
    0,
    winreg.KEY_READ | winreg.KEY_WOW64_32KEY
)
```

### Common Access Rights

```python
# Common access right combinations
READ_ONLY = winreg.KEY_READ
WRITE_ONLY = winreg.KEY_WRITE
FULL_ACCESS = winreg.KEY_ALL_ACCESS
READ_WRITE = winreg.KEY_READ | winreg.KEY_WRITE

# 64-bit specific
READ_64BIT = winreg.KEY_READ | winreg.KEY_WOW64_64KEY
WRITE_64BIT = winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY
```

## Troubleshooting

### Common Issues and Solutions

**Issue**: `PermissionError: [WinError 5] Access is denied`
- **Solution**: Run script as administrator or use HKEY_CURRENT_USER instead of HKEY_LOCAL_MACHINE

**Issue**: `FileNotFoundError: [WinError 2] The system cannot find the file specified`
- **Solution**: Check if the registry key path exists, use `CreateKey` instead of `OpenKey`

**Issue**: `OSError: [WinError 1010] The configuration registry key is invalid`
- **Solution**: The key might not be empty when trying to delete, use recursive deletion

**Issue**: Changes don't take effect
- **Solution**: Some registry changes require:
  - Restarting the application
  - Logging out and back in
  - Rebooting the system
  - Broadcasting a `WM_SETTINGCHANGE` message

### Broadcasting Registry Changes

Some applications need to be notified of registry changes:

```python
import win32api
import win32con

def notify_registry_change():
    """Notify applications of registry changes"""
    win32api.SendMessage(
        win32con.HWND_BROADCAST,
        win32con.WM_SETTINGCHANGE,
        0,
        "Environment"
    )
```

## Summary

Key takeaways for managing the Windows Registry with Python:

1. **Use the `winreg` module** - It's part of the standard library and provides full registry access

2. **Always check permissions** - Many operations require administrator rights

3. **Create backups** - Before modifying important keys, always backup

4. **Handle errors gracefully** - Registry operations can fail for many reasons

5. **Test carefully** - Registry mistakes can break your system

6. **Use appropriate root keys**:
   - `HKEY_CURRENT_USER` for user-specific settings (safer)
   - `HKEY_LOCAL_MACHINE` for system-wide settings (requires admin)

7. **Close keys properly** - Always close registry keys after use or use context managers

8. **Validate input** - Check data types and ranges before writing to registry


## Additional Resources

- [Microsoft Registry Documentation](https://docs.microsoft.com/en-us/windows/win32/sysinfo/registry)
- [Python winreg Documentation](https://docs.python.org/3/library/winreg.html)
- [Registry Data Types](https://docs.microsoft.com/en-us/windows/win32/sysinfo/registry-value-types)
- [Windows Registry Best Practices](https://docs.microsoft.com/en-us/windows/win32/sysinfo/registry-best-practices)

## Warning

⚠️ **IMPORTANT**: Incorrect registry modifications can cause serious system problems. Always:
- Understand what you're changing
- Create backups before modifications
- Test in a safe environment first
- Have a recovery plan ready
- Never modify registry keys you don't understand

When in doubt, don't make the change without proper research and testing!

---

*This tutorial covers the essentials of Windows Registry management with Python. For production use, always implement comprehensive error handling, logging, and backup mechanisms.*
