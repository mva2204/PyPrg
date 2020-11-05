# -*- coding: utf-8 -*-

import sys
from cx_Freeze import setup, Executable

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Dependencies are automatically detected, but it might need fine tuning.
# build_exe_options = {"includes": ["validate_email"], "excludes": ["PyQt5"]}

executables = [
    Executable('Matplotlib_grphics_in_qt5.py', base=base)
]

setup(
    name = 'Text_bot_pyqt',
    version = '1.0',
    description = 'Text_bot_with_pyqt_interface',
    # options={"build_exe": build_exe_options},
    #Прописываем основной исполняемый файл
    executables = executables
)
