import logging
from random import randint
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

app = Flask(__name__)
ask = Ask(app, '/')

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

@ask.launch
def dinnerbot_launch():
    welcome_msg = render_template('welcome')
    dinner_list = test_data[:]
    dinner_list.shuffle()
    session.attributes['dinners'] = dinner_list
    return question(welcome_msg)

@ask.intent("StartIntent")
def next_round():
    try:
        dinner = session.attributes['dinners'].pop()
    except IndexError:
        return statement("I'm out of ideas.")

    suggestion_msg = render_template('suggestion', dinner=dinner)

    return question(suggestion_msg)


if __name__ == '__main__':
    app.run(debug=True)
