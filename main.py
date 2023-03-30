import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Book, Shop, Sale, Stock

DSN = 'postgresql://postgres:admin@localhost:5432/SQL_ORM'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

publisher1 = Publisher(name='Пушкин')
session.add(publisher1)
session.commit()

book1 = Book(title='Капитанская дочка', publishers=publisher1)
book2 = Book(title='Руслан и Людмила', publishers=publisher1)
book3 = Book(title='Евгений Онегин', publishers=publisher1)
session.add_all([book1, book2, book3])
session.commit()

shop1 = Shop(name='Буквоед')
shop2 = Shop(name='Лабиринт')
shop3 = Shop(name='Книжный дом')
session.add_all([shop1, shop2, shop3])
session.commit()

stock1 = Stock(books=book1, shops=shop1, count=5)
stock2 = Stock(books=book2, shops=shop1, count=7)
stock3 = Stock(books=book1, shops=shop2, count=8)
stock4 = Stock(books=book3, shops=shop3, count=10)
stock5 = Stock(books=book1, shops=shop1, count=11)
session.add_all([stock1, stock2, stock3, stock4])
session.commit()

sale1 = Sale(price=600, date_sale='09-11-2022', count=5, stocks_sale=stock1)
sale2 = Sale(price=500, date_sale='08-11-2022', count=7, stocks_sale=stock2)
sale3 = Sale(price=580, date_sale='05-11-2022', count=8, stocks_sale=stock3)
sale4 = Sale(price=490, date_sale='02-11-2022', count=10, stocks_sale=stock4)
sale5 = Sale(price=600, date_sale='26-10-2022', count=5, stocks_sale=stock5)
session.add_all([sale1, sale2, sale3, sale4, sale5])
session.commit()

publisher_name = input('Имя издателя: ')
for c in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Stock.shops).join(Stock.books).\
    join(Stock.sales).join(Book.publishers).filter(Publisher.name == publisher_name):
    print(f'{c[0]} | {c[1]} | {c[2]} | {c[3]}')

