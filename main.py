# Creator LE
# Time 2022/3/24 23:55
# coding=UTF-8


from crawl_lib import *
from book_insert import *



if __name__ == '__main__':

    urlfinished = []
    urlrepo = ['https://book.douban.com/subject/26763973/']

    count = 0

    while count <= 100:
        url = urlrepo.pop(0)
        book, urllist = getbook(url)
        for item in urllist:
            if item not in urlfinished:
                urlrepo.append(item)
        if url not in urlfinished:
            urlfinished.append(url)
            print(book['title'])
            insert_book(book)
            count = count + 1

