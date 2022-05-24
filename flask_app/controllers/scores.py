from flask import render_template ,redirect, session, request
from flask_app import app
from flask_app.models.score import Score
from flask_app.models.user import User
from flask_app.models.score import QuestionList


@app.route('/scores')
def scores():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    d = Score.get_all()
    # usrname = x.first_name
    print("Session UserID: ", session['user_id'])
    for x in d:
        print("user ", x.user_id)
    return render_template("scores.html",user=session['user_id'],scores=d)

@app.route('/questions/<int:index>')
def questions(index):
    if 'user_id' not in session:
        return redirect('/logout')

    question = QuestionList().questions[index]
    return render_template('questions.html', index = index, question=question)

@app.route('/selected/<int:index>/<int:answer>',methods=['POST'])
def selected(index,answer):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Score.validate_option(request.form):
        return redirect('/questions/' + str(index))
    print(request.form)

    correct = False

    if answer == 0:
        #check for option0
        if "option0" in request.form.keys():
            correct = True
    elif answer == 1:
        #option1
        if "option1" in request.form.keys():
            correct = True
    else:
        #option2
        if "option2" in request.form.keys():
            correct = True

    if correct == True:
        if "score" in session.keys():
            session["score"] = session["score"]+1
        else:
            session["score"] = 1

    print(session)

    if index == 4:
        # exit
        if "score" in session.keys():
            result = session["score"]
            #save score
            data = {
                "score": result,
                "users_id" : session["user_id"]
            }
            Score.save(data)
        else:
            #score is 0
            data = {
                "score": 0,
                "users_id" : session["user_id"]
            }
            Score.save(data)
        print("Session Before: ", session)
        session.pop('score', None)
        print("Session After: ", session)
        return redirect('/scores')
    
    index = index+1
    redirection = '/questions/' + str(index)

    return redirect(redirection)

@app.route('/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Score.delete(data)
    return redirect('/scores')