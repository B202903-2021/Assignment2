n.py
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

# global variables
orig_stdout = sys.stdout

######Tick List

# All functions used at some point, except float check
#The intial taxanomic search is robust,still somethings we can do
#Expert mode, manually altering the variables : can break the script
#Filter: Accesion is currently robust
#Filter: Min or max is currently robust
#Greater loop is complete. Restart can occurat each filter level as well as each module





#esearch -db protein -query "Aves[organism] AND glucose-6-phosphatase[protein] NOT PARTIAL NOT PREDICTED" |efetch -db protein -format acc > file.txt
#### Make them enter taxaonomic group then ask if they would like add additional
### Make the script rerunnable


# Import webbrowser
# ebbrowser.get("firefox").open(fullname)


##############################################Creating function for assessing validity of taxanomic group#################################################


#Retrieves taxonomy ID
def taxanomy_function(tax_input):
    taxData = edirect.execute(f"esearch -db taxonomy -query '{tax_input}'")  # Requests web data
    taxDRetrieve = edirect.execute("esummary", taxData)  # Make the web data readable
    taxIdentity = edirect.execute("xtract -pattern DocumentSummary -element Id",taxDRetrieve)  # Extract Taxonomy ID from readable data
    return taxIdentity

