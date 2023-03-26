import os
from flask import Blueprint, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
import pandas as pd
from ..models import db
from ..models.data import Data
from ..models.cart_product import CartProduct
from ..models.product import Product
from ..models.customer_product import CustomerProduct
from ..models.customer import Customer
from app import app


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx'}
upload_bp = Blueprint('upload', __name__)

# Helper function to check for allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to process the uploaded XLSX file and store data in the SQLite database
def process_file(filepath):
    with app.app_context():
        df = pd.read_excel(filepath, engine='openpyxl')
        data = df.to_dict(orient='records')
        for row in data:
            entry = Data(data=str(row))
            db.session.add(entry)
        db.session.commit()

@upload_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            process_file(filepath)
            flash('Data successfully extracted and saved.')
            return redirect(url_for('index'))
    return render_template('upload.html')
