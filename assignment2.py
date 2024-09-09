import urllib.request
import datetime
import logging 
import argparse

def downloadData(url): # we are going to be using this to download the data that is stored in the URL. 
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8') 
            if not data:
                print("No data received from the URL.")
                return None
        return data
    except Exception as e:
        print(f"Error downloading data: {e}")
        
url = "https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv"
csv_data = downloadData(url)

if csv_data:
    print(csv_data[:3000])

def processData(file_contents):

    """What is happening here is that we are acquiring the data from the personData
    and this is able to go through the records"""
    
    personData = {}
    logger = logging.getLogger('assignment2')

    for linenum, line in enumerate(file_contents.splitlines(), start=1):
        try:
            person = line.split(',')
            if len(person) != 3:
                raise ValueError("Incorrect number entered")

            id = int(person[0].strip())
            name = person[1].strip()
            birthday = datetime.datetime.strptime(person[2].strip(), '%d/%m/%Y').date()

            personData[id] = (name, birthday)
        except (ValueError, IndexError) as e:
            logger.error(f"Error processing line #{linenum} for ID #{person[0] if len(person) > 0 else 'unknown'}")
            continue

    return personData

def displayPerson(id, personData): # in this section what we will be achieving is displaying the users ID
    try:
        name, birthday = personData[id]
        print(f"Person #{id} is {name} with a birthday of {birthday.strftime('%Y%m%d')}.")
    except KeyError:
        print(f"No user with the ID #{id}.")

def main():

    """What's happening here is that it's setting up the logging and 
    basically able to handle the data and download the process and display the info that is provided """

    parser = argparse.ArgumentParser(description="Launch and display CSV data")
    parser.add_argument('url', nargs='?', default="https://s3.amazonaws.com/cuny-is211-spring2015/birthdays100.csv",
                        help="URL to the CSV file")
    args = parser.parse_args()

    """we will be addingthe argument and this is usually for the URL that connected to the CSV file """

    logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format='%(message)s'
)
    """this section will be checking for error.log and anything that passes through as error will be logged though meaning recorded"""
    try:
        csvData = downloadData(args.url)
        if csvData is None:
            print(f"Error: Unable to retrieve data from {args.url}.")
            return
        
        personData = processData(csvData)
        if not personData:
            print("Error: Could not process data.")
            return
    except Exception as error:
        print(f"Error: {error}")
        return
    
    """We will be using this to check if the CSV file has gone through but if not it will give us an error
    so using this would be able to determine if the data is successful if not then it would raise an error."""

    while True:
        id_input = input("Input ID (0 or a negative number to exit): ")
        if id_input.lstrip('-').isdigit():  
            user_id = int(id_input)
            if user_id <= 0:
                print("Exiting...")
                break
            displayPerson(user_id, personData)
        else:
            print("Error: Please input a valid integer.")

    """in this section what is happening is there is an loop, by doing this we will be able to input an ID and then with the following programming we could check if the 
    interger is valid or not, and then if user_id <=0 is input then anything with a 0 or negative would exit the program  """

if __name__ == "__main__":
    main()



    