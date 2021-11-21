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


#Creating function to obtain protein sequences that meet the taxanomic and protein requirments
def PRetr_function(tax_input, pro_input) :
    Accession_input = edirect.execute(f"esearch -db protein -query '{tax_input}[organism] AND {pro_input}[protein] NOT PARTIAL'")
    Accession_list = edirect.execute("efetch -format fasta", Accession_input)  # Download all protein sequence files fasta
    return Accession_list


#Retrieve Accesion list for above function
def AL_PRetr_function(tax_input, pro_input) :
    Accession_input = edirect.execute(f"esearch -db protein -query '{tax_input}[organism] AND {pro_input}[protein] NOT PARTIAL'")
    Accession_list = edirect.execute("efetch -format acc", Accession_input)  # Download all protein sequence files fasta
    return Accession_list


#True or False function : If user input y or n
def YN(YNinput):
    while "Input is not Y or N":
        response=str((YNinput+ '(y/n):')).lower().strip()
        if response[0] =="y":
            return True
        if response[0] =="n":
            return False
        else :
            print("\n Cannot interpret \n")
            response = input("Please retype")
            return YN(response)


#Input check function
def Special_check(SC_input): # Checks for special characters
    SC_value = any(not SC.isalnum() for SC in SC_input)
    if SC_value == True:
        return True
    else:
        return False


def Int_check(IC_input) : # Checks for integer
    if IC_input.isnumeric() == True:
        return True
    else:
        return False


def Float_check(IC_input) : #Checks for float
    if isinstance(IC_input, float) :
        return True
    else:
        return False


#Create Species Dic with count per species
def dict_species(fasta_input):
    with open(f'{fasta_input}', 'r') as i:
        empty_list = []
        empty_dic = {}
        for line in i:
            if line[0] == ">":
                s = line
                pattern = "\[(.*?)\]"
                substring = re.search(pattern, s).group(1)
                if substring not in empty_list:
                    empty_dic[substring] = 1
                    empty_list += [substring]
                else:
                    empty_dic[substring] += 1
        return empty_dic

# Show count of each specieis
def count_per_species(fasta_input):
    print("\n Counts per species \n")
    for species, count in dict_species(fasta_input).items():
        print(f"{species} and {count}")
# Summary count_per_sepcieis
#Count Species
def count_species(fasta_input):
    with open(f'{fasta_input}', 'r') as i:
        empty_list = []
        empty_dic = {}
        count = 0
        for line in i:
            if line[0] == ">":
                s = line
                pattern = "\[(.*?)\]"
                substring = re.search(pattern, s).group(1)
                if substring not in empty_list:
                    empty_list += [substring]
                    count += 1

        return count


