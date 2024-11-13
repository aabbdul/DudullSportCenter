from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = b'\xad\x07\x93Y+\xcc\x9aX\xcf\xf8?\xda\xf9^\xa4\xbd\n\x06\xbaE\x0bz\x84~'

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/user-management"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/registrasi')
def register():
    return render_template('registrasi-login/index.html')

@app.route('/auth', methods=['GET','POST'])
def auth():
    if 'register' in request.form:

        email = request.form['email']
        password = request.form['password']
        fullname = request.form['fullname']
        phone = request.form['phone']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        newUser = {
            'fullname':fullname,
            'phone':phone,
            'email': email, 
            'password': hashed_password
            }
        
        if mongo.db.users.find_one({'email': email}):
            flash('User already exists', 'danger')
        else:
            mongo.db.users.insert_one(newUser)
            flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('register'))
    
    elif 'login' in request.form:

        email = request.form['email']
        password = request.form['password']
        user = mongo.db.users.find_one({'email': email})

        if user and bcrypt.check_password_hash(user['password'], password):
            session['email'] = email
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')
    
    return redirect(url_for('register'))

@app.route('/logout')
def userLogout():
    session.pop('email', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
