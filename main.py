#!/usr/bin/env python3
#File called main.py
import sys
print("\n Imported sys\n")
import os
print("\n Imported os\n")
import shutil
print("\n Imported shutiln\n")

#Import edirect module
sys.path.insert(1, os.path.dirname(shutil.which('xtract')))
import edirect
print("\n Imported edirect\n")
import subprocess
print("\n Imported subprocess\n")
import re

from PIL import Image
print("\n Imported Image\n")
from os.path import exists # Check if the file exists
print("\n Imported exists from os.path\n")
import pandas as pd
print("\n Imported pandas as pd \n")

