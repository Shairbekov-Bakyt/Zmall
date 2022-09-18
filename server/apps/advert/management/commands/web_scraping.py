from django.core.management.base import BaseCommand
from advert.web_scraping.salexy import salexy
from advert.web_scraping.doska import doska


class Command(BaseCommand):
    def handle(self, *args, **options):
        if options["salexy"]:
            salexy()
        elif options["doska"]:
            doska()

    def add_arguments(self, parser):
        parser.add_argument(
            "--salexy",
            action="store_true",
            help="web scraping site salexy",
        )
        parser.add_argument(
            "--doska",
            action="store_true",
            help="web scraping site doska",
        )
