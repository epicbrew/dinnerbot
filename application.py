import logging
from random import shuffle
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

app = Flask(__name__)
ask = Ask(app, '/dinnerbot')

test_data = [
  'spaghetti and meatballs',
  'fried rice',
  'that sausage and tortellini thing',
  'hamburgers',
  'ham steaks',
  'tacos',
  'pot roast',
  'fried catfish',
  'steak',
]

@app.route('/')
def index():
    return "dinnerbot"

@ask.launch
def dinnerbot_launch():
    welcome_msg = render_template('welcome')
    dinner_list = test_data[:]
    shuffle(dinner_list)
    session.attributes['dinners'] = dinner_list
    return question(welcome_msg)

@ask.intent("SuggestionsIntent")
def start_suggesting():
    try:
        dinners = session.attributes['dinners']
    except KeyError:
        dinner_list = test_data[:]
        shuffle(dinner_list)
        session.attributes['dinners'] = dinner_list
        dinners = session.attributes['dinners']

    try:
        dinner = session.attributes['dinners'].pop()
    except IndexError:
        return statement("I'm out of ideas.")

    session.attributes['last'] = dinner
    suggestion_msg = render_template('suggestion', dinner=dinner)

    return question(suggestion_msg)

@ask.intent("NoIntent")
def next_suggestion():
    try:
        dinner = session.attributes['dinners'].pop()
    except IndexError:
        return statement("I'm out of ideas.")

    session.attributes['last'] = dinner
    suggestion_msg = render_template('suggestion', dinner=dinner)

    return question(suggestion_msg)

@ask.intent("YesIntent")
def finish():
    if 'last' in session.attributes:
        dinner = session.attributes['last']
    else:
        dinner = 'whatever you are having'

    enjoy_msg = render_template('enjoy', dinner=dinner)
    return statement(enjoy_msg)

if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0')
    app.run(debug=True)
