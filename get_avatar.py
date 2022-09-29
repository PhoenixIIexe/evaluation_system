import subprocess
import datetime


def get_avatar(date: datetime, gender: str):
    text = subprocess.check_output(
        f'D:\\GitHub\\evaluation_system\\RAM.exe {date} {gender}')
    decoded = text.decode('cp866')
    return decoded
