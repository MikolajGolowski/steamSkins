import pandas as pd
import time

import seaborn as sns

from selenium import webdriver

from bs4 import BeautifulSoup

names = ["hkp2000", "glock","fiveseven", "deagle", "p250", "tec9", "usp_silencer"]

ileStron = [21, 28, 24, 33, 28, 24, 23]

dane = []

setToLast = False

for i in range(0, len(names)):
    if not setToLast:
        page_number = 1
    else:
        page_number = ileStron[i]
        setToLast = False
    infos = []
    back = False
    while(1):
        adress = f"https://steamcommunity.com/market/search?q=&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=tag_weapon_{names[i]}&appid=730#p{page_number}_price_desc"
        print(f'Pobieranie strony {page_number} {names[i]}')
        print(adress)
        try:
            browser = webdriver.Chrome('C:\PATH\chromedriver')
            browser.get(adress)
            time.sleep(10)
            processed_page = BeautifulSoup(browser.page_source, 'html.parser')
            if ("You've made too many requests recently. Please wait and try your request again later." in browser.page_source or "Dokonano zbyt wielu żądań. Proszę poczekać i spróbować później." in browser.page_source):
                print('429 error - czekam 3 minuty')
                time.sleep(180)
                if not back:
                    if(page_number != 1):
                        page_number -= 1
                    else:
                        i -= 1
                        setToLast = True
                    back = True
            else:
                back = False
                infos += processed_page.find_all(class_='normal_price')
                if(page_number == ileStron[i]):
                    break
                page_number += 1
            #if(page_number == 3):
            #break
        except Exception as e:
            print(e)
            page_number = page_number - 1
            pass

    prices1 = []
    prices = []

    for info in infos:
        prices1 += info.find_all(class_='normal_price')

    for price in prices1:
        daneBroni = {}
        daneBroni['bron'] = names[i]
        daneBroni['cena'] = float(price.text.replace('$', '').replace(' USD', '').replace(',',''))
        dane.append(daneBroni)


df = pd.DataFrame.from_dict(dane)
df.head()

sns.catplot(x="bron", y="cena", kind="violin", data=df).savefig('img.pdf')
sns.catplot(x="bron", y="cena", kind="violin", data=df[df.cena < 100]).savefig('img2.pdf')
sns.catplot(x="bron", y="cena", kind="violin", data=df[df.cena < 10]).savefig('img3.pdf')
sns.catplot(x="bron", y="cena", kind="violin", data=df[df.cena < 50]).savefig('img4.pdf')