from bs4 import BeautifulSoup
import requests
import csv

def get_page(url):
    # Accepts url of page to be scraped
    # Returns soup object of requested page html
    response = requests.get(url)

    if not response.ok:
        print('Server responded:', response.status_code)
        soup = False
    else:
        soup = BeautifulSoup(response.text, 'lxml')

    return soup

def get_data(soup):
    # Acceptes soup object of html to scrape
    # Returns list of item dicts
    try:
        listings = soup.find_all("div", class_="s-item__info clearfix")
    except:
        listings = []

    page_data = []

    for item in listings:

        price = item.find('span', class_='s-item__price').text
        title = item.find('a', class_='s-item__link').text
        link  = item.find('a', class_='s-item__link').get('href')

        item_data = {
            'price': price,
            'title': title,
            'link': link
        }
        
        page_data.append(item_data)

    return page_data

def write_csv(data):
    # Accepst list of item dicts
    # Writes list data to outout.csv
    with open('output.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)

        for row in data:
            writer.writerow(
                [
                    row['title'],
                    row['price'],
                    row['link']
                ]
            )

def main():
    # Funtion to scrape first 10 pages of an ebay search
    # Writes the found: title, price anfd link to output.csv
    url = 'https://www.ebay.co.uk/sch/i.html?_nkw=rtx+3080&pgn='
    i   = 1

    while i <= 10:
        page = get_page(url + str(i))
        if page:
            write_csv(get_data(page))
        i += 1

if __name__ == '__main__':
    main()