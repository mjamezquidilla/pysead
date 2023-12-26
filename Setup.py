import sys, os
from cx_Freeze import setup, Executable

# add files
files = []

# target
target = Executable(
    script="Truss2D_Main_UI.py",
    base="Win32GUI",
    target_name="Truss2D_Main.exe"
)

# setup cx_freeze
setup(
    name="Pysead Truss 2D",
    version="0.1.0",
    description="Python implementation of solving 2D trusses",
    options={'build_exe':{'include_files':files}},
    executables=[target]
)
