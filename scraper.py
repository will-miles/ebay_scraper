from bs4 import BeautifulSoup
import requests
import csv

def get_page(url):
    response = requests.get(url)
    if not response.ok:
        print('Server responded:', response.status_code)
        soup = False
    else:
        soup = BeautifulSoup(response.text, 'lxml')
    return soup

def get_data(soup):

    page_data = []
    try:
        listings = soup.find_all("div", class_="s-item__info clearfix")
    except:
        listings = []

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
    url = 'https://www.ebay.co.uk/sch/i.html?_nkw=rtx+3080&pgn='
    i = 1

    while i <= 10:
        page = get_page(url + str(i))
        if page:
            write_csv(get_data(page))
        i += 1

if __name__ == '__main__':
    main()