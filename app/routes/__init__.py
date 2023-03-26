from flask import Blueprint

bp = Blueprint('routes', __name__)

from .index import *
from .product_selection import *
from .cart import *
from .upload import *
from .cart_product import CartProduct

__all__ = ['db', 'Customer', 'Product', 'CartProduct', 'CustomerProduct']
