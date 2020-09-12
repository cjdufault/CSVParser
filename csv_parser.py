"""Application to parse .csv files and output a csv that contains all rows in
which a specified column contains a specified string. Assumes that all rows
contain the same number of values as the top row, and that the top row contains
the column names."""

import sys


def main():
    args = parse_args()
    input_path = args[0]
    column_name = args[1]
    search_term = args[2]
    
    try:
        with open(input_path) as csv_file:
            columns = get_column_names(csv_file)
            
            if column_name == None:
                print_row(columns)
                    
    except CSVError as csve:
        print(csve)
    except FileNotFoundError as fnfe:
        print(fnfe)
        
        
def get_column_names(csv_file):
    top_line = csv_file.readline().strip()
    
    if "," not in top_line:
        raise CSVError("File does not appear to be a .csv file")
    else:
        return top_line.split(",")
    

def print_row(values_list):
    


# gets command line arguments
def parse_args():
    num_args = len(sys.argv)
    column_name = None
    search_term = None
    
    if num_args == 1:
        input_path = input("Input .csv file path:  ")
        
    elif num_args > 1:
        input_path = sys.argv[1]
        
        if num_args > 2:
            column_name = sys.argv[2]
        if num_args > 3:
            search_term = sys.argv[3]
            
    return input_path, column_name, search_term


class CSVError(Exception):
    pass


if __name__ == "__main__":
    main()
