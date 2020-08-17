# pdfparser
Parses fill-able PDF files and extracts fields into a CSV file.

# usage
```
$ winpty python pdf_parser.py -h
usage: pdf_parser.py [-h] input_path output_csv

positional arguments:
  input_path  An absolute path to either a folder which houses the relevant
              PDF files (and no other files) OR an absolute path to one pdf
              file
  output_csv  An absolute filepath where we save results to a comma separated
              value file. Include the filename. The file extension is
              typically '.csv'

optional arguments:
  -h, --help  show this help message and exit
```

# author
Sohrab Towfighi (C) 2020
Licence: GPL v 3.0
