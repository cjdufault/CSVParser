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
                ask_for_column(columns)
            if search_term == None:
                search_term = input("Enter search term:\t")
                    
    except CSVError as csve:
        print(csve)
    except FileNotFoundError as fnfe:
        print(fnfe)
        
        
# read the first line of the file and use those values as column names
def get_column_names(csv_file):
    top_line = csv_file.readline().strip()
    
    if "," not in top_line:
        raise CSVError("File does not appear to be a .csv file")
    else:
        return top_line.split(",")
    

# gets the column the user wants to search
def ask_for_column(columns):
    while True:
        print("\nColumns:")
        print_row(columns)
        column_name = input("Select a column:\t")
        
        if column_name in columns:
            return column_name
        else:
            print("Column not found")
    
# prints the contents of a row from the csv, inputed as a list of values
def print_row(values_list):
    print_string = ""
    
    for value in values_list:
        if " " in value or "\t" in value: # put in quotes if there's whitespace
            value = f"'{value}'"
            
        print_string += value + " "
    
    print(print_string)


# gets command line arguments
def parse_args():
    num_args = len(sys.argv)
    column_name = None
    search_term = None
    
    if num_args == 1:
        input_path = input("Input .csv file path:\t")
        
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
