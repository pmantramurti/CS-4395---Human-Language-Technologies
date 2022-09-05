# Program 1 Overview

## Description
  This program processes a data file of employee information, reformats any incorrect entries, creates a dictionary of Employees, saves the dictionary to a pickle file, then retrieves the dictionary from the file and prints the data of each Employee to the console.
  
## Instructions
  Run the program with the relative path to Data.csv as an argument. When prompted, enter the corrected form of the given incorrectly formmated entry.
  
## Strengths and Weaknesses
  One of the strengths of the Python text processing is that Regex makes it really easy to check the format of a string without a series of if statements. Another is how easy it is to turn a row in an Excel sheet into a list of strings in the program. One disadvantage is that the split() method can get confused if a comma already exists in an entry. For example, if one of the phone numbers was misformatted witha comma instead of a dash, it would completely mess up the program. A more comprehensive way to process text to split up entries would avoid such possibilities.

## What I learned
  I would say that the aspects of this assignment that are new to me would be the pickle package, as well as regex. Otherwise, the rest of the program, such as using functions, classes, sys args, file I/O and getting input from the console was review for me, as I've used python for some simple programs in the past.
