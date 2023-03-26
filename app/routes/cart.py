from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from ..models import db, Customer, CartProduct, Product, CustomerProduct
import os
import pandas as pd

cart_bp = Blueprint('cart_bp', __name__)

ALLOWED_EXTENSIONS = {'xlsx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_file(filepath):
    df = pd.read_excel(filepath, engine='openpyxl')
    data = df.to_dict(orient='records')
    for row in data:
        entry = Product(name=row['product_name'], price=row['price'], description=row['description'])
        current_app.db.session.add(entry)
    current_app.db.session.commit()

@cart_bp.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        customer_email = request.form['customer_email']
        customer_address = request.form['customer_address']
        customer_phone_number = request.form['customer_phone_number']
        customer_is_multi_location = request.form.get('customer_is_multi_location') == 'on'

        customer = Customer(name=customer_name, email=customer_email, address=customer_address, phone_number=customer_phone_number, is_clan=customer_is_multi_location)
        current_app.db.session.add(customer)
        current_app.db.session.commit()

        cart_products = CartProduct.query.all()

        for cart_product in cart_products:
            product = Product.query.get(cart_product.product_id)
            customer_product = CustomerProduct(customer_id=customer.id, product_id=product.id, quantity=cart_product.quantity)
            current_app.db.session.add(customer_product)
            current_app.db.session.delete(cart_product)
        current_app.db.session.commit()

        flash('Offer created for {}.'.format(customer_name))
        return redirect(url_for('index'))

    products = Product.query.all()

    cart_products = CartProduct.query.all()

    return render_template('cart.html', products=products, cart_products=cart_products)
