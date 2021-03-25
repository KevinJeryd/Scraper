from scraper import Scraper
from view import ScraperGUI

def main():
    url_arr = []
    items_current_price = {}
    items_last_price = {}

    scraper = Scraper(url_arr, items_current_price, items_last_price)
    view = ScraperGUI(scraper)

    view.GUI()

main() 