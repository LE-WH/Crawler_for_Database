# Creator LE
# Time 2022/3/26 23:38
# coding=UTF-8

from instructions import *
import mysql.connector
import re
from datetime import date


def insert_book(book: dict):
    cnx = mysql.connector.connect(user='root', database='e-book', password='')
    cursor = cnx.cursor()

    book_info_cat = '(book_id, title, '                  # to be added
    post_fix = 'VALUES (%s, %s, '                        # to be added
    book_info = [book['ISBN'], book['title']]            # to be added

    # author
    HaveAuthor = False
    author_id_list = []
    try:
        author_list = re.split('[,|;*、，/]+', book['author'])
        for author in author_list:
            cursor.execute('SELECT author_id FROM author WHERE name = "{}"'.format(author))
            res = cursor.fetchone()
            if res is None:
                try:
                    author_info = book['author_intro']
                    cursor.execute(instructions['add_author_with_info'], (author, 0, author_info))
                    cnx.commit()
                except KeyError:
                    cursor.execute(instructions['add_author'], (author, 0))
                    cnx.commit()
                cursor.execute('SELECT author_id FROM author WHERE name = "{}"'.format(author))
                author_id_list.append(cursor.fetchone()[0])
            else:
                author_id_list.append(res[0])
        HaveAuthor = True
    except ValueError:
        pass


    # translator
    HaveTranslator = False
    translator_id_list = []
    try:
        translator_list = re.split('[,|;*、/，]+', book['translator'])
        for translator in translator_list:
            cursor.execute('SELECT author_id FROM author WHERE name = "{}"'.format(translator))
            res = cursor.fetchone()
            if res is None:
                cursor.execute(instructions['add_author'], (translator, 1))
                cnx.commit()
                cursor.execute('SELECT author_id FROM author WHERE name = "{}"'.format(translator))
                translator_id_list.append(cursor.fetchone()[0])
            else:
                translator_id_list.append(res[0])
        HaveTranslator = True


    except KeyError:
        pass

    # publisher
    try:
        publisher = book['publisher']
        cursor.execute('SELECT press_id FROM press WHERE name = "{}"'.format(publisher))
        res = cursor.fetchone()
        if res is None:
            cursor.execute(instructions['add_press'], (publisher,))
            cnx.commit()
            cursor.execute('SELECT press_id FROM press WHERE name = "{}"'.format(publisher))
            res = cursor.fetchone()
        res = res[0]
        book_info_cat = book_info_cat + 'press_id, '
        post_fix = post_fix + '%s, '
        book_info.append(res)
    except KeyError:
        pass

    # date
    try:
        date_list = book['time'].split('-')
        if len(date_list) == 2:
            publish_date = date(int(date_list[0]), int(date_list[1]), 1)
        elif len(date_list) == 3:
            publish_date = date(int(date_list[0]), int(date_list[1]), int(date_list[2]))
        else:
            raise Exception("Date error!")
        book_info_cat = book_info_cat + 'publish_date, '
        post_fix = post_fix + '%s, '
        book_info.append(publish_date)
    except KeyError:
        pass

    # price
    try:
        price = book['price']
        if price[-1] == '元':
            price = price[0:-1]
        book_info_cat = book_info_cat + 'price_standard, '
        post_fix = post_fix + '%s, '
        book_info.append(price)
    except KeyError:
        pass

    # score
    try:
        score = book['score']
        book_info_cat = book_info_cat + 'score, '
        post_fix = post_fix + '%s, '
        book_info.append(score)
    except KeyError:
        pass

    # intro
    try:
        intro = book['intro']
        book_info_cat = book_info_cat + 'introduction, '
        post_fix = post_fix + '%s, '
        book_info.append(intro)
    except KeyError:
        pass

    book_info_cat = book_info_cat[0:-2]+')'
    post_fix = post_fix[0:-2] + ')'
    book_info = tuple(book_info)
    try:
        cursor.execute(instructions['add_book_prefix'] + book_info_cat + post_fix, book_info)
        cnx.commit()

        if HaveAuthor:
            for author_id in author_id_list:
                cursor.execute(instructions['add_book_author'], (book['ISBN'], author_id))
                cnx.commit()
        if HaveTranslator:
            for translator_id in translator_id_list:
                cursor.execute(instructions['add_book_author'], (book['ISBN'], translator_id))
                cnx.commit()
    except Exception as e:
        print(e)
        pass
    cursor.close()
    cnx.close()
