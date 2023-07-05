import urllib.request
import requests
import re
from PIL import Image
from bs4 import BeautifulSoup
import os
clear = lambda: os.system('cls')


while True:

    clear()
    brand = input("Enter brand: ")
    model = input("Enter model: ")

    cars = []
    prices = []
    years = []
    images = []

    for i in range(3):
        URL = "https://m.mobile.bg/results?pubtype=1&marka={}&model={}&currency=%D0%BB%D0%B2.&sort=1&nup=0~1&slink=sy7jbk&page={}".format(brand, model, i)
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        
        cars += soup.find_all(string=re.compile("^{}".format(brand)))
        prices += soup.find_all("div", class_="price")
        years += soup.body.find_all("div", class_="info")
        images += soup.find_all("img", attrs={"loading":"lazy"})

    price = 0
    year = 0

    for car in cars:
        if len(car) < 50:
            if years[year].string[0] == 'Ц':
                year+=1
            print(str(price+1) + ". " + car.string.strip() + " - " + prices[price].text.strip() + " - " + years[year].text.strip())
            price+=1
            year+=1

    for image in images:
        if image["src"].find("https") != -1:
            images.remove(image)

    while True:
        
        i = input("\n\nSelect a car to view or press ENTER to search again...  ")

        if i == "": #If ENTER is pressed
            break
        elif len(cars) > 1 and int(i) >= 1 and int(i) <= len(cars)-3:
            urllib.request.urlretrieve("https:" + images[int(i)-1]["src"], "image.png")
            
            img = Image.open("image.png")
            img.show()
        else:
            print("Invalid number!")
