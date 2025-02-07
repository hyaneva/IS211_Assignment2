
import argparse
import urllib.request
import logging
import csv
from datetime import datetime




#Downloading the file and converting it from bytes to a string with decode()

def downloadData(url):
    with urllib.request.urlopen(url) as response:
        the_file = response.read().decode('utf-8')     
    return the_file    
    
    


#Splitting the csv file and adding the data to a dictionary
#Stores date as a datetime object not string
#Includes logger which saves error messages caused by lines that couldn't be added due to incorrect formatting


def processData(file, logger):
    
    birthday_dict = {}
    split_by_line = file.strip().split("\n")
    
  


    
    for linenum, line in enumerate(split_by_line[1:], start=2):         #Excludes the first line of the dictionary since those are just column names
        words = line.split(",")
        if len(words) == 3:                #Making sure line contains exactly three values for correct formatting
            id, name, birthday = words
            try:
                id = int(id)
                datetime_birthday = datetime.strptime(birthday, "%d/%m/%Y").date()
                birthday_dict[id] = name, datetime_birthday
            
            except ValueError:
                logger.error(f"Error processing line #{linenum} for ID #{id}")
        
    return birthday_dict
    
    
    




def displayPerson(id, downloaded_data):
    
    if id in downloaded_data:
        name, date = downloaded_data[id]
        print(f"Person #{id} is {name} with a birthday of {date}.")
    else:
        print("No user found with that ID.")   



#Main funciton that runs the program


import sys   #test
import argparse

def main(url):
    print(f"Running main with URL = {url} ...")
    

    logger = logging.getLogger("assignment2")
    logging.basicConfig(filename='error.log',
                            level=logging.ERROR,
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

    try:
        csv_data = downloadData(url)   #Downloads data with whichever url was put in
    except Exception as e:
        print(f"Error downloading data: {e}")
        return
    
    personData = processData(csv_data, logger)
    
    
    
    while True:
        try:
            user_id = int(input("Enter an ID to lookup (0 or negative ID to exit): "))
            
            if user_id <= 0:
                print("Exiting program.")
                break
        
            displayPerson(user_id, personData)
        
        except ValueError:
            print("Oops! Invalid input. Please enter a valid number.")
            continue

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)   #Makes program takes --url string parameter 
    
    # Simulate command-line input (you can change the URL as needed) test
    sys.argv = ['script_name', '--url', 'https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv']
    
    args = parser.parse_args()
    main(args.url)



