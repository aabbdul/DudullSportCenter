from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_pymongo import PyMongo
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = b'\xad\x07\x93Y+\xcc\x9aX\xcf\xf8?\xda\xf9^\xa4\xbd\n\x06\xbaE\x0bz\x84~'

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/user-management"
mongo = PyMongo(app)

@app.route('/')
def admin():
    return render_template('admin/admin.html')

@app.route('/authAdmin', methods=['GET','POST'])
def authAdmin():
    if 'login' in request.form:

        username = request.form['username']
        password = request.form['password']
        user = mongo.db.admin.find_one({'username': username})

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            flash("You're now admin", 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password', 'danger')
    
    return redirect(url_for('admin'))

@app.route('/adminlogout')
def adminLogout():
    session.pop('username', None)
    flash("You're no longer admin.", 'success')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
