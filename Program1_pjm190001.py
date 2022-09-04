import sys
import os
import re
import pickle


# Person class to contain person data. Constructor takes list of data, saves to corresponding variables.
# Display prints person data to console
class Person:

    def __init__(self, dataList):
        self.last = dataList[0]
        self.first = dataList[1]
        self.mi = dataList[2]
        self.id = dataList[3]
        self.phone = dataList[4]

    def display(self):
        print("Employee id: " + self.id)
        print("\t" + self.first + " " + self.mi + " " + self.last)
        print("\t" + self.phone)


# procStr takes input string, splits into separate values, and formats where required. Returns list of person data
def procStr(inputStr):
    dataList = inputStr.split(',')
    dataList[0] = dataList[0].capitalize()
    dataList[1] = dataList[1].capitalize()
    if dataList[2]:
        dataList[2] = dataList[2][0].upper()
    else:
        dataList[2] = 'X'
    isCorrect = False
    while not isCorrect:
        x = re.search("^[a-zA-Z]{2}[0-9]{4}$", dataList[3])
        if x:
            dataList[3] = "" + dataList[3][0].upper() + dataList[3][1].upper() + dataList[3][2:]
            isCorrect = True
        else:
            print("ID invalid: " + dataList[3])
            print("ID is two letters followed by 4 digits")
            dataList[3] = input("Please enter a valid id: ")
    isCorrect = False
    while not isCorrect:
        x = re.search("^[0-9]{3}[-][0-9]{3}[-][0-9]{4}$", dataList[4])
        if x:
            isCorrect = True
        else:
            print("Phone " + dataList[4] + " is invalid")
            print("Enter phone number in form 123-456-7890")
            dataList[4] = input("Enter phone number:")
    return dataList


# accesses data file, passes input strings to procStr, converts list output into person objects and saves to dict.
# returns dict
def procFile():
    dict_o = {}
    if len(sys.argv) != 2:
        print("Incorrect sysArg. Please run again with correct sysArg.")
        exit()
    filepath = sys.argv[1]
    f = open(os.path.join(os.getcwd(), filepath), 'r')
    text_in = f.readline()
    text_in = f.readline()
    while text_in:
        personData = procStr(text_in)
        dict_o[personData[3]] = Person(personData)
        text_in = f.readline()
    return dict_o


# saves dict output from procFile to dict object, creates pickle file with dict, then retrieves dict from pickle
# file and runs display method from Person class
if __name__ == '__main__':
    dict_out = procFile()

    pickle.dump(dict_out, open('dict.p', 'wb'))

    dict_res = pickle.load(open('dict.p', 'rb'))
    print("Employee List:")
    for person in dict_res:
        dict_res[person].display()
        print()
