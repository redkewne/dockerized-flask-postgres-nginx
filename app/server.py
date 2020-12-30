from decimal import Decimal
from flask import Flask, render_template, request, redirect, url_for
from app.controller import Controller


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    products = Controller.retrieve_all_products()

    return render_template('index.html', PRODUCTS=products)


@app.route('/process_payment', methods=['POST'])
def process_payment():
    product_id = int(request.form['product_id'])
    payment_amount = Decimal(request.form['payment_amount'])

    res = Controller.check_if_purchase_valid(payment_amount, product_id)

    return redirect(url_for('result', message=res))


@app.route('/create_product', methods=['POST'])
def create_product():
    name = request.form['name']
    price = Decimal(request.form['price'])
    quantity = int(request.form['quantity'])

    res = Controller.create_product(name, price, quantity)

    return redirect(url_for('result', message=res))


@app.route('/result', methods=['GET'])
def result():
    return render_template('result.html', MESSAGE=request.args.get('message'))


if __name__ == '__main__':
    app.run()
