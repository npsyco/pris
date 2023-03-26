from flask import Blueprint, request, redirect, url_for, render_template
from ..models import Product

product_selection_bp = Blueprint('product_selection', __name__)

@product_selection_bp.route('/product_selection', methods=['GET', 'POST'])
def product_selection():
    if request.method == 'POST':
        # Get the selected products from the form
        selected_products = request.form.getlist('product')
        # Process selected_products and add them to the cart
        # ...

        # Redirect to the cart route
        return redirect(url_for('cart'))

    # Load product data from the database
    products = Product.query.all()

    # Render the select_products template with the product data
    return render_template('select_products.html', products=products)
