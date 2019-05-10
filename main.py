
from bs4 import BeautifulSoup
import requests
import html2text
import csv
import time
import numpy as np


def fetch_results(search_term, number_results, language_code):
    escaped_search_term = search_term.replace(' ', '+')

    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.\
        format(escaped_search_term, number_results, language_code)
    response = requests.get(google_url, headers=USER_AGENT)
    response.raise_for_status()

    return search_term, response.text


# %% md
### Helper function that converts a list of labels to '/' separated values
# %%
def list_string(mylist):
    ret_str = str(mylist[0])
    remaining_list = mylist[1:]
    for item in remaining_list:
        ret_str += '/' + str(item)
    return ret_str


# %% md
### Function that gets the labels for a given address
# %%
def get_labels(address, depth=5):
    '''
    address: the address we wish to
    depth: the number of websites to return
    '''
    keyword, html = fetch_results(address, depth, 'en')
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find_all('div', {'class': 'r'})
    websites = []
    for div in divs:
        children = div.findChildren("a", recursive=False)
        for child in children: websites.append(child['href'])

    Labels_for_addresses = []
    for site in websites:
        url = site
        response = requests.get(url, headers=USER_AGENT)
        response.raise_for_status()
        html = response.text
        text = html2text.html2text(html)

        for Label in Labels:
            if Label not in Labels_for_addresses and Label in text:
                Labels_for_addresses.append(Label)
                continue

    return Labels_for_addresses



Labels = ['Exchange', 'Gambling', 'hosted wallet',
          'Merchant', 'online shopping store',
          'mining pools', 'mixing', 'tor',
          'ransomware', 'scam', 'smart contract',
          'bank', 'simple user']

USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

with open('new_data_h_1.csv') as f:
    firstColumn = [line.split(',')[0] for line in f]

data = firstColumn[1:len(firstColumn) - 1]
dataX = data[0:1000]
Assigned_Labels = {}
for address in dataX:
    a = time.perf_counter()
    Assigned_Labels[address] = get_labels(address)

    # delay so that we don't get banned from google due to too many requests
    b = time.perf_counter()
    if b - a < 2:
        time.sleep(2)

with open('people.csv', 'w', newline='') as writeFile:
    writer = csv.writer(writeFile)
    for key, val in Assigned_Labels.items():
        row = [key, list_string(val)]
        writer.writerow(row)