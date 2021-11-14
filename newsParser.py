from bs4 import BeautifulSoup
import requests
import config

def getNews():
    """
    Retrieves news by parsing yandex.ru
    """
    response = requests.get(config.news_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news = soup.find_all("span", {"class": "news__item-content"})
    news = soup.find_all("a", {"class": "news__item"})

    output = ""
    for new in news:
        output = output + "<a href='{}'>{}</a>".format(new.get('href'),new.get('aria-label')) + "\n\n"
    output = output + "Источник: yandex.ru"
    return output
