#So we can pull data from websites
import requests
#Used to parse the data
from bs4 import BeautifulSoup
#Enables me to send emails
import smtplib
import time
#Enables threading
import threading
import tkinter as tk

class Scraper:

    def __init__(self, url_arr, items_current_price, items_last_price):
        self.url_arr = url_arr
        self.items_current_price = items_current_price
        self.items_last_price = items_last_price

    def main(self):
        self.set_interval(self.update_prices, 10)

    #Updates the prices with a regular interval
    def set_interval(self, func, sec):
        def func_wrapper():
            self.set_interval(func, sec)
            func()
        t = threading.Timer(sec, func_wrapper)
        t.start()
        return t

    def update_prices(self):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"}

        for url in self.url_arr:
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.content, "html.parser")

            item_name = soup.find(id="productTitle").get_text()
            item_name = item_name.replace("\n", "")

            try:
                item_price = soup.find(id="priceblock_ourprice").get_text() 
                item_price = item_price.replace(",", ".")
                item_price = item_price.replace('\xa0', '')
                item_price = float(item_price[:-2])
            except:
                item_price = 0
        

            self.items_current_price[item_name] = item_price

            if(len(self.url_arr) > 0):
                self.check_price()
            print(self.items_current_price)



    def get_price(self, url, currentlyMonitoring):
        #The website we scrape from
        self.url_arr.append(url)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"}


        #Requests data from page
        page = requests.get(url, headers=headers)
        #Parses the html of the page (All of it, but we only want price and potentially some other stuff)
        soup = BeautifulSoup(page.content, "html.parser")


        #formatting (did originally make a method for this but for some reason it didn't work half of the time so just kept it like this)
        item_name = soup.find(id="productTitle").get_text()
        item_name = item_name.replace("\n", "")


        try:
            item_price = soup.find(id="priceblock_ourprice").get_text() 
            item_price = item_price.replace(",", ".")
            item_price = item_price.replace('\xa0', '')
            item_price = float(item_price[:-2])
        except:
            item_price = ""

        #Since dictionaries doesn't support duplicate keys we don't have to check that the key has been entered before
        self.add_item(self.items_current_price, item_name, item_price, currentlyMonitoring)

    def add_item(self, items, item_name, item_price, currentlyMonitoring):
        self.items_current_price[item_name] = item_price

        #Fix this and the check price and the program is almost done
        currentlyMonitoring.insert("end", item_name)



    #Compares the current price to what it was before and sends an email if it has gone down
    def check_price(self):
        for item in self.items_current_price:
            if(self.items_current_price.get(item) < self.items_last_price.get(item, 0)):
                self.send_email()
            self.items_last_price[item] = self.items_current_price[item]


    def delete_item(self, URL, currentlyMonitoring):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"}
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")

        item_name = soup.find(id="productTitle").get_text()
        item_name = item_name.replace("\n", "")

        self.url_arr.remove(URL)
        self.items_current_price.pop(item_name)
        self.items_last_price.pop(item_name, None)
        currentlyMonitoring.delete("anchor")


    def send_email(self):
        #Gmails smtp server and port
        server = smtplib.SMTP("smtp.gmail.com", 587)
        #Used to identify itself when connecting to another email server to start the process of sending an email
        server.ehlo()
        #Encrypt connection
        server.starttls()
        server.ehlo()

        server.login("kevinjeryd01@gmail.com", "INSERT YOUR PASSWORD HERE")

        subject = "An item you are monitoring has fallen in price"
        body = "The product in question is : https://www.amazon.se/Redken-Stylinglera-Rough-Clay-20/dp/B00IZPNYSW/ref=sr_1_1?dchild=1&keywords=redken+rough+clay+20&qid=1616514443&sr=8-1"

        msg = f"Subject: {subject}\n\n{body}"

        server.sendmail("kevinjeryd01@gmail.com", "kevinjeryd01@gmail.com", msg)

        server.quit()
