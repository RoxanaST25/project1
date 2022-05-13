from flask import render_template ,redirect, session, request
from flask_app import app
from flask_app.models.score import Score
from flask_app.models.user import User


@app.route('/paintings/new')
def nav_add_painting():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    x = User.get_user(data)
    return render_template('add_painting.html',user=x)

@app.route('/paintings')
def paintings():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    x = User.get_user(data)
    d = Painting.get_all()
    usrname = x.first_name + " " + x.last_name
    return render_template("paintings.html",user=x,painting=d, username=usrname )

@app.route('/show/<int:id>')
def show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    painting_data = {
        "id":id
    }
    data = {
        "id":session['user_id']
    }
    x = Painting.get_painting(painting_data)
    f = User.get_user(data)
    return render_template("show.html",painting=x ,user=f)

@app.route('/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Painting.delete(data)
    return redirect('/paintings')


@app.route('/create_painting',methods=['POST'])
def create_painting():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Painting.validate_painting(request.form):
        return redirect('/paintings/new')

    data ={
        'id': session['user_id']
    }
    x = User.get_user(data)
    paintedBy = x.first_name + " " + x.last_name
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "price": request.form["price"],
        "painted_by": paintedBy,
        "user_id": session["user_id"]
    }
    Painting.save(data)
    return redirect('/paintings')

@app.route('/paintings/<int:id>/edit')
def edit_painting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    painting_data = {
        "id":id
    }
    data = {
        "id":session['user_id']
    }
    g = Painting.get_painting(painting_data)
    h = User.get_user(data)
    return render_template("edit_painting.html",painting=g,user=h)

@app.route('/update/<int:id>',methods=['POST'])
def update(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Painting.validate_painting(request.form):
        return redirect('/paintings/' + str(id) + '/edit')
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "price": request.form["price"],
        "id": id
    }
    Painting.update(data)
    return redirect('/paintings')
