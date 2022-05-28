# Creator LE
# Time 2022/3/26 21:13
# coding=UTF-8

instructions = {}

instructions['add_author'] = ("INSERT INTO author "
                              "(name, is_translator) "
                              "VALUES (%s, %s)")

instructions['add_author_with_info'] = ("INSERT INTO author "
                                        "(name, is_translator,intro) "
                                        "VALUES (%s, %s,%s)")

instructions['add_book_class'] = ("INSERT INTO book_class "
                                           "(name) "
                                           "VALUES (%s)")

instructions['add_press'] = ("INSERT INTO press "
                             "(name) "
                             "VALUES (%s)")

'''
Using add_book should be like this:

add_book = instructions['add_book_prefix'] + ''(book_id, title, ...)' + 'VALUES (%s, %s, ... )'

'''
instructions['add_book_prefix'] = ("INSERT INTO book ")

instructions['add_book_author'] = ("INSERT INTO book_author "
                                   "(book_id, author_id) "
                                   "VALUES (%s, %s)")
