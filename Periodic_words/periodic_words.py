import string
import copy
import sys
"""
Nathan Schneider
periodic_words.py 7/10/19

This program takes words, and checks to see if they can be 
expressed as a series of periodic table element symbols. It
performs a recursive branching process in which it progresses through 
the input word with single or double character elemental symbols until 
it reaches the end of the word. 
"""

#A cleaning input function, to avoid any non-letters from being input into the function
def clean_input(input_string):
    new_string = ""
    for char in input_string:
        if char.isalpha(): new_string+=char.lower()
    return new_string


#The Periodic_Table_Maker class is the class that will perform the operation on the input word
#It uses dictionaries between letters and lists of element symbols. These maps map each letter
#To lists of elements that also begin with that letter
class Periodic_Table_Maker():
    def __init__(self,filename):

        #initialize the elements from a csv I found
        elements_file = open(filename,"r")
        file_string = elements_file.read()
        element_array = [line.split("\t") for line in file_string.split("\n")]

        #Intermediate arrays
        names = [line[1] for line in element_array]
        symbols = [line[2] for line in element_array]

        #The maps that will do the work
        self.letter_to_symbols = {}
        self.letter_to_names = {}

        #For each letter and symbol, see if they match the first character
        for letter in string.ascii_lowercase:
            for index in range(len(symbols)):
                if symbols[index][0].lower() == letter:

                    #If the dict isn't initalizes
                    if letter not in self.letter_to_names:
                        self.letter_to_names[letter] = []
                        self.letter_to_symbols[letter] = []

                    #Add the symbol to the mapping dictionary
                    self.letter_to_symbols[letter].append(symbols[index])
                    self.letter_to_names[letter].append(names[index])
        
        #These lists of lists hold all the possible configurations for names and symbols
        self.symbol_configurations = []
        self.name_configurations = []

    #Convert takes the input string, calls parse to update the instance variable, then prints 
    #The configurations
    def convert(self,input_string):
        self.parse(input_string)
        for i in range(len(self.symbol_configurations)):
            print(self.symbol_configurations[i],self.name_configurations[i])

        self.symbol_configurations = self.name_configurations = []

    #Parse is a recursive algorithm that steps through the word and branches when it 
    #can continue through the word with more than one element
    #The index increases compared to the index, the symbol_list is the list of symbols
    #That holds the current elemental configuration, same with name_list
    def parse(self,input_string,index=0, symbol_list = [],name_list = []):
        #Base case, if we made it to the end of the word, an elemental configuration is
        #possible, and should be equal to the symbol/name list
        if index == len(input_string): 
            self.symbol_configurations.append(symbol_list)
            self.name_configurations.append(name_list)
            return 
        
        #Consider the letter at the index of input_word
        letter = input_string[index].lower()

        #Check if there is element that begins with this letter of input_word
        if letter not in self.letter_to_symbols: return


        #For each symbol/name that does work for the given letter
        for i in range(len(self.letter_to_names[letter])):
            symbol = self.letter_to_symbols[letter][i]
            name = self.letter_to_names[letter][i]

            #We know that the first letter of the symbol matches our current letter, we now break it into cases

            #For len(symbol)==1, we have no problem continuing
            length_one_good = len(symbol)==1

            #For len(symbol)==2, we have to make sure not to go over the length of the string, and that it matches the
            #second character as well
            length_two_good = (len(symbol) ==2 and index < len(input_string)-1 and symbol[1]==input_string[index+1])

            #For the rare len(symbol)==3, we must watch length, and match the second and third character
            length_three_good = (len(symbol)==3 and index<len(input_string)-2 and \
                symbol[1]==input_string[index+1] and symbol[2]==input_string[index+2])

            if length_one_good or length_two_good or length_three_good:
                new_symbol_list = copy.deepcopy(symbol_list) #copy the lists
                new_symbol_list.append(symbol)
                new_name_list = copy.deepcopy(name_list)
                new_name_list.append(name)

                #Recurse the algorithm for this case
                self.parse(input_string,index = index+len(symbol),\
                    symbol_list = new_symbol_list,name_list = new_name_list)





elements_file = "elements.txt"
ptm = Periodic_Table_Maker(elements_file)
input_word = input("Enter a word to be turning to elements, or 'stop' to end: ")
ptm.convert(clean_input(input_word))
while input_word!='stop':
    input_word = input("Enter a word to be turning to elements, or 'stop' to end: ")
    ptm.convert(clean_input(input_word))

