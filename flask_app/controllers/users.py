from flask import render_template,redirect,session,request, flash
from flask_app import app

from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.score import Score

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['POST'])
def register():

    if not User.validate(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data) 
    session['user_id'] = id

    return redirect('/scores')

@app.route('/login',methods=['POST'])
def login():
    user = User.get_user_with_email(request.form)

    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/scores')

@app.route('/logout')
def logout():
    print('Logging Out')
    session.clear()
    return redirect('/')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/logout')
    x = User.get_user({"id": session["user_id"]})
    return render_template('profile.html', user = x)

@app.route('/profile_save',methods=['POST'])
def profile_save():
    if 'user_id' not in session:
        return redirect('/logout')

    if not User.edit_validate(request.form):
        return redirect('/profile')
    data ={ 
        "first_name": request.form['first_name'],
        "email": request.form['email'],
        "id": session["user_id"]
    }
    User.update(data)

    return redirect('/scores')