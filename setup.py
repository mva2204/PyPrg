# -*- coding: utf-8 -*-

import sys
from cx_Freeze import setup, Executable

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable('hello_world_qt.py', base=base)
]

setup(
    name = 'Text_bot_pyqt',
    version = '1.0',
    description = 'Text_bot_with_pyqt_interface',
    #Прописываем основной исполняемый файл
    executables = executables
)
