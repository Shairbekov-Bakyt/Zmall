from django.core.management.base import BaseCommand
from web_scraping.salexy import main


class Command(BaseCommand):
    help = """
            command web scraping will scraping site kivano
          """

    def handle(self, *args, **kwargs):
        main()
