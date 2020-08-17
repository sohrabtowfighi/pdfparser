#
# This script parses PDF files, extracts the information that has been written 
# in the fillable slots, and appends this information to a CSV file.
# This software needs to be used from a command line terminal. On Windows, use 
# Git Bash.
#
# You can read the manual using the terminal: `winpty python pdf_parser.py -h`
#
# Written in Python 3.6
# Sohrab Towfighi 2020
#

from pdfrw import PdfReader
import sys
import argparse
import csv
import os
import pdb

def append_fields_in_pdf_to_csv(input_path, output_csv):
    """
    Given an input path to one PDF OR a directory where the PDF files are all 
    from the same fillable template, this function takes all the PDF files, gets 
    the values in the fillable sections, and saves them to a CSV file.    
    
    Inputs
    -----
    `input_path`: string
    `output_csv`: string
    
    ----
    Returns
        None
    """
    pdf_filepaths = list()
    if os.path.isdir(input_path) == True:        
        pdf_filepaths = os.listdir(input_path)
        pdf_filepaths = [x for x in pdf_filepaths if x.lower().endswith('pdf')]
    elif os.path.isfile(input_path) == True:
        if input_path.lower().endswith('pdf') == False:
            msg = "This file does not use a '.pdf' extension. "
            msg += "Only supply this script with pdf files."
            raise Exception(msg)
        pdf_filepaths.append(input_path)
    else:
        print("The input path is neither a file nor a folder on your system")
        print("You gave " + input_path + " as the input path")
        exit(1)
    output_table = list()
    for pdf_path in pdf_filepaths:
        filename = os.path.basename(pdf_path)
        x = PdfReader(pdf_path)
        csv_row = dict()
        for page in x.Root.Pages.Kids:  
            for field in page.Annots:
                if field.T is None:
                    continue
                else:
                    label = field.T[1:-1]
                if field.V is None:
                    value = ''
                else:
                    value = field.V[1:-1]
                csv_row[label] = value
        output_table.append(csv_row)
    with open(output_csv, 'w+') as myfile:              
        fnames = output_table[0].keys()
        writer = csv.DictWriter(myfile, fieldnames=fnames, lineterminator='\n', 
                                quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for row in output_table:
            writer.writerow(row)

if __name__ == '__main__':        
    parser = argparse.ArgumentParser(prog='pdf_parser.py', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("input_path", help="An absolute path to either a folder which houses the relevant PDF files (and no other files) OR an absolute path to one pdf file")
    parser.add_argument("output_csv", help="An absolute filepath where we save results to a comma separated value file. Include the filename. The file extension is typically '.csv'")
    if len(sys.argv) == 0:
        parser.print_usage()
        sys.exit(1)
    arguments = parser.parse_args()
    input_path = arguments.input_path
    output_csv = arguments.output_csv    
    append_fields_in_pdf_to_csv(input_path, output_csv)
    
    