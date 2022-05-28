# Crawler_for_Database
A crawler tool for a databse course.

Note that this tool is customized for my own database and specific website (douban). It cannot be directly used for other purpose.

The reason I put it here is to save it for unexpected needs. Maybe when I have to crawl another website, I'll come back to check the codes.

## Code Structure

book_insert.py handles only operations with Mysql database.

instructions.py contains only a dictionary with instructions that book_insert.py may use.

crawl_lib.py handles only operations with web crawling. The target is [do](https://book.douban.com/).

main.py is the only one needs to run.
