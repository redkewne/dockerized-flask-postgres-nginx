from app.model import Product, db_session


class Controller:


    @staticmethod
    def retrieve_all_products():
        return Product.retrieve_all()

    @staticmethod
    def check_if_purchase_valid(payment_amount, product_id):
        valid_funds = Controller.payment_is_sufficient(payment_amount, product_id)
        valid_quantity = Controller.product_in_stock(product_id)

        if valid_quantity:
            if valid_funds['success']:
                Product.reduce_product_quantity_by(1, product_id)

            return valid_funds['message']

        return 'Sorry, product is out of stock.'

    @staticmethod
    def product_in_stock(product_id):
        return Product.in_stock(product_id)

    @staticmethod
    @db_session
    def payment_is_sufficient(payment_amount, product_id):

        product = Product[product_id]
        if product.price > payment_amount:
            return {'success': False,
                    'message': '{} costs {} but client provided {},'
                               ' please request the correct amount.'.format(product.name.capitalize(), product.price, payment_amount)}

        return {'success': True, 'message': '{} order processed successfully.'.format(product.name.capitalize())}

    @staticmethod
    def create_product(name, price, quantity):
        result = Product.create(name, price, quantity)
        return result['message']
