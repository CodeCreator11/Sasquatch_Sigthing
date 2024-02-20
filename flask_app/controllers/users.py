from flask_app import app, bcrypt
from flask import render_template, redirect, request, session
from flask_app.models import user  

@app.route('/')
def home():
    return render_template('login_registration.html')

@app.route('/users/registration', methods=['POST'])
def register():
    if not user.User.validate_registration(request.form):
        return redirect('/')
    hashed_pw = bcrypt.generate_password_hash(request.form['password'])

    data={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": hashed_pw
    }
    one_user_id =user.User.create_user(data)
    session['logged_in_id'] = one_user_id
    return redirect('/sasquatch/dashboard')

@app.route('/users/login', methods=['POST'])
def login():
    one_user=user.User.validate_login(request.form)

    if not one_user:
        return redirect('/')
    session['logged_in_id'] = one_user.id
    return redirect('/sasquatch/dashboard')

@app.route('/users/logout')
def logout():
    session.clear()
    return redirect('/')