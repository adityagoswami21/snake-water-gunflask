from flask import Flask, render_template, request
from random import choice
from replit import db

app = Flask(__name__)

if 'game_start' not in db:
  db['game_start'] = False

if 'player_score' not in db:
    db['player_score'] = 0

if 'choices' not in db:
    db['choices'] = ''

if 'result' not in db:
    db['result'] = ''

@app.route('/')
def index():
    return render_template('index.html', 
                           game_start=db['game_start'],
                           player_score=db['player_score'],
                           choices=db['choices'],
                           result=db['result'])

@app.route('/play', methods=['POST'])
def play():
    db['game_start'] = True
    player_choice=request.args['choice']
    computer_choice= get_computer_choice()
    score= calculate_result(player_choice, computer_choice)
    db['result']=get_result(score)
    db['choices']=f'👨 {player_choice} 🤖 {computer_choice}'
    db['player_score'] += score
    return render_template('index.html',
                           game_start=db['game_start'],
                           player_score=db['player_score'],
                           choices=db['choices'],
                           result=db['result'])


def get_computer_choice():
    return choice(['Snake','Water','Gun']) 


def calculate_result(player_choice, computer_choice):
    score=None
    if player_choice==computer_choice:
      score=0
    elif player_choice=='Snake' and computer_choice=='Water':
      score=1
    elif player_choice=='Water' and computer_choice=='Gun':
      score=1
    elif player_choice=='Gun' and computer_choice=='Snake':
      score=1

    else:
      score=-1

    return score


def get_result(score):
    
    if score==0:
      return "It's a Draw!"
    elif score==1:
      return "You Win!"
    else:
      return "You Lose!"
    
@app.route('/end')
def end_game():
    db['game_start'] = False
    db['player_score'] = 0
    db['choices'] = ''
    db['result'] = ''    
    return render_template('index.html', 
                           game_start=db['game_start'],
                           player_score=db['player_score'],
                           choices=db['choices'],
                           result=db['result'])


app.run(host='0.0.0.0', port=81)
