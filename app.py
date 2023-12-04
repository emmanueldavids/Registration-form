from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    picture_filename = db.Column(db.String(120), nullable=False)


with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    fullname = request.form.get('fullname')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    dob_str = request.form.get('dob')


    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(filename)

    # Convert the string representation of the date to a datetime.date object
    dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

    # Save user details and picture filename to the database
    new_user = User(fullname=fullname, username=username, email=email, password=password, dob=dob, picture_filename=secure_filename(file.filename))
    db.session.add(new_user)
    db.session.commit()

    return render_template('success.html')
@app.route('/users')
def view_users():
    users = User.query.all()
    return render_template('view_users.html', users=users)


if __name__ == '__main__':
    app.run(debug=True)
