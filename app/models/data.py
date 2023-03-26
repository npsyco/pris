from . import db

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))

    def __repr__(self):
        return f"<Data {self.product_name}: {self.price}>"
