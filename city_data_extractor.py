# For web scraping

import requests
from bs4 import BeautifulSoup
import pandas as pd

# To print colored text in terminal
import colorama
from colorama import Fore, Back, Style

colorama.init()

# Others
import unidecode
from markdownify import markdownify as md

def extract_city_data(city_url: str):
    """Extract the required table from Numbeo"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(city_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', {'class': 'data_wide_table'})
    if table:
        # Remove the third column from the table
        for row in table.find_all('tr'):
            th = row.find_all('th')
            if len(th) > 2:
                th[2].decompose()
            td = row.find_all('td')
            if len(td) > 2:
                td[2].decompose()

        # Remove hyperlink references
        for a in table.find_all('a'):
            a.replace_with(a.text)

        # Convert the modified HTML table to Markdown
        markdown_table = md(str(table))
        return markdown_table
    return None

if __name__ == "__main__":
    # Example usage
    city_url = "https://www.numbeo.com/cost-of-living/in/Auburn"
    city_data = extract_city_data(city_url)
    if city_data:
        print(Fore.GREEN + "City Data Extracted Successfully!" + Style.RESET_ALL)
        print(city_data)
    else:
        print(Fore.RED + "Failed to extract city data." + Style.RESET_ALL)