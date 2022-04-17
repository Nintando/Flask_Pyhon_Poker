from flask import Flask, render_template, url_for, request, session, redirect
from label import str_TOO_YOUNGER, str_TOO_HIGH
from module_tirage import premier_tirage, deuxieme_tirage
from module_gain import gain

app = Flask(__name__)
app.secret_key = "super_secret_key"

@app.route('/')
def homepage():
    return render_template('start.html')

@app.route('/', methods=['POST'])
def check_age():
    user_age = int(request.form['age'])
    session['error-form'] = False
    if user_age < 18:
        session['error-form']= str_TOO_YOUNGER
        return render_template('start.html')
    else:
        session['wallet'] = int(request.form['wallet'])
        return redirect(url_for('board'))


@app.route('/board')
def board():
    return render_template('board.html')

@app.route('/board', methods=['POST'])
def tirage():

    deck = ['2-h','3-h','4-h','5-h','6-h','7-h','8-h','9-h',
    '10-h','J-h','Q-h','K-h','A-h','2-d','3-d','4-d','5-d',
    '6-d','7-d','8-d','9-d','10-d','J-d','Q-d','K-d','A-d',
    '2-c','3-c','4-c','5-c','6-c','7-c','8-c','9-c','10-c',
    'J-c','Q-c','K-c','A-c','2-s','3-s','4-s','5-s','6-s',
    '7-s','8-s','9-s','10-s','J-s','Q-s','K-s','A-s']

    session['bet'] = int(request.form['bet'])
    session['error-bet'] = False
    if session['bet'] > session['wallet']:
        session['error-bet'] = str_TOO_HIGH
        return render_template('board.html')
    else:
        tirage_1, deck_1 = premier_tirage(deck)
        session['tirage_1'] = tirage_1
        session['deck_1'] = deck_1
        session['wallet'] = session['wallet'] - session['bet']
        return redirect(url_for('round'))

@app.route('/board/round')
def round():
    return render_template('tirage_1.html')

@app.route('/board/round', methods=['POST'])
def check_card():
    if request.method == 'POST':
        session['tet'] = request.form.getlist('i')
        tirage_final = deuxieme_tirage(session['tet'],session['deck_1'])
        session['gain'], res = gain(tirage_final, int(session['bet']))
        session['wallet'] = session['wallet'] + int(session['gain'])
        session['message'] = res
    
        if int(session['wallet']) == 0:
            session['message'] = "You lost !"
            return redirect(url_for('end'))
    return render_template('tirage_2.html')

@app.route('/board/round', methods=['POST','GET'])
def round_2():
    return render_template('tirage_2.html')

@app.route('/end', methods=['POST', 'GET'])
def end():
    return render_template('end.html')

if __name__ == '__main__':
    app.run(debug=True)