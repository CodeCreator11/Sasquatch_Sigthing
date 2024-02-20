from flask_app import app, bcrypt
from flask import render_template, redirect, session, request
from flask_app.models import sasquatch,user

@app.route('/sasquatch/dashboard')
def dashboard():
    if 'logged_in_id' not in session:
        return redirect('/')
    data={
        'id': session['logged_in_id']
    }
    return render_template('dashboard.html', all_sasquatches=sasquatch.Sasquatch.get_all_sasquatches(), one_user=user.User.get_user_by_id(data))

@app.route('/sasquatch/new')
def new_sasquacth():
    if 'logged_in_id' not in session:
        return redirect('/')
    return render_template('new_sighting.html')

@app.route('/sasquatch/create', methods=['POST'])
def create_sasquatch():
    if not sasquatch.Sasquatch.validate_sasquatch(request.form):
        return redirect('/sasquatch/new')
    sasquatch.Sasquatch.create_sasquatch(request.form)
    return redirect('/sasquatch/dashboard')

@app.route('/sasquatch/edit/<int:id>')
def edit_sasquatch(id):
    if 'logged_in_id' not in session:
        return redirect('/')
    data={
        'id':id
    }
    return render_template('edit_sighting.html', one_sasquatch=sasquatch.Sasquatch.get_one_sasquatch(data))

@app.route('/sasquatch/update', methods=['POST'])
def update_sasquatch():
    if not sasquatch.Sasquatch.validate_sasquatch(request.form):
        return redirect(f'/sasquatch/edit/{request.form["id"]}')
    sasquatch.Sasquatch.update_sasquatch(request.form)
    return redirect(f'/sasquatch/dashboard')


@app.route('/sasquatch/show/<int:id>')
def show_sasquatch(id):
    if 'logged_in_id' not in session:
        return redirect('/')
    data = {
        'id': id
    }
    return render_template('view_sighting.html', one_sasquatch=sasquatch.Sasquatch.get_one_sasquatch(data))


@app.route('/sasquatch/delete', methods=['POST'])
def delete_sasquatch():
    sasquatch.Sasquatch.delete_sasquatch(request.form)
    return redirect('/sasquatch/dashboard')
