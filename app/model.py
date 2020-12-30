import os
from decimal import Decimal
from pony.orm import Database, Required, PrimaryKey, db_session, delete

db = Database()

class Product(db.Entity):
    product_id = PrimaryKey(int, auto=True)
    name = Required(str)
    price = Required(Decimal)
    quantity_available = Required(int)

    @staticmethod
    @db_session
    def retrieve_all():
        return Product.select()[:]

    @staticmethod
    @db_session
    def create(name, price, quantity):
        Product(name=name, price=price, quantity_available=quantity)
        return {'success': True, 'message': '{} {}(s) priced at {} created.'.format(quantity, name, price)}

    @staticmethod
    @db_session
    def in_stock(product_id):
        product = Product[product_id]
        return product.quantity_available > 0

    @staticmethod
    @db_session
    def delete_all():
        delete(p for p in Product)

    @staticmethod
    @db_session
    def reduce_product_quantity_by(amount, product_id):
        Product[product_id].quantity_available -= 1

user = os.environ['POSTGRES_USER']
pwd = os.environ['POSTGRES_PASSWORD']
db_name = os.environ['POSTGRES_DB']

db.bind(provider='postgres', host='db', user=user, password=pwd, database=db_name)
db.generate_mapping(create_tables=True)
