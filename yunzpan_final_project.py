import json
import csv
import requests
import webbrowser
from datetime import datetime
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from subprocess import Popen



CACHE_FILENAME = "indeed_cache.json"
CACHE_DICT = {}
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47'
}

def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 



def get_url(position, location):
    """
    create unique url link based on position and location name
    
    """
    template = 'https://www.indeed.com/jobs?q={}&l={}'
    url = template.format(position, location)
    return url

def make_request_with_cache(url,headers = {}):
    '''Check the cache for a saved result for this url. 
    If the result is found, return it. Otherwise send a new 
    request, save it, then return it.
    ----------
    url: string
        The URL for the http address

    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''
    # request_key = get_url(url,headers = headers)
    if url in CACHE_DICT.keys():
        print('Using Cache...')
        return CACHE_DICT[url]
    else:
        print('Fetching...')
        response = requests.get(url,headers = headers)
        CACHE_DICT[url]=response.text
        save_cache(CACHE_DICT)
        return CACHE_DICT[url]

def get_record(card):
    '''Extract job date from a single job record '''
    # open_cache()
    card_dict = {}
    # source = make_request_with_cache(card_url)
    # soup = BeautifulSoup(source,'lxml')
    # for card in soup.find_all('div', 'jobsearch-SerpJobCard'):
        
    atag = card.h2.a
    try:
        card_dict['Job_Title'] = atag.get('title')
    except AttributeError:
        card_dict['Job_Title'] = ''
    try:
        card_dict['Company'] = card.find('span', 'company').text.strip()
    except AttributeError:
        card_dict['Company'] = ''
    try:
        card_dict['Location'] = card.find('div', 'recJobLoc').get('data-rc-loc')
    except AttributeError:
        card_dict['Location'] = ''
    try:
        card_dict['Job_Summary'] = card.find('div', 'summary').text.strip()
    except AttributeError:
        card_dict['Job_Summary'] = ''
    try:
        card_dict['Post_Date'] = card.find('span', 'date').text.strip()
    except AttributeError:
        card_dict['Post_Date'] = ''
    try:
        card_dict['Salary'] = card.find('span', 'salarytext').text.strip()
    except AttributeError:
        card_dict['Salary'] = ''
    
    card_dict['Extract_Date'] = datetime.today().strftime('%Y-%m-%d')
    card_dict['Job_Url'] = 'https://www.indeed.com' + atag.get('href')

    return card_dict

def display_info(List):
    i=1
    for card_dic in List:
        print(f"\n")
        print(f"[{i}] {card_dic}")
        i+=1






def main():
    # Run the main program reouting
      # creating the record list
    while True:
        
        user_input1 = input("Hello! Do you want to make a job search? Please type 'Y' or 'N' >>>   ").lower()
        if user_input1 == 'y': 
            position = input("Please type the job position (e.g. data analyst) >   ").lower()
            location = input("Please type the location :city and state (e.g. ann arbor, mi) >   ").lower()
            url = get_url(position, location)  # create the url while passing in the position and location.
            records = []
            
            while True:
                response = make_request_with_cache(url, headers=headers)
                soup = BeautifulSoup(response, 'html.parser')
                cards = soup.find_all('div', 'jobsearch-SerpJobCard')

                for card in cards:
                    record = get_record(card)
                    records.append(record)
                    
                 

                try:
                    url='https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
                    delay = randint(1, 10)
                    sleep(delay)
                except AttributeError:
                    break



            field_names = ['Job_Title', 'Company', 'Location', 'Job_Summary', 'Post_Date', 'Salary','Extract_Date',  'Job_Url']
            with open('indeed.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f,fieldnames=field_names)
                writer.writeheader()
                for data in records:
                    writer.writerow(data)



            
            ask_display = input("Do you want to see the results in excel? Y/N  >>>   ").lower()
            while True:
                if ask_display == 'y': 
                    Popen('indeed.csv', shell=True)
                    break

                elif ask_display == 'n':
                    break
                else:
                    print("invalid input")
                    ask_display = input("Do you want to see the results in excel? Y/N  >>>   ")
            display_info(records)
            user_input = input("Do you want to review the job detail? Type number to open the browser or 'no' >>>    ")
            while True:
                if user_input == 'no':
                    # user_input1 = input("Hello! Do you want to make a job search? Please type 'Y' or 'N' >>>   ").lower()
                    break

                
                elif user_input != 'no':
                    try:
                        num = int(user_input)
                        if num in range(len(records)+1):
                            webbrowser.open_new_tab(records[num-1]['Job_Url'])
                            display_info(records)
                            user_input = input("Do you want to review the job detail? Type number to open the browser or 'no' >>>    ")
                        else:
                            print("Number out of range!")
                            user_input = input("Do you want to review the job detail? Type number to open the browser or 'no' >>>    ")
                    except ValueError:
                        # if user_input == 'no':
                        #     user_input1 = input("Hello! Do you want to make a job search? Please type 'Y' or 'N' >>>   ").lower()
                        #     break
                        # else:
                        print("Invalid input")
                        user_input = input("Do you want to review the job detail? Type number to open the browser or 'no' >>>    ")
                # elif user_input == 'no':
                    
            
        
        elif user_input1.isalpha() is False:
            print("This is not a valid input")
            user_input1 = input("Hello! Do you want to make a job search? Please type 'Y' or 'N' >>>   ").lower()

        elif user_input1 == 'n':
            print("Thank you")
            break


       

main()
