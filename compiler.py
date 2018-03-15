# compiler

import py_compile as pc

filenames = ["LabourExport.py", "DBside.py"]
for file in filenames:
    pc.compile(file)
