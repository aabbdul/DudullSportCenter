from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId


app = Flask(__name__)
app.secret_key = b'\xad\x07\x93Y+\xcc\x9aX\xcf\xf8?\xda\xf9^\xa4\xbd\n\x06\xbaE\x0bz\x84~'

# MongoDB configuration

client = MongoClient('mongodb://localhost:27017/')

db = client['user-management']
users_collection = db['users']
admins_collection = db['admin']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/registrasi')
def register():
    return render_template('registrasi-login/index.html')

@app.route('/auth', methods=['GET','POST'])
def auth():
    if 'register' in request.form:

        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        newUser = {
            'fullname':fullname,
            'phone':phone,
            'email': email, 
            'password': hashed_password
            }
        
        if users_collection.find_one({'email': email}):
            flash('User already exists', 'danger')
        else:
            users_collection.insert_one(newUser)
            flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('register'))
    
    elif 'login' in request.form:

        email = request.form['email']
        password = request.form['password']
        user = users_collection.find_one({'email': email})

        if 'email' in session:
            return redirect(url_for('home'))

        if user and check_password_hash(user['password'], password):
            session['email'] = email
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'danger')
    
    return redirect(url_for('register'))

@app.route('/bookingFutsal')
def bookFutsal():
    return render_template('booking/futsal.html')

@app.route('/bookingBadminton')
def bookBadminton():
    return render_template('booking/badminton.html')


@app.route('/logout')
def userLogout():
    session.pop('email', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/dashboardAdmin',methods=['GET', 'POST'])
def admin():
    admin = list(admins_collection.find({}))
    return render_template('admin/admin.html', admin=admin)

@app.route('/authAdmin', methods=['GET','POST'])
def authAdmin():
    if 'login' in request.form:

        username = request.form['username']
        password = request.form['password']
        user = admins_collection.find_one({'username': username})

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            flash("You're now admin", 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password', 'danger')
    
    return redirect(url_for('admin'))

@app.route('/tambahDataAdmin', methods=['GET', 'POST'])
def tambah_data_admin():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hash_password = generate_password_hash(password)

        doc = {
            'username': username,
            'password': hash_password
        }
        
        admins_collection.insert_one(doc)
        return redirect(url_for("admin"))
        
    return render_template('admin/tambahData.html')

@app.route('/hapusDataAdmin/<string:_id>', methods=["GET", "POST"])
def hapus_data_admin(_id):
    admins_collection.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('admin'))

@app.route('/dashboardUser',methods=['GET', 'POST'])
def users():
    user = list(users_collection.find({}))
    return render_template('admin/user.html', user=user)

@app.route('/hapusDataUser/<string:_id>', methods=["GET", "POST"])
def hapus_data_user(_id):
    users_collection.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('users'))

@app.route('/adminlogout')
def adminLogout():
    session.pop('username', None)
    flash("You're no longer admin.", 'success')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
