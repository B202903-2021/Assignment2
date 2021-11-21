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



########################### ###How many taxanomic groups you want to add, then loop through that many times, creating function to variable tax_input#######################################################
Initiate_search = input("\n Would you like to initiate taxanomic search Y/N: ")
while YN(Initiate_search) == False:
    Initiate_search = input("\n Please initiate when ready Y/N:  ")

else:
    loop_var = False
    while loop_var == False: #Allows the user to restart the process of eneteirng taxanomic and protein family parameters
        # Ask the user for tax input
        tax_input = input("\n Please enter taxonomic group: ") or "Aves"

        print("\n Identifying Taxonomy ID for inputed taxonomic group \n")

        # Loop until user inputs correct tax input, if there is no group present in the data base it will continue forever
        while taxanomy_function(tax_input) == "":
            tax_input = input("The taxanomic group you inputed is not available in the NCBI databse, please input again: ") or "Aves"
            # prints the id code
        else:
            taxIDn = taxanomy_function(tax_input)
            print(f"\n Taxanomic ID of", {taxIDn})
            taxID = "txid" + taxIDn  # correct format e.g. txid8782 for Aves

        # Declare protein family
        pro_input = input("\n Please enter the name of the protein family: ") or "glucose-6-phosphatase"

        # Output file name
        document_name = f"proto_seq_{taxIDn}"

        # First check how long the desired search is and ask if they would like to continue download sequence
        print("\n Checking accession count for desired search \n ")

        ## Using the inputed taxanomic group and protin family, search for protein sequences that match these criteria ##
        print(f"\n Identifying protein sequences that meet the criteria of {tax_input} and {pro_input} \n")
        while PRetr_function(tax_input, pro_input) == "":
            pro_input = input(
                "\n There is not protein sequences meeting these requirments available on the NCBI database, please enter new protein family ") or "glucose-6-phosphatase"
            # PRetr_function(tax_input, pro_input)
        else:
            ACC_count = AL_PRetr_function(tax_input, pro_input)
            with open(f"{document_name}_ACC.fa", 'w') as i:
                sys.stdout = i
                print(ACC_count)
                sys.stdout = orig_stdout
            ACC_bash_count = f"wc -l {document_name}_ACC.fa "
            subprocess.call(ACC_bash_count, shell=True)

            ask_count = input("\n Would you like to continue downloading the fasta sequences ")
            if YN(ask_count) == True:
                protein_sequence_output = PRetr_function(tax_input, pro_input)
                print("\n Extracting protein sequence complete! \n")
                loop_var = True #Desired outcome achieved, break loop


                # Export data to file
                with open(f"{document_name}.fa", 'w') as i: #File used for further filtering
                    sys.stdout = i
                    print(protein_sequence_output)
                    sys.stdout = orig_stdout

                with open(f"{document_name}_Ori.fa", 'w') as i: # Copy made of the original file
                    sys.stdout = i
                    print(protein_sequence_output)
                    sys.stdout = orig_stdout

            else:
                print("\n Please re-enter parameters \n")

print(count_per_species(f"{document_name}.fa"))
#######################################################################Filtering the protein list down #######################################################################

#create a variable that is passed along the entire filter, ensuring that each section has the same file input
filter_input = f"{document_name}.fa"

#Filtering functions
def SeqL_count(document_name): # Calculates the length of each protein sequence
    protein_name = None
    l = 0  # set length to 0

    with open(f"{document_name}.fa") as f:
        for line in f:

            line = line.rstrip()  # Removes any characters at the end of the string
            if line.startswith('>'):
                # If we captured one before, print it now
                if protein_name != None:
                    print(l, protein_name, sep="\t")
                    l = 0 #reset the count
                protein_name = line[1:]
            else:
                l += len(line)
    if l:  # prints the lastseq length
        print(l, protein_name, sep="\t")# Basically starting after each > if there is a header print, set to 0, then until length of charcters till the next header in which print will activate
        #Due to the last one not having a header after, it is unable to print thus it has to manually be done


############################

# Building blocks for filter commands
call_pullseq = f"/localdisk/data/BPSM/Assignment2/pullseq -i"
c = "'>'"

###########################


blast_input_SC = count_species(f'{document_name}.fa')
print(f"\n The number of species within fasta file is {blast_input_SC}\n")

###Let them select which protein sequence to use in the blast
###Make sure every stage has count the number of species
greater_loop = True
pull_seq_ask = input("\n Would you like to filter using pullseq Y/N: \n")
if YN(pull_seq_ask) == False:
    greater_loop = False
while greater_loop == True: # Greater loop that enables a restart of the entire filtering process
    while YN(pull_seq_ask) == True: # Given that they would like to filter using pullseq, the following will Accesion and min/max filter can be chosen


                ################################################################## FILTER 1 : ACCESSION LIST#############################################################
        # Ask whether they want to specifcy specific accesion names / State the number of species in the file produced for their reference
        Continue_filter = input("\n Would you like to use accesion filter Y/N: ")
        if YN(Continue_filter) == False:
            loop_var = False
        else:
            loop_var = True
        while loop_var == True:  # Allows for restart of the filter process at this stage
            blastDB_set = True
            while YN(Continue_filter) == True:
                gen_blastpAcc = input("\n Would you like to generate a accesion list using blastp Y/N: ")
                if YN(gen_blastpAcc) == True:
                    blast_input_SC = count_species(f'{document_name}.fa')
                    print(f"\n The number of species within fasta file is {blast_input_SC}\n")
                    blastp_output = input(
                        "\n Enter blastp output name, cannot have special characters including . : ").replace(" ",
                                                                                                              "") or "blastp_def"  # Allow them to input file name, or set default file name
                    print(blastp_output)

                    while Special_check(blastp_output) == True:  # Checks their input for special characters
                        print("\n The output name given contains special characters! \n")
                        blastp_output = input(
                            "\n Enter blastp output name, cannot have special characters including . : \n") or "blastp_def"

                    else:
                        print("\n File name output is valid, commence blastp\n")
                        if blastDB_set == True:  # Only when the filter is on its first run as well as on restart will the blastdb be generated
                            print("\n Generating blast database\n")
                            make_blastdb = f"makeblastdb -in {document_name}.fa -dbtype prot -out {taxIDn}_db.fa"
                            subprocess.call(make_blastdb,
                                            shell=True)  # Generates blastdb based on the file produced from the taxanomic and protein family search / protein database.

                        print("\n\ Loading... \n")

                        blastpAcc = f"blastp -db {taxIDn}_db.fa -query 1.FASTA -outfmt '10 saccver' -out {blastp_output}.fa "  # Command line for blastp the file selected
                        subprocess.call(blastpAcc, shell=True)

                header_file_input = input(
                    "Please write the name of the file containing the accesion names: ").strip() or f"{document_name}_ACC.fa"  # create a file containing header names
                while os.path.exists(
                        header_file_input) == False:  # Check whether the file exists, if not then make the user input a file until it does
                    print(f"\n There is no file with {header_file_input}\n")
                    header_file_input = input("\nPlease input a new file name\n").strip() or "EX.txt"
                else:
                    while header_file_input == "":  # Then once the file is known
                        print("\n No file input \n")
                    else:
                        pullseq_names = f"-n {header_file_input}"
                        filter_accesions_list = f"{call_pullseq} {filter_input} {pullseq_names} > temp.fa && mv temp.fa ProSeq_AF.fa"  # the > temp.fa etc is a trick used to create a file and overwrite the original, pullseq alone cant input and overwrite the same file
                        print(filter_accesions_list)
                        subprocess.call(filter_accesions_list, shell=True)
                        filter_input = "ProSeq_AF.fa"
                        blast_input_SC = count_species(filter_input)
                        print(f"\n The number of species within filtered file is {blast_input_SC}\n")

                F_lineC = f"cat {filter_input} | grep -c {c}"
                print(F_lineC)
                subprocess.call(F_lineC, shell=True)
                blastDB_set = False  # Prevents blastdb being generated again unless restart filter

                Continue_filter = input("\n Would you like to continue to use accession list filter Y/N: ")

            else:
                restart_filter = input("\n Would you like to restart the filtering process Y/N: ")
                if YN(restart_filter) == False:
                    break
                else:
                    Continue_filter = "y"
                    filter_input = f"{document_name}.fa"  # Resets the input file back to the original,
                    blast_input_SC = count_species(
                        f'{document_name}.fa')  # Makes sure they see the number of species upon restarting the filter process
                    print(f"\n The number of species within fasta file is {blast_input_SC}\n")

                ##########################################################################################FILTER 2: MIN MAX SEQUENCE LIST##############################################################################

        # Ask whether they would like to specify min or max
        MMM = input(" Would you like filter based on minium and/or maximum sequence length, type y or n: ")
        if YN(MMM) == False:
            loop_varMMM = False
            pull_seq_ask = 'n'
        else:
            loop_varMMM = True
        filter_input_restart = filter_input
        # Calculate length of each protein sequence
        MMM_calculations = False  # Prevents break when not declared
        if YN(MMM) == True:  # Given that they want to use min and max
            # Create a file, containing the lengths for each protein sequence
            with open(f"{document_name}_SL.csv", 'w') as i:
                sys.stdout = i  # towards file
                sys.stdout = SeqL_count(document_name)
                sys.stdout = orig_stdout  # away from file
            headed_document = pd.read_csv(f"{document_name}_SL.csv", sep="\t", names=['Sequence length',
                                                                                      'Protein sequence name'])  # Add headers to file of lengths per protein sequence
            with open(f"{document_name}_SL_headed.csv", 'w') as i:  # Create the headed version as calculations will remove the first line becomes header
                sys.stdout = i
                print(headed_document)
                sys.stdout = orig_stdout
            # Using the headed version and panada, using column 1, calculate the min, max and mean
            seq_min = headed_document['Sequence length'].agg('min')
            seq_max = headed_document['Sequence length'].agg('max')
            seq_mean = round(headed_document['Sequence length'].agg('mean'))  # Rounded
            MMM_calculations = True  # makes sure that if the calcualtions for length are not done, mean min and max stages will not occur
        else:
            print("Commencing next stage")

        if MMM_calculations == True:
            # Present a summary of min, max and mean
            # Ask if they want to see the summary
            Summary_MMM = input(" Would you like to see a summary of Mean, Min and Max: ")
            if YN(Summary_MMM) == True:
                print("\nProtein Sequences: Mean, Min and Max\n")
                print(f"\nMean: {seq_mean}\n")
                print(f"\nMin: {seq_min}\n")
                print(f"\nMax: {seq_max}\n")
            else:
                print("Commencing next stage")

            # Ask if they want to see a list of protein sequences with their lengths
            Seq_per_PS = input(" Would you like to see all protein sequences along with their length: ")
            if YN(Seq_per_PS) == True:  # Open the headed file to print its content
                with open(f"{document_name}_SL_headed.csv", 'r') as f:
                    content = f.read()
                    print(content)
            else:
                print("Commencing next stage")

        print(filter_input)
        # Given that they would like to use min or max for filter, allow them to specify whether they would like to use min, max or both together
        while loop_varMMM == True:  # Allows for restart of the filter process at this stage
            while YN(MMM) == True:
                ask_min = YN(
                    input("Would you like to filter based on min sequence length, Y/N : "))  # Ask for min length input
                ask_max = YN(
                    input("Would you like to filter based on max sequence length, Y/N : "))  # Ask for max length input
                if ask_min == True:  # Given that they would like to use min, let them input value
                    min = input("Please input the minimum sequence length: ").replace(" ",
                                                                                      "")  # .replace(" ", "") converts all spaces to no spaces, basically removes all possible spaces
                    while min == "":
                        print("\n No min input \n")
                        min = input(" Please input minimum sequence length again: ").replace(" ", "")

                    else:
                        while Int_check(min) == False:  # Checks whether the min value is a int
                            print("\n Input was not integer or float \n")
                            min = input("\n Please enter a integer or a float value: ").replace(" ", "")
                        else:
                            print("Minium sequence length inputed into command line")
                            min_pullseq = f"-m {min}"  # Ensures the command line is created given they fail to input the 1st time

                if ask_max == True:  # Given that they would like to use max, let them input value
                    max = input("Please input the maximum sequence length: ").replace(" ", "")

                    while max == "":
                        print("\n No max input: ")
                        max = input("Please input maximum sequence length again: ").replace(" ", "")
                    else:
                        while Int_check(max) == False:  # Checks whether the min value is a int
                            print("\n Input was not integer\n")
                            max = input("\n Please enter a integer: ").replace(" ", "")
                        else:
                            print("Maximmum sequence length inputed into command line")
                            max_pullseq = f"-a {max}"  # Ensures the command line is created given they fail to input the 1st time

                if ask_max == True or ask_min == True:  # Given that either min or max has been selected

                    if ask_min == True and ask_max == False:  # Generates command line for min specified
                        MMM_pullseq = f"{call_pullseq} {filter_input} {min_pullseq}"
                    if ask_max == True and ask_min == False:  # Generates command line for max specified
                        MMM_pullseq = f"{call_pullseq} {filter_input} {max_pullseq}"
                    if ask_min == True and ask_max == True:  # Generates command line for min and max specified
                        MMM_pullseq = f"{call_pullseq} {filter_input} {min_pullseq} {max_pullseq}"
                    MMM_pullseq_complete = f"{MMM_pullseq} > temp.fa && mv temp.fa ProSeq_MMM.fa"  # Completes the command line that needs to be run, then as the file cannot overwrite directly, we need to create a temp file to pass the info through
                    print(MMM_pullseq_complete)
                    MMM_output = subprocess.call(MMM_pullseq_complete,
                                                 shell=True)  # Creates a shell to run bash command
                    filter_input = "ProSeq_MMM.fa"  # Reassigns the most recent file to the variable

                    # Count the number of protein sequences in each file
                    F_lineC = f"cat {filter_input} | grep -c {c}"
                    print(F_lineC)
                    subprocess.call(F_lineC, shell=True)

                    MMM = input(
                        "\n Would you like to continue to use min/max filter Y/N: ")  # Breaks the loop if N or continues if Y

            else:
                restart_filter = input("\n Would you like to restart the filtering process Y/N: ")
                if YN(restart_filter) == False:
                    pull_seq_ask = 'n'
                    break

                else:
                    MMM = "y"
                    # Deletes variables to ensure restart is clean
                    #if ask_min == True:
                        #del min
                   # if ask_max == True:
                        #del max

                    filter_input = filter_input_restart  # Resets the input file back to the original,
                    blast_input_SC = count_species(
                        f'{document_name}.fa')  # Makes sure they see the number of species upon restarting the filter process
                    print(f"\n The number of species within fasta file is {blast_input_SC}\n")

    else:
        restart_filter = input("\n Would you like to restart the filtering process Y/N: ")
        if os.stat(filter_input).st_size == 0 :
            print("\n There is no content in the fasta file, please re-do filtering \n")
            restart_filter = "y"
        if YN(restart_filter) == False:
            break
        else:
            pull_seq_ask = "y"
            filter_input = f"{document_name}.fa"  # Resets the input file back to the original,
            blast_input_SC = count_species(
                f'{document_name}.fa')  # Makes sure they see the number of species upon restarting the filter process
            print(f"\n The number of species within fasta file is {blast_input_SC}\n")








################################################################################ Stage 2###########################################################################



##### Multi sequence alignment using Clustero
Cluster_YN = input("Initiate clustero multi alignment of protein sequences, Y/N")
while YN(Cluster_YN) == False:
   print("\n To carry out following protein analysis, multi-sequence allignment must be carried out, please initiate when ready: \n")
   Cluster_YN = input("Initiate clustero Y/N : ")
else:
    cl_command = f"clustalo -t Protein -i {filter_input} -o {document_name}.msf -v --force"  # can add -maxnumseq = 1000 to limit the process
    print("Aligning protien sequnces, generating file")
    subprocess.call(cl_command, shell=True)
    cl_command_phylo = f"clustalo -t Protein -i {filter_input} -o {document_name}.phy -v --force"  # can add -maxnumseq = 1000 to limit the process
    print("\n Generating copy for phylogenetic analysis\n ")
    subprocess.call(cl_command_phylo, shell = True)
    print("Commencing next stage")


###File cleanup from Stage 1
# Removes all MMM files
remove_all_MMM = "rm -f *_MMM.fa"
subprocess.call(remove_all_MMM, shell=True)

#Removes all AF files
remove_all_AF = "rm -f *_AF.fa"
subprocess.call(remove_all_AF, shell=True)

###### CHANGE TO FALSE as you want to force them to do this
Emboss_YN = input("Would you like display basic information on the multiple sequence alignment")
if YN(Emboss_YN) == True:
    emboss_align = f"infoalign -auto -sequence {document_name}.msf -outfile ruociCatacylsm.doc "
    subprocess.call(emboss_align, shell=True)
else:
    print("Commencing next stage")

