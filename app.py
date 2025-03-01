from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "your_secret_key_here".encode('utf-8')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):  # Changed class name to PascalCase
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)  # Unique constraint
    password = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(40), nullable=False, unique=True)  # Unique constraint

with app.app_context():
    db.create_all()


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("Username or Email already exists!", "danger")
            
            return redirect(url_for('register'))

        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful!", "success")
        return redirect(url_for('users'))  # Redirect to users page

    return render_template('register.html')

@app.route('/users')
def users():
    users = User.query.all()  # Updated model reference
    return render_template('users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
