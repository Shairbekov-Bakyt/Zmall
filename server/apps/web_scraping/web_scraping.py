import requests
import csv
from bs4 import BeautifulSoup
import datetime

main_url = 'https://www.kivano.kg/mobilnye-telefony'
page_url = "?page="


def get_html(url: str) -> str:
    response = requests.get(url)
    return response.text


def get_total_pages(html: str) -> int:
    soup = BeautifulSoup(html, "html.parser")
    pages = soup.find('div', class_='pager-wrap').find_all('a')[-1].get("href")
    total_pages = pages.split("=")[1]
    return int(total_pages)


def write_csv(data: dict) -> None:
    with open('kivano.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['title'],
                         data['price'],
                         data['img']))


def get_page_data(html: str) -> None:
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('div', class_='list-view').find_all('div', class_='item')

    for element in table:
        title = element.find('div', class_='listbox_title').find('a').text
        price = element.find('div', class_='listbox_price').find('strong').text.strip()
        img = element.find('div', class_='listbox_img').find('img').get('src')
        full_img = 'https://www.kivano.kg' + img

        data = {'title': title,
                'price': price,
                'img': full_img}

        write_csv(data)


def main():
    start = datetime.datetime.now()
    total_pages = get_total_pages(get_html(main_url))

    for each_page in range(1, total_pages + 1):
        url_gen = main_url + page_url + str(each_page)
        html = get_html(url_gen)
        get_page_data(html)
    end = datetime.datetime.now()
    print('Completed in', end - start)


