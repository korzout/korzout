from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier

@route("/")
@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    # PUT YOUR CODE HERE
    with session.begin() as s:
        article = s.query(News).filter(News.id == request.query.id).first()
        article.label = request.query.label
        s.commit()
    redirect("/news")


@route("/update")
def update_news():
    news = get_news("https://news.ycombinator.com/newest")
    s = session()
    for new in news:
        if not s.query(News).filter(News.author == new["author"], News.title == new["title"]).all():
            s.add(
                News(
                    author=new["author"],
                    title=new["title"],
                    points=new["points"],
                    comments=new["comments"],
                    url=new["url"],
                )
            )
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():



    s = session()
    marked_news = s.query(News).filter(News.label != None).all()
    marked_news = [[new.title, new.label] for new in marked_news]

    x_train = [a[0] for a in marked_news]

    y_train = [a[1] for a in marked_news]

    model = NaiveBayesClassifier(alpha=0.1)
    model.fit(x_train, y_train)

    news = s.query(News).filter(News.label is None).all()
    news_ids = [new.id for new in news]
    news = [new.title for new in news]
    predicts = model.predict(news)

    classified_news = {"good": [], "maybe": [], "never": []}

    for i, predict in enumerate(predicts):
        classified_news[predict].append(news_ids[i])

    rows = []
    for label in ["good", "maybe", "never"]:
        for id in classified_news[label]:
            rows.append(s.query(News).filter(News.id == id).first())
    return template("news_template", rows=rows)


if __name__ == "__main__":
    run(host="localhost", port=8080)

