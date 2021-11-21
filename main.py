

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
                print("\n Please re-enter pa:wq

