import telebot
from Name3songs import config
import os
import time
import random
from Name3songs import utils
from Name3songs.SQLighter import SQLighter
from telebot import types

bot = telebot.TeleBot(config.token)
points = 0

@bot.message_handler(commands=['start'])
def welcome(message):
	bot.send_message(message.chat.id, 'Welcome to "<b>{1.first_name}</b>"!\n\n'
                                      'To read the rules, enter /rules'.format(message.from_user, bot.get_me()),
                     parse_mode='html')

@bot.message_handler(commands=['rules'])
def rules(message):
    bot.send_message(message.chat.id, 'When the game starts, I will send you an audio file. '
                                      'Your task is to choose the correct name of the song from '
                                      'the proposed options.\n'
                                      'If you answer correctly 3 times, you will win.\n'
                                      'If you answer incorrectly at least 1 time, you will lose.\n'
                                      'Good Luck!\n\n'
                                      'To start the game, enter /game')

@bot.message_handler(commands=['test'])
def find_file_ids(message):
    for file in os.listdir('music/'):
        if file.split('.')[-1] == 'mp3':
            f = open('music/'+file, 'rb')
            msg = bot.send_voice(message.chat.id, f, None)
            # Send after the file its file_id
            bot.send_message(message.chat.id, msg.voice.file_id, reply_to_message_id=msg.message_id)
        time.sleep(3)


@bot.message_handler(commands=['game'])
def game(message):
    # Connecting to the database
    db_worker = SQLighter(config.database_name)
    # Get random row from database
    row = db_worker.select_single(random.randint(1, utils.get_rows_count()))
    # Forming the Markup
    markup = utils.generate_markup(row[2], row[3])
    # Send an audio file with response options
    bot.send_voice(message.chat.id, row[1], reply_markup=markup, duration=20)
    # Turn on "Game Mode"
    utils.set_user_game(message.chat.id, row[2])
    # Disconnecting from the database
    db_worker.close()


@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
	# If the function returns None -> The person is not in the game
    answer = utils.get_answer_for_user(message.chat.id)
	# answer can be either text or None
	# if None:
    if not answer:
	   	bot.send_message(message.chat.id, 'To read the rules, enter /rules\n'
                                          'To start the game, enter /game')
    else:
        # Remove the keyboard with answer options
        keyboard_hider = types.ReplyKeyboardRemove()
	    # If the answer is correct/incorrect
        if message.text == answer:
            global points
            points += 1
            if points < 3:
                bot.send_message(message.chat.id, f'Right!\nPoints scored: {points}\nTo continue, enter /game', reply_markup=keyboard_hider)
            else:
                bot.send_message(message.chat.id, f'Congratulations!\nYou have completed the game!\nPoints scored: {points}', reply_markup=keyboard_hider)
                points = 0
        else:
            bot.send_message(message.chat.id, 'Unfortunately the answer is wrong.\nTo start over, enter /game', reply_markup=keyboard_hider)
            points = 0
	   	# Delete user from storage (game over)
        utils.finish_user_game(message.chat.id)

if __name__ == '__main__':
    utils.count_rows()
    random.seed()
    bot.polling()