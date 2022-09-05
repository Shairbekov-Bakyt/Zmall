from django.core.management.base import BaseCommand
from web_scraping.web_scraping import main


class Command(BaseCommand):
    help = """
            command web scraping will scraping site kivano
          """

    def handle(self, *args, **kwargs):
        main()
