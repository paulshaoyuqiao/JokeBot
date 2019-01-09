# Author: Paul Shao

# Functionality: Methods for Fetching Data from Reddit Posts.

# Importing necessary dependencies and libraries
import requests, json, csv, os
from Utils import restart_bot, contain_prefixes

# Declaring necessary constants.
CUSTOMIZED_HEADERS = {'User-agent': 'jokebot beta - v1'}
ACCEPTABLE_PREFIXES = ['what', 'how', 'why']

def throw_exception(exception, error_type=''):
    '''
    Util Method for throwing an exception and restarting the Jokebot.
    @Parameters:
        exception => the exception (stack trace).
        error_type => the type of exception (human readable).
    @Returns:
        input for the main function deliver_jokes()
    '''
    print('Error {}: \n'.format(error_type))
    print('Here is the stack trace from the Python Interpreter: {} \n'.format(exception))
    print('Exiting Reddit posts fetch mode... \n')
    return restart_bot()

def filter_posts(res):
    '''
    Filter Reddit Posts and Save the Data to a local CSV file.
    @Parameters:
        res => the json response object (as a Python dictionary).
    @Returns:
        name the csv files.
    '''
    # Clears previous version of the fetched csv file to allow updated content.
    try:
        os.remove('fetched.csv')
    except FileNotFoundError as e:
        pass
    # Filtering Content.
    try:
        list_res = res['data']['children']
    except KeyError as e:
        return throw_exception(e, 'Key {} Not Found'.format('data/children'))
    with open('fetched.csv', 'w', newline='') as r:
        f = csv.writer(r, quoting = csv.QUOTE_ALL)
        f.writerow(['prompt', 'punchline'])
        for single_res in list_res:
            try:
                data = single_res['data']
                over_18 = data['over_18']
                title = data['title']
                response = data['selftext']
            except KeyError as e:
                continue
            if (not over_18) and contain_prefixes(ACCEPTABLE_PREFIXES, title):
                f.writerow([title, response])
        return 'fetched.csv'

def fetch_filtered_posts():
    '''
    Fetches and returns the csv file with all the satisfactory Reddit jokes.
    '''
    try:
        res = requests.get('http://www.reddit.com/r/dadjokes.json', headers=CUSTOMIZED_HEADERS).json()
    except ConnectionError as e:
        return throw_exception(e, 'Connecting to the Web')
    except ValueError as e:
        return throw_exception(e, 'Interpreting and Decoding the HTTP Response')
    return filter_posts(res)
