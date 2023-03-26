from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from . import bp
from ..models import Data
from .. import app
from .. import db
import os
import pandas as pd

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx'}

bp.config = {
    "UPLOAD_FOLDER": UPLOAD_FOLDER,
    "ALLOWED_EXTENSIONS": ALLOWED_EXTENSIONS,
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_file(filepath):
    df = pd.read_excel(filepath, engine='openpyxl')
    data = df.to_dict(orient='records')
    for row in data:
        entry = Data(data=str(row))
        db.session.add(entry)
    db.session.commit()

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(bp.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            process_file(filepath)
            flash('Data successfully extracted and saved.')
        return redirect(url_for('routes.index'))
    return render_template('index.html')
