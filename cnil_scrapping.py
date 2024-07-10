import requests
from bs4 import BeautifulSoup
import json
import time

# Before running this script, make sure to install the required packages:
# pip install requests beautifulsoup4

def scrape_page(url):
    # Send a GET request to the URL
    response = requests.get(url)

    all_links=[]
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Part 1: Extract pagination information
        # Find all elements with class "definition-liste-titre"
        definition_titles = soup.find_all(class_="definition-liste-titre")

        # Extract and print the links
        for title in definition_titles:
            link = title.find('a')
            if link:
                all_links.append(link['href'])     
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    return all_links
    
def get_definition(url):
    # Send a GET request to the URL
    response = requests.get(url)

    item={}

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the term and its definition
        term = soup.find(class_='ctn-gen-titre').text
        definition = soup.find(class_='field--type-text-with-summary')
        
        if term:
            item['term']=term
        if definition:
            paragraphs = definition.find_all('p')
            item['definition']='\n'.join([p.text for p in paragraphs])

    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

    return item

def main():

    all_links=[]
    # Process each link
    for n in range(0,13):
        print(f"Processing page {n}")
        url="https://www.cnil.fr/fr/intelligence-artificielle/glossaire-ia?page="+str(n)
        page_soup = scrape_page(url)
        all_links.extend(page_soup)
        time.sleep(1)
    
    all_defintions=[]
    # Process each link
    for link in all_links:
        definition=get_definition("https://www.cnil.fr/"+link)
        all_defintions.append(definition)
        print(f"Processed {definition['term']}")
        time.sleep(1)

    with open('cnil_glossary.json', 'w') as f:
        json.dump(all_defintions, f, indent=4)

    with open('cnil_glossary.html', 'w') as f:
        html = ""

        for item in all_defintions:
            html += f"<h2>{item['term'].strip()}</h2>"
            for p in item['definition'].split('\n'):
                html += f"<p>{p}</p>"
            
        f.write(html)


if __name__ == "__main__":
    main()