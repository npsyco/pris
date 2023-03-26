from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .data import Data
from .customer import Customer
from .location import Location
from .customer_product import CustomerProduct
from .product import Product
