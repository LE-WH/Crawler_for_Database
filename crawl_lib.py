# Creator LE
# Time 2022/3/24 23:32
# coding=UTF-8

# this is library intends to handle interaction with web

import urllib.request as req
import bs4


def getdata(url):
    # 建立一个request物件，附加headers
    request = req.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/99.0.4844.51 Safari/537.36)'})

    with req.urlopen(request) as response:
        data = response.read().decode('utf-8')

    return data


def getbook(url):
    '''

    cons:

    :param url:
    :return: (book, urllist)
    book = {
                    must            PS
    title           Y
    ISBN            Y
    author          N
    translator      N
    publisher       N
    time            N               sometimes 2022-2 sometimes 2022-2-2
    price           N               sometimes with 元 sometimes not
    score           N
    intro           N
    author_intro    N
    }
    urllist = []
    '''
    data = getdata(url)
    raw = bs4.BeautifulSoup(data, 'html.parser')

    book = {'title': raw.find('span', property="v:itemreviewed").string}  # contains all info
    urllist = []

    # find other info
    info = raw.find('div', id='info')
    related = raw.find('div', class_='related_info')

    try:  # 有的页面信息不全
        book['author'] = info.find(text=' 作者').next_element.next_element.string
    except:
        pass

    try:
        book['translator'] = info.find(text=' 译者').next_element.next_element.string
    except:
        pass

    try:
        book['publisher'] = info.find(text='出版社:').next_element.next_element.string
    except:
        pass

    try:
        book['time'] = info.find(text='出版年:').next_element.strip()
    except:
        pass

    try:
        book['price'] = info.find(text='定价:').next_element.strip()
    except:
        pass

    try:
        book['ISBN'] = info.find(text='ISBN:').next_element.strip()
    except:
        print("Error: can't find ISBN")
    try:
        book['score'] = float(raw.find(property="v:average").string)
    except:
        pass

    try:
        link_report = related.find('div', id='link-report')
        book['intro'] = '\n'.join(str(e.string) for e in link_report.find('div', class_='intro').find_all('p'))
        try:
            hidden = link_report.find('span', class_='all hidden')
            book['intro'] = ('\n'.join(str(e.string) for e in hidden.find('div', class_='intro').find_all('p')))
        except:
            pass
    except:
        pass

    try:
        info = related.find('span', string='作者简介').next_element.next_element.next_element.next_element
        book['author_intro'] = '\n'.join(str(e.string) for e in info.find('div', class_='intro').find_all('p'))
        book['author_intro'] = book['author_intro'].replace('(展开全部)', '')
    except:
        pass

    try:
        more = related.find('div', class_='block5 subject_show knnlike').find('div', class_='content clearfix')
        all_url = more.findAll('a')
        for i in range(len(all_url)):
            if i % 2 == 0:
                urllist.append(all_url[i]["href"])
    except:
        pass

    return book, urllist

