#------------------------------------------#
# Title:CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# TDavis, Mar 2022, Modified for Assignment 07
#------------------------------------------#

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object
import pickle #needed for reading and writing data and calling pickle functions


# -- PROCESSING -- #
class DataProcessor:

    "Allows the user o create and delete entries in current memory"
   
    def create_entry(newRow):
        
        """Allows the user to create an entry"
       
        Args: newRow: list of inventory entry/one data line
       
        Returns: None"""
       
        intID=int(newRow[0])
        strTitle=newRow[1]
        stArtist=newRow[2]
        dicRowloc = {'ID': intID, 'Title': strTitle, 'Artist': stArtist}
        lstTbl.append(dicRowloc)
        IO.show_inventory(lstTbl)
        
     
        
    def delete_entry(table, idNumber):
        """Allows the user to delete an entry
        
        Args: table:list of dictionary rows (i.e. full inventory in current memory
              idNumber: the selected value for deletion
        
        Returns: none"""
        
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == idNumber:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
        IO.show_inventory(table)
        
      
    
        

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from

        Returns:
             table (list of dict): 2D data structure (list of dicts) that holds current inventory
            
        """

        while True: #created loop to handle no existing file error and prompt user to begin creating entries
            try:  
                with open(file_name, 'rb') as objFile: #opening the file
                     table=pickle.load(objFile) #unpickling the data and defining as table
                     return table #returning the table
                     break
            except FileNotFoundError: #error handling
             print('\n No CD Inventory currently exists.  Try selecting \'a\' from the menu to begin building library')  
             break
        

    @staticmethod
    def write_file(table, file_name):
        """Function to save entries in memory to strFileName aka CdInventory.txt
        
            Args: 
                file_name:identifies the file to be written to
                table: parameter for lstTbl identified below
                
            Returns: None"""
        with open(file_name, 'wb') as objFile:#opening file
            pickle.dump(table, objFile)#pickling the data and writing to file
          


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """
        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():#no additional error handling necessary
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):#no error handling necessary 
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')
        
    @staticmethod
    def get_entry(strIDloc, strTitleloc, stArtistloc):
        
        """Collects data from the user for an entr
        
        Args: 
            strIDloc: the id number for the entry
            strTitleloc: the title for the entry
            stArtistloc: the artist name for the entry
    
        Returns:
            lstRowloc: a list that will be converted to a dicRow and added to the lstTbl in another function"""
        while True: #testing for string that can be converted to integer for proper DataProcessor function with while try loop
            try:
                strIDloc = int(input('Enter ID: ').strip()) 
                strTitleloc = input('What is the CD\'s title? ').strip()
                stArtistloc = input('What is the Artist\'s name? ').strip()
                lstRowloc=[str(strIDloc), strTitleloc, stArtistloc]
                break
            except :
                print('\n Invalid entry for ID number.  Must be integer')
        return lstRowloc
        

# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice() #Error handling addressed within function (i.e no change necessary)

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled \n')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            lstTbl=FileProcessor.read_file(strFileName)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
        #Any unexpected entry will just cancel the function and return to the menu (tested with special characters and integrers)
        #No additional error handling necessary 
    # 3.3 process add a CD
    elif strChoice == 'a': #Error handling addressed in get_entry function
        # 3.3.1 Ask user for new ID, CD Title and Artist
        strID=''
        strTitle=''
        stArtist=''
        lstRow=IO.get_entry(strID, strTitle, stArtist)

        # 3.3.2 Add item to the table
        DataProcessor.create_entry(lstRow)
      
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        
        # 3.5.1.2 ask user which ID to remove
        while True: #Added to address non-integer entry
            try:
                intIDDel = int(input('Which ID would you like to delete? ').strip())
                break
            except:
                print('\n Invalid entry.  ID must be an integer')
        
        # 3.5.2 search thru table and delete CD
        DataProcessor.delete_entry(lstTbl, intIDDel)
        
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's': #Tested for user entering an integer rather than y/n and error handled by current code
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(lstTbl,strFileName)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




