# Crawl data about books from the internet(taobao.com)

import requests
import re

headers = {
    'User-Agent': r'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
}

URL = 'https://book.douban.com/tag/%E6%97%A5%E6%9C%AC%E6%96%87%E5%AD%A6?start={}&type=T'


def get_data(URL):
    r = requests.get(URL, headers=headers)
    r.encoding = 'UTF8'
    return r.text


def get_des(url):
    r = requests.get(url, headers=headers)
    reg = re.compile('<p>(.*?)</p>')
    result = '\n'.join(re.findall(reg, r.text))
    print(result)
    return result


def clean_data(html):
    reg = re.compile('<li class="subject-item">([\s\S]*?)</li>')
    lis = re.findall(reg, html)
    for li in lis:
        reg_detail_url = re.compile('<a class="nbg" href="(.*?)"')
        book_url = re.findall(reg_detail_url, li)[0].strip()
        reg_pic_url = re.compile('<img class="" src="(.*?)"')
        reg_book_name = re.compile('<a href="{}" title="(.*?)"'.format(book_url))
        reg_pub = re.compile('<div class="pub">([\s\S]*?)</div>')
        reg_brief_des = re.compile('<p>([\s\S]*?)</p>')

        pic_url = re.findall(reg_pic_url, li)[0].strip()
        book_name = re.findall(reg_book_name, li)[0].strip()
        pub = re.findall(reg_pub, li)[0].strip()
        brief_des = re.findall(reg_brief_des, li)[0].strip()
        des = get_des(book_url)
        yield book_name, pic_url, pub, brief_des, des


def db_connect():
    import sqlite3
    conn = sqlite3.connect('db.sqlite')
    return conn


def main():

    with db_connect() as conn:
        count = 1
        for i in range(0, 100, 20):
            html = get_data(URL.format(i))
            gen_data = clean_data(html)
            for book_name, pic_url, pub, brief_des, des in gen_data:
                conn.execute("""INSERT INTO books(book_name, pic_url,
     pub, brief_des, des) VALUES(?, ?, ?, ?, ?)""", (book_name, pic_url, pub, brief_des, des))
                print('Inserting {}...'.format(count))
                conn.commit()
                count += 1




if __name__ == '__main__':
    main()
