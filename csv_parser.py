"""Application to parse .csv files and output a .csv that contains all rows in
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
                column_name = ask_for_column(columns)
            if search_term == None:
                search_term = input("Enter search term:  ")
            
            column_index = columns.index(column_name)
            matches = search(csv_file, column_index, search_term)
            
            if len(matches) > 0:
                print(f"{len(matches)} matching rows")
                
                while True:
                    yN = input("Write matching rows to file? Y/n:  ")
                    
                    if yN.lower() == "y" or yN.lower() == "yes":
                        original_filename = input_path.replace(".csv", "")
                        filename = f"{original_filename}_{column_name}_{search_term}.csv"
                        write_to_file(filename, matches)
                        print(f"Wrote to {filename}")
                        break
                    
                    elif yN.lower() == "n" or yN.lower() == "no":
                        break
            else:
                print("No matching rows")
                    
    except CSVError as csve:
        print(csve)
    except FileNotFoundError as fnfe:
        print(fnfe)
        
        
# read the first line of the file and use those values as column names
def get_column_names(csv_file):
    top_line = csv_file.readline().strip()
    columns = []
    
    if "," not in top_line:
        raise CSVError("File does not appear to be a .csv file")
    else:
        
        for column in top_line.split(","):
            if column not in columns:
                columns.append(column)
            else:
                raise CSVError("Column names must be unique")
    
    return columns
    

# reads the .csv line by line, adding a row to matches if search term is found
def search(csv_file, column_index, search_term):
    matches = []
    
    line = csv_file.readline().strip()
    while line:
        values = line.split(",")
        
        # check that there are enough values for the index
        if not column_index >= len(values):
            if values[column_index] == search_term:
                matches.append(values)
        line = csv_file.readline().strip()
    
    return matches
    

# gets the column the user wants to search
def ask_for_column(columns):
    while True:
        print("Columns:")
        print_row(columns)
        column_name = input("Select a column:  ")
        
        if column_name in columns:
            return column_name
        else:
            print("Column not found\n")
    
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
        input_path = input("Input .csv file path:  ")
        
    elif num_args > 1:
        input_path = sys.argv[1]
        
        if num_args > 2:
            column_name = sys.argv[2]
        if num_args > 3:
            search_term = sys.argv[3]
            
    return input_path, column_name, search_term


def write_to_file(filename, matches):
    with open(filename, "w") as out_file:
        lines = []
        for row in matches:
            line = ""
            for value in row:
                if row.index(value) < len(row) - 1:
                    line += value + ","
                else:
                    line += value
            lines.append(line + "\n")
        out_file.writelines(lines)


class CSVError(Exception):
    pass


if __name__ == "__main__":
    main()
