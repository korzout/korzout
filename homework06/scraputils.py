import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """Extract news from a given web page"""
    news_list = []
    # lst = parser.select("a span")
    # lst = parser.body.findAll("span", class_="titleline")

    urls_list = parser.body.findAll("span", class_="sitestr")
    for i in range(len(urls_list)):
        urls_list[i] = urls_list[i].string

    titles_list = parser.body.findAll("span", class_="titleline")
    for i in range(len(titles_list)):
        titles_list[i] = titles_list[i].find("a").string

    names_list = parser.body.findAll("a", class_="hnuser")
    for i in range(len(names_list)):
        names_list[i] = names_list[i].string

    points_list = parser.body.findAll("span", class_="score")
    for i in range(len(points_list)):
        points_list[i] = int(points_list[i].string.split()[0])

    comments_list = parser.body.findAll("span", class_="subline")
    for i in range(len(comments_list)):
        com = comments_list[i].findAll("a")[-1].string.split("\xa0")[0]
        if com != "discuss":
            comments_list[i] = int(com)
        else:
            comments_list[i] = 0
    minlen = min(
        len(comments_list), len(points_list), len(names_list), len(titles_list), len(urls_list)
    )
    for i in range(minlen):
        d = {
            "author": names_list[i],
            "comments": comments_list[i],
            "points": points_list[i],
            "title": titles_list[i],
            "url": urls_list[i],
        }
        news_list.append(d)

    return news_list


def extract_next_page(parser):
    """Extract next page URL"""
    return parser.find("a", class_="morelink")["href"]


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
