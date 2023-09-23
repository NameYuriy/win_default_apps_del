import subprocess
import os
from pathlib import Path


TMP_DIRECTORY = Path(Path.cwd(), 'temp')


def get_apps_txt():
    """Функция получения списка комманд и записи в фаил."""
    COMMAND = r'Get-AppxPackage | select Name'
    process = subprocess.Popen(['powershell.exe', COMMAND],
                               stdout=subprocess.PIPE, text=True)
    output = str(process.stdout.read())
    apps_list = open(r'./temp/installed_apps.txt', 'w')
    apps_list.write(output)

    apps_list.close()


def get_apps():
    """Возвращает список из приложений."""
    get_apps_txt()
    apps = []
    new_file = open(r'./temp/apps_without_rubbish.txt', 'a', encoding='UTF-8')
    with open(r'./temp/installed_apps.txt', 'r') as file:
        for fullname in file:
            app = fullname.strip()
            exceptions = ['Name', '----', '']
            if app not in exceptions:
                apps.append(app.strip().replace('Microsoft.', '').
                            replace('MicrosoftWindows.', ''))
                new_file.write(app + '\n')
    new_file.close()
    os.remove(r'./temp/installed_apps.txt')
    return apps


def run_powershell(app_name):
    command = f'Get-AppxPackage *{app_name}* | Remove-AppxPackage'
    process = subprocess.Popen(['powershell.exe', command],
                               stdout=subprocess.PIPE, text=True)
    with open(r'./logs.txt', 'a', encoding='UTF-8') as logs:
        log = str(process.stdout.read())
        if log == '':
            log = 'Done!'
            logs.write(f'{app_name}\n{log}\n')
            return True
        else:
            logs.write(f'{app_name}\n{log}\n')
            return False


def delete_temp():
    for file in TMP_DIRECTORY.iterdir():
        os.remove(file)
