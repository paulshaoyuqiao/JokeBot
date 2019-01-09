# Author: Paul Shao

# Functionality: Main Script For Jokebot.

# Usage: To use, simply go into the directory of Jokebot.py and enter the command 'python Jokebot.py <csv file>' in the terminal.
#        Note that the argument <csv file> is completely optional. If no argument is provided, the bot will directly fetch from the Reddit posts.

# Importing necessary dependencies and libraries
import time, csv, os, sys, glob, sys
from Utils import restart_bot, read_and_deliver
from Fetch import fetch_filtered_posts

# Declaring necessary constants.
CSV_FILE_PATH = './{}'
VALID_COMMANDS = ['next', 'quit']
VALID_END_COMMANDS = ['Y', 'N']

def deliver_jokes(joke_file=''):
    '''
    Deliver jokes to the user through either a local csv files containing the jokes or fetching from Reddit posts.
    @Parameter:
        joke_file => the name of the csv file (It is highly recommended to have csv file in the same directory as the Jokebot script.)
    '''
    if joke_file is '':
        # Handles the case when no CSV file is provided.
        print("Fetching jokes from Reddit... \n")
        deliver_jokes(fetch_filtered_posts())
    else:
        # Handles the case when the CSV file doesn't exist in the current directory
        if not os.path.isfile(CSV_FILE_PATH.format(joke_file)):
            retry = str(input('The CSV file you have provided doesn\'t exist in the current directory. Do you want to try again? \n Acceptable Commands: Y for Yes / N for No / L to List all the potential csv files in the current directory. \n'))
            prompting_command, max_commands = 0, 1
            while prompting_command < max_commands:
                # Case I: N (No) => Shutting down Jokebot.
                if retry.upper().startswith('N'):
                    print('Thanks for using Jokebot! Shutting down...')
                    sys.exit()
                # Case II: L (List) => Listing all the available CSV files in the current directory.
                elif retry.upper().startswith('L'):
                    print('Below is a list of all the CSV files in the current directory: \n')
                    print(str([f for f in glob.glob('*.csv')]) + '\n')
                    retry = str(input('Please provide Y or N or L as your next command. \n Please re-enter your command below: \n'))
                    max_commands += 1
                # Case III: Y (Yes) => Restarting the whole joke-delivering process.
                elif retry.upper().startswith('Y'):
                    break
                # Case IV: The given commands cannot be recognized; reprompting the user to enter a correct command.
                else:
                    retry = str(input('Please make sure you provide either Y or L or N as the command. \n'))
                    max_commands += 1
            # Restarting the joke-delivering process.
            deliver_jokes(restart_bot('','Restarting Jokebot...'))
        try:
            # Parse through the CSV file and deliver the jokes one by one; accepting certain user commands per joke throughout the process.
            read_and_deliver(joke_file)
        # Handles the case when there is an error reading in the content of the CSV file.
        except IOError as e:
            print('Error: encountered issues while reading csv files. \n')
            deliver_jokes(restart_bot())
        # Handles the case when we've reached the end of the list of the jokes.
        print('You\'ve reached the end of all jokes. Do you want to continue using Jokebots?')
        end_command = input(' Acceptable Commands: Y to continue using by choosing to provide a CSV file or fetch from Reddit / N to exit the Jokebot. \n')
        end_command = str(end_command).strip().upper()[0]
        # Handles the case when the user command cannot be recognized; reprompting the user to enter a correct command.
        while end_command not in VALID_END_COMMANDS:
            end_command = input('Error: the given command cannot be found. Please provide a valid command. \n Acceptable Commands: Y to continue using by choosing to provide a CSV file or fetch from Reddit / N to exit the Jokebot. \n')
            end_command = str(end_command).strip().upper()[0]
        # Case I: N (No) => Shutting down Jokebot.
        if end_command == 'N':
            print('Thanks for using Jokebot! Shutting down... \n')
            sys.exit()
        # Case II: Y (Yes) => Restarting Jokebot for another round.
        else:
            deliver_jokes(restart_bot())

# Main Function
if __name__ == "__main__":
    # Case I: No arguments are provided to this method.
    if len(sys.argv) == 1:
        deliver_jokes('')
    # Case II: some CSV file is provided as an argument to the method.
    else:
        deliver_jokes(sys.argv[1].strip())