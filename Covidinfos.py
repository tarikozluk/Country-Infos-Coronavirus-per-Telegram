"""
    Coronavirus data mining from the site worldometers.info/coronavirus
    When there is no Beautiful Soup and requests libraries on your computer system for py documents
    https://pypi.org/project/beautifulsoup4/ => for Beautfiul Soup library
    https://pypi.org/project/requests/ => for requests library
    remind: You can use any telegram libraries(telepot, telebot or telegram). For the commands i used telegram.ext for the token management and sending message i used telebot
    Istanbul/Turkey
"""


import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler
from datetime import datetime
import telebot
import time

Botun_Tokeni="token of the your Bot"
ChatID = "Personal Chat ID"
Araci = telebot.TeleBot(Botun_Tokeni)
Bugun = str(datetime.now())
def vaka(bot, Update):
    dosya = open('gunlukVaka.txt', 'w')
    covidsitesi = "https://www.worldometers.info/coronavirus/"
    r = requests.get(covidsitesi)
    soup = BeautifulSoup(r.content, "html.parser")
    veri = soup.find_all("table", {"id": "main_table_countries_today"})
    Covid19GenelTablo = (veri[0].contents)[len(veri[0]) - 6]
    Covid19GenelTablo = Covid19GenelTablo.find_all("tr")
    print(len(Covid19GenelTablo))
    for covid in Covid19GenelTablo:
        ulke_isimleri = covid.find_all("a", {"class": "mt_a"})
        ulkeler = ulke_isimleri
        yenivaka = covid.find_all("td", {"style": "font-weight: bold; text-align:right;background-color:#FFEEAA;"})
        for j in ulkeler:
            print("\n")
            s = ulkeler[0].text
            for i in yenivaka:
                virusVeri = ("Ulke: " + s + " YeniVaka:" + yenivaka[0].text+"\n")
                time.sleep(1)
                dosya.write(virusVeri)
    dosya.close()
    YollanacakVeri= open(r'gunlukVaka.txt','rb')
    Araci.send_document(ChatID,YollanacakVeri)


def calistir():
    updater= Updater(Botun_Tokeni)
    dispatch=updater.dispatcher
    dispatch.add_handler(CommandHandler('gunlukVaka',vaka))
    updater.start_polling()
    updater.idle()


if __name__=='__main__':
    calistir()