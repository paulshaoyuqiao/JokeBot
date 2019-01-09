# Author: Paul Shao

# Functionality: Util Methods for the Jokebot.

# Importing necessary dependencies and libraries
import time, csv, sys

# Declaring necessary constants.
VALID_COMMANDS = ['next', 'quit']

def restart_bot(prompt='', additional_msg=''):
    '''
    Util method for restarting the Jokebot.
    @Parameters:
        prompt => the prompt to provide to the user to ask for input.
        additional_msg => additional message to provide to the user upon providing input.
    @Returns:
        the user input.
    '''
    if prompt == '':
        reinitialize_input = input('Thanks for continuing using jokebot! Please provide a csv filename or simply press enter to fetch from Reddit posts. \n')
    else:
        reinitialize_input = input('{} \n'.format(prompt))
    if not additional_msg == '':
        print('{} \n'.format(additional_msg))
    return str(reinitialize_input).strip()

def contain_prefixes(prefix, s):
    '''
    Checks if a given string s contains any of the strings in the given list as a prefix.
    @Parameters:
        prefix => a list of all available prefixes.
        s => a given string.
    @Returns:
        whether the string contains any satisfactory prefix.
    '''
    s = s.lower()
    for p in prefix:
        if s.startswith(p):
            return True
    return False

def read_and_deliver(joke_file):
    '''
    Reads in a CSV file and delivers all the jokes one by one based on user input.
    @Parameters:
        joke_file => the CSV file with all the jokes in it.
    '''
    with open(joke_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count > 0:
                prompt, punchline = row[0], row[1]
                print('\n' + prompt)
                time.sleep(2)
                user_command = input(punchline + '\n\n' + 'Please provide your next command. Enter next to move on to the next joke or quit to shut down the Jokebot...' + '\n')
                while str(user_command).strip().lower() not in VALID_COMMANDS:
                    user_command = input('Error: the given command cannot be found. Please provide either next to move on to the next joke or quit to shut down the joke bot...' + '\n')
                if user_command == 'quit':
                    print('Thanks for using Jokebot! Shutting down... \n')
                    sys.exit()
            line_count += 1
