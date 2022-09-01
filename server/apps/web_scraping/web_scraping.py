import requests
from bs4 import BeautifulSoup

from advert.models import Category, SubCategory, City, Advert, AdvertImage
from user.models import CustomUser
from .utils import get_price_from_description

main_url = 'https://salexy.kg/bishkek/rabota'
page_url = "?page="


def setUp():
    owner = CustomUser.objects.get_or_create(first_name='test', last_name='test', phone_number='+996999312292', email='test@gmail.com')[0]
    category = Category.objects.get_or_create(icon='icon.png', name='rabota')[0]
    sub_cateogry = SubCategory.objects.get_or_create(category=category, name='rabota')[0]
    city = City.objects.get_or_create(name='Bishkek')[0]
    return {'category': category, 'sub': sub_cateogry, 'city': city, 'owner':owner}


def get_html(url: str) -> str:
    response = requests.get(url)
    return response.text


def get_page_data(html: str) -> None:
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('ul', class_='product-list').find_all('li', class_='')

    for element in table:
        title = element.find('div', class_='content').find('div', class_='top-info').find('div',
                                                                                          class_='info-content').find(
            'div', class_='title').text
        price = element.find('div', class_='content').find('div', class_='top-info').find('div',
                                                                                          class_='info-content').find(
            'div', class_='price').text.strip()
        description = element.find('div', class_='content').find('div', class_='top-info').find('div',
                                                                                                class_='info-content').find(
            'div', class_='description').text
        img = element.find('div', class_='img-holder').find('a').find('img').get('src')
        price = get_price_from_description(price)
        setup = setUp()
        data = {'owner': setup['owner'],
                'name': title,
                'to_price': price,
                'from_price': price,
                'email': 'otsasi991@gmail.com',
                'phone_number': '+996999312292',
                'wa_number': '+996999312292',
                'description': description,
                'category': setup['category'],
                'sub_category': setup['sub'],
                'city': setup['city']}
        advert = Advert.objects.create(**data)
        AdvertImage.objects.create(advert_id=advert, image=img)


def main():
    html = get_html(main_url)
    # print(html)
    get_page_data(html)
#

#
# def write_csv(data: dict) -> None:
#     with open('kivano.csv', 'a') as file:
#         writer = csv.writer(file)
#         writer.writerow((data['title'],
#                          data['price'],
#                          data['img']))
#
#
#
#
#
# def main():
#     start = datetime.datetime.now()
#     total_pages = get_total_pages(get_html(main_url))
#
#     for each_page in range(1, total_pages + 1):
#         url_gen = main_url + page_url + str(each_page)
#         html = get_html(url_gen)
#         get_page_data(html)
#     end = datetime.datetime.now()
#     print('Completed in', end - start)
#
#
