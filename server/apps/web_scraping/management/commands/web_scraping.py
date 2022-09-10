from django.core.management.base import BaseCommand
from web_scraping.salexy import salexy
from web_scraping.doska import doska

class Command(BaseCommand):
    help = """
            command web scraping will scraping site kivano
          """

    def handle(self, *args, **kwargs):
        doska()
        salexy()
