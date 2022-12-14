#https://learnpython.com/blog/
# https://docs.google.com/spreadsheets/d/1pYKu6C1IkkCmDl5Q8Rn1Sc4p_IhKPm1VXJkdoXSBgs8/edit?usp=sharing
from requests_html import HTML
from requests_html import HTMLSession
import pandas as pd
parse_data = []
base_url="https://learnpython.com"

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36' }
def make_request(url):
    session = HTMLSession()
    res = session.get(url)
    return res

def parse(res):
    articles= res.html.find('div.blog-list-summary')

    for article in articles:
        blog_title = article.find('h2.blog-list-summary-title',first=True).text
        blog_post_date = article.find('div.blog-post-date',first=True).text
        blog_post_author = article.find('span.summary-blog-post-meta-list-author-name',first=True).text
        blog_post_summary = article.find('a.summary__content',first=True).text
        blog_post_url = base_url+article.find('a.summary__content',first=True).attrs['href']

        parse_data.append(
            {
                'blog_title':blog_title,
                'blog_post_date':blog_post_date,
                'blog_post_author':blog_post_author,
                'blog_post_summary':blog_post_summary,
                'blog_post_url':blog_post_url,

            }
        )

    #I tried pagination but it didn't work

    # l = res.html.find('ul.pagination',first=True)
    # link = l.find('li.page-item a.page-link')
    # next_page = link[3].attrs['href']
    # if next_page is not None:
    #     try:
    #         request_url = base_url+next_page
    #         r = make_request(request_url)
    #         parse(r)
    #     except:
    #         print("No more pages")

#deploying
#instead used safe method. upadate may come later
for i in range(1,26):
    try:
        res = make_request(f"https://learnpython.com/blog/page/{i}/")
        parse(res)
    except:
        print("No more pages")


df = pd.DataFrame(parse_data)
df.to_csv('learpython.csv', index = False, encoding='utf-8')
print(df)


print(f"Scraped Total items {len(parse_data)}")
