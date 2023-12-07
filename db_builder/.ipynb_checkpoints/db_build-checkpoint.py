import subprocess
import datetime


def get_time():
    return datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")


def db_builder(file_name: str):
    command = f"pyinstaller --onefile --name {file_name}_{get_time()} db_create.py"
    subprocess.run(command, shell=True)


db_builder('TensionTerminator_DB_builder')
