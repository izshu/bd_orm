import json
import sqlalchemy as sq

from sqlalchemy.orm import sessionmaker
from models import Publisher, Book, Shop, Stock, Sale, create_tables

DSN = "postgresql://postgres:123@localhost:5432/net_db"
engine = sq.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine)

with open("C:\\Users\\III\\Desktop\\codes\\bd\\fixtures\\tests_data.json", "r") as fd:
    data = json.load(fd)


for record in data:
    model = {
        "publisher": Publisher,
        "shop": Shop,
        "book": Book,
        "stock": Stock,
        "sale": Sale,
    }[record.get("model")]
    session.add(model(id=record.get("pk"), **record.get("fields")))
session.commit()


def get_stores_by_publisher(publisher_name_or_id):
    if isinstance(publisher_name_or_id, str):
        publisher = session.query(Publisher).filter(Publisher.name == publisher_name_or_id).first()
    elif isinstance(publisher_name_or_id, int):
        publisher = session.query(Publisher).filter(Publisher.id == publisher_name_or_id).first()

    if publisher is None:
        print(f"Издатель с именем/ID '{publisher_name_or_id}' не найден.")
        return

    query = (
        session.query(
            Shop.name.label("shop_name"),
            Book.title.label("book_title"),
            Sale.count.label("sold_count"),
            Sale.price.label("sale_price"),
            Sale.date_sale.label("sale_date"),
        )
        .select_from(Book)
        .join(Stock, Stock.id_book == Book.id)
        .join(Sale, Sale.id_stock == Stock.id)
        .join(Shop, Shop.id == Stock.id_shop)
        .filter(Book.publisher == publisher)
    )
    results = query.all()

    if not results:
        print(f"Нет продаж книг издателя '{publisher.name}'.")
        return

    print(f"Книги издателя '{publisher.name}', проданные в магазинах:")
    for result in results:
        print(
            f"{result.book_title} | {result.shop_name} | {result.sale_price} | {result.sale_date.strftime('%d-%m-%Y')}"
        )


publisher_input = input("Введите имя или ID издателя: ")

if publisher_input.isdigit():
    publisher_input = int(publisher_input)


get_stores_by_publisher(publisher_input)

session.close()
