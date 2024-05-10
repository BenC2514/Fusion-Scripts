#Author- BenC2514
#Description- Bulk export STL's from CSV file. Make sure sketch is in tree root

# Import necessary modules
import csv, tkinter as tk
from tkinter import filedialog

#open file from file dialog box
filename = filedialog.askopenfilename()
file = open(filename, encoding='utf-8-sig')

#take data as list and close file
data = list(csv.reader(file,delimiter=","))    
file.close

#loop through everything in list and print formatted data
for x in data:
    name = str(x).strip("['']")
    print ("Exporting "+ name)
    #EXPORT STL CODE HERE

