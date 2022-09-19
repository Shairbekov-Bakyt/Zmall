import requests
from bs4 import BeautifulSoup

from advert.models import Category, SubCategory, City, Advert, AdvertImage
from user.models import CustomUser
from advert.utils import get_price_from_description
from config.celery import app


main_url = "https://salexy.kg/bishkek/rabota"
page_url = "?page="


def setUp():
    owner = CustomUser.objects.get_or_create(
        first_name="test",
        last_name="test",
        phone_number="+996999312292",
        email="test@gmail.com",
    )[0]
    category = Category.objects.get_or_create(icon="icon.png", name="rabota")[0]
    sub_cateogry = SubCategory.objects.get_or_create(category=category, name="rabota")[
        0
    ]
    city = City.objects.get_or_create(name="Bishkek")[0]
    return {"category": category, "sub": sub_cateogry, "city": city, "owner": owner}


def get_html(url: str) -> str:
    response = requests.get(url)
    return response.text


def get_page_data(html: str) -> None:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("ul", class_="product-list").find_all("li", class_="")
    for element in table:
        title = (
            element.find("div", class_="content")
            .find("div", class_="top-info")
            .find("div", class_="info-content")
            .find("div", class_="title")
            .text
        )
        price = (
            element.find("div", class_="content")
            .find("div", class_="top-info")
            .find("div", class_="info-content")
            .find("div", class_="price")
            .text.strip()
        )
        description = (
            element.find("div", class_="content")
            .find("div", class_="top-info")
            .find("div", class_="info-content")
            .find("div", class_="description")
            .text
        )
        img = element.find("div", class_="img-holder").find("a").find("img").get("src")
        price = get_price_from_description(price)
        setup = setUp()
        data = {
            "owner": setup["owner"],
            "name": title,
            "start_price": price,
            "end_price": price,
            "email": "otsasi991@gmail.com",
            "wa_number": "+996999312292",
            "description": description,
            "category": setup["category"],
            "sub_category": setup["sub"],
            "city": setup["city"],
            "status": "act",
        }
        advert = Advert.objects.update_or_create(**data)
        image = AdvertImage.objects.update_or_create(advert_id=advert.id, image=img)
        if img.startswith("https://salexy.kg/"):
            image.get_remote_image(img)


@app.task
def salexy():
    html = get_html(main_url)
    get_page_data(html)
    for each_page in range(1, 4):
        url_gen = main_url + page_url + str(each_page)
        html = get_html(url_gen)
        get_page_data(html)
