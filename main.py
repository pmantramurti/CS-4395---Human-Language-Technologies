
import sys  # to get the system parameter
import os   # used by method 1

filepath = "data\\data.csv"

if __name__ == '__main__':
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        text_in = f.read()
    print(text_in)