# aura-cleaner
Script that (hopefully) cleans up Asus AURA software leftovers in the registry and fixes it.  
**PROCEED AT YOUR OWN RISK/CAUTION**

## Description
ASUS's AURA software is notorious for breaking, and once it breaks, no one knows how to fix it, especially ASUS.  

I've noticed that you can't really uninstall 100% of it as most stuff that AURA installs is NOT listed in the Add/Remove Apps in  Control Panel of Windows.  

Having fought Armoury Crate and AURA for months now, nothing helped, so I decided to try and automate as much of the process as possible.  

What this script does - it scans the registry for AURA related entries, runs software uninstallation for them and removes the related registry keys.  

Notes:
- YMMV, this worked for **ME**.
- This **shouldn't** ruin your PC, or make the situation worse. **No guarantees**, though.
- This does **NOT** fix Armoury Crate. Fixed AURA for me.

## Requirements
- Windows 10
- Python 3
- Broken AURA

Tested on Windows 10 only, with AURA `1.07.79`

## Steps

1. Uninstall as much ASUS/AURA software through your Control Panel.
2. Reboot.
3. Delete everything from `C:\Program Files\ASUS`, `C:\Program Files (x86)\ASUS` and `C:\Program Files (x86)\LightingService`
4. If you can't delete something, use Task Manager to kill its process and then remove it.
5. Reboot.
6. Run `services.msc` and check for `LightningService`. If it's running, stop it, run `cmd` and run `SC DELETE LightingService`. Reboot.
6.1 You might also want to remove other ASUS services, like ROGLiveService. Not sure if this step is needed though.
7. Run the script. `python aura-cleaner.py`
8. Edit the output .BAT file to verify its contents.
9. Run the .BAT file as Admin.
10. Reboot.
11. Install AURA
