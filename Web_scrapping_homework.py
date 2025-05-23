import requests
from bs4 import BeautifulSoup


KEYWORDS = ['дизайн', 'фото', 'web', 'python']


def get_article(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    return soup.find('article')


def search_articles(keywords):
    base_url = 'https://habr.com'
    url = f'{base_url}/ru/articles/'
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    snippets = soup.find_all('div', class_='tm-article-snippet')

    for snippet in snippets:
        link_tag = snippet.find('a', class_='tm-article-snippet__readmore')
        if not link_tag:
            continue
        article_url = base_url + link_tag.get('href')
        article = get_article(article_url)
        if article is None:
            continue
        time_tag = article.find('time')
        title_tag = article.find('h1')
        text = article.get_text().lower()
        for kw in keywords:
            if kw.lower() in text:
                print(
                    f"{kw.title()}\n"
                    f"{time_tag.text if time_tag else ''} - "
                    f"{title_tag.text if title_tag else ''} - "
                    f"{article_url}"
                )


if __name__ == '__main__':
    search_articles(KEYWORDS)
