import re
from bs4 import BeautifulSoup
import requests
import cssutils

from web_scraping.salexy import setUp
from advert.models import Advert, AdvertImage
from config.celery import app

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.160 YaBrowser/22.5.3.673 Yowser/2.5 Safari/537.36"
}

URL = 'http://resume.doska.kg/vacancy/'


def get_price_from_description(data: str) -> int:
    new_data = re.findall(r"(^|\\s)([0-9]+)($|\\s)", data)
    if new_data:
        return int(new_data[0][1])
    return 0


def get_html(url: str) -> str:
    response = requests.get(url, headers=headers)
    return response.text


def get_page_data(html: str) -> None:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find('div', class_="mp_last_items_block2").find_all('div', class_='list_full')
    for element in table:
        title = (
            element.find("div", class_="list_full_title")
            .find("a", class_="title_url").contents[0]
        )
        price = (
            element.find("div", class_="list_full_price_date")
            .find("div", class_="list_full_price")
            .text.strip()
        )
        description = (
            element.find("div", class_="list_full_title")
            .find("a", class_="title_url").text.strip()
        )
        try:
            img = element.find('div', class_='list_full_photo')['style']
            style = cssutils.parseStyle(img)
            url = style['background-image']
            img = 'http:'+url.replace('url(', '').replace(')', '')
        except KeyError:
            img = ''

        setup = setUp()
        price = get_price_from_description(price)
        data = {
            "owner": setup["owner"],
            "name": title,
            "start_price": price if price != '' else 0,
            "end_price": price if price != '' else 0,
            "email": "otsasi991@gmail.com",
            "wa_number": "+996999312292",
            "description": description,
            "category": setup["category"],
            "sub_category": setup["sub"],
            "city": setup["city"],
            'status': "act",
        }
        advert = Advert.objects.update_or_create(**data)

        image = AdvertImage.objects.update_or_create(advert_id=advert.id, image=img)
        if img.startswith('http://static.akipress.org'):
            image.get_remote_image(img)
    
@app.task

def doska():
    get_page_data(get_html(URL))
