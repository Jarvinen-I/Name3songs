import shelve
from telebot import types
from random import shuffle
from TelegramBot.SQLighter import SQLighter
from TelegramBot.config import database_name, shelve_name

def count_rows():
    """
    This method counts the total number of rows in the database and stores it in storage.
    """
    db = SQLighter(database_name)
    rowsnum = db.count_rows()
    with shelve.open(shelve_name) as storage:
        storage['rows_count'] = rowsnum


def get_rows_count():
    """
    Get the number of rows in the database from the storage
    :return: (int) Number of rows
    """
    with shelve.open(shelve_name) as storage:
        rowsnum = storage['rows_count']
    return rowsnum


def set_user_game(chat_id, estimated_answer):
    """
    Write the user to the players and remember what he must answer.
    :param chat_id: user id
    :param estimated_answer: correct answer (from database)
    """
    with shelve.open(shelve_name) as storage:
        storage[str(chat_id)] = estimated_answer


def finish_user_game(chat_id):
    """
    End the current user's game and remove the correct answer from storage
    :param chat_id: user id
    """
    with shelve.open(shelve_name) as storage:
        del storage[str(chat_id)]


def get_answer_for_user(chat_id):
    """
    Get the correct answer for the current user.
    If the person entered some characters without starting the game, return None
    :param chat_id: user id
    :return: (str) Correct answer / None
    """
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer
        # Если человек не играет, ничего не возвращаем
        except KeyError:
            return None

def generate_markup(right_answer, wrong_answer):
    """
    Create a keyboard to select an answer
    :param right_answer: Correct answer
    :param wrong_answer: Set of wrong answers
    :return: Keyboard object
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    # Merge correct answer with incorrect
    all_answers = '{},{}'.format(right_answer, wrong_answer)
    # Create a list and write all elements into it
    list_items = []
    for item in all_answers.split(','):
        list_items.append(item)
    # Shuffle all elements
    shuffle(list_items)
    # Fill Markups with shuffled elements
    for item in list_items:
        markup.add(item)
    return markup