import os
from winreg import EnumKey, EnumValue, QueryInfoKey, OpenKey, HKEY_CLASSES_ROOT, HKEY_LOCAL_MACHINE

def check_name(name):
    if 'ASUS' in name:
        return True
    if 'HAL' in name:
        return True
    if 'AURA' in name:
        return True
    if 'RGB' in name:
        return True
    if 'ENE' in name:
        return True
    return False

def collect_registry(hkey, root_key):
    things_to_remove = []
    with OpenKey(hkey, root_key) as depKey:
        dep_key_count = QueryInfoKey(depKey)[0]
        print('Found {0} keys'.format(dep_key_count))
        for i in range(0, dep_key_count):
            dep_key_str = EnumKey(depKey, i)
            if dep_key_str[0] == '{':
                with OpenKey(depKey, dep_key_str) as targetKey:
                    target_key_count = QueryInfoKey(targetKey)[1]
                    for j in range(0, target_key_count):
                        key_value = EnumValue(targetKey, j)
                        if key_value[0] == 'DisplayName':
                            installer_name = key_value[1]
                            if check_name(installer_name):
                                things_to_remove.append((
                                    installer_name, dep_key_str
                                ))
    return things_to_remove

def generate_bat(commands):
    try:
        os.remove('aura_clean.bat')
    except:
        pass
    batfile = open('aura_clean.bat', 'x')
    batfile.write('\n'.join(commands))
    batfile.close()

def main():
    print('This script will generate a .BAT file that should uninstall and cleanup registry after AURA.')
    batfile_commands = [
        '@echo on',
        'echo This script will remove AURA leftovers (hopefully).',
        'echo Clean up as much as you can using the Control Panel first!',
        'echo Remember to Run As Admin. THIS CANNOT REVERTED.',
        'pause',
        ''
    ]
    print('Collecting Installer\\Dependencies...')
    batfile_commands.append('echo Uninstalling dependencies...')
    batfile_commands.append('')
    dependencies_to_remove = collect_registry(HKEY_CLASSES_ROOT, '\\Installer\\Dependencies\\')
    print('Generating commands...')
    for software in dependencies_to_remove:
        batfile_commands.append("echo Uninstalling {} ({})".format(software[0], software[1]))
        batfile_commands.append("C:\WINDOWS\system32\msiexec.exe /quiet /x {}".format(software[1]))
        batfile_commands.append('')
        batfile_commands.append("echo Removing related registry key ...")
        batfile_commands.append('reg delete \"HKEY_CLASSES_ROOT\\Installer\\Dependencies\\{}" /f'.format(software[1]))
        batfile_commands.append('')
    print('Done.')

    print('Collecting Uninstallers...')
    uninstallers_to_remove = collect_registry(HKEY_LOCAL_MACHINE,
                                        'SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\')
    print('Generating commands...')
    batfile_commands.append('echo Cleaning up uninstallers...')
    batfile_commands.append('')
    for software in uninstallers_to_remove:
        batfile_commands.append("echo Uninstalling {} ({})".format(software[0], software[1]))
        batfile_commands.append("C:\WINDOWS\system32\msiexec.exe /quiet /x {}".format(software[1]))
        batfile_commands.append('')
        batfile_commands.append("echo Removing related registry key ...")
        batfile_commands.append('reg delete \"HKEY_LOCAL_MACHINE\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{}" /f'.format(software[1]))
        batfile_commands.append('')
    print('Done.')

    batfile_commands.append('echo Done. Reboot your system.')
    batfile_commands.append('pause')

    generate_bat(batfile_commands)

    print('Done.')
    print('File generated.')
    print('REMEMBER: Double check it\'s contents before running it - make sure it\'s not removing something important.')

main()
