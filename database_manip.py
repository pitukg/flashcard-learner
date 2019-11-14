#file containing the functions that manipulate the database where the decks are saved
#using the sqlite3 library for interpreting SQL commands
import sqlite3

import deck
from deck import deckCurrent, deckRetired, progressDeck
import flashcard

#open the database file
database = sqlite3.connect('flashcards.db')
cursor = database.cursor()


#function for loading the data from the database to the decks
def load_database():

    #create empty table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cards
            (ID INTEGER PRIMARY KEY, word TEXT UNIQUE, translation TEXT UNIQUE, deck INTEGER, tier INTEGER)
        ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS session (next INTEGER)''')

    cursor.execute('''
        SELECT ID, word, translation, deck, tier FROM cards
        ''')

    entries = cursor.fetchall()

    for entry in entries:

        _ID = entry[0]
        _word = entry[1]
        _translation = entry[2]
        _deck = entry[3]
        _tier = entry[4]

        print(_word, _tier)

        card = flashcard.Flashcard(_ID, _word, _translation, _deck, _tier)

        if _deck == deck.CURRENT:
            deckCurrent.push(card)
        elif _deck == deck.RETIRED:
            deckRetired.push(card)
        else:
            progressDeck[ _deck ].push(card)


def get_nextSession():
    cursor.execute('''
        SELECT next FROM session''')
    sess = cursor.fetchall()
    if len(sess) == 0:
        cursor.execute('''
            INSERT INTO session VALUES (1)''')
        database.commit()
        return 0
    else:
        nextSess = (sess[0][0]+1) % 10
        cursor.execute('''
            UPDATE session SET next = ? WHERE next = ?''', (nextSess, sess[0][0]))
        database.commit()
        return sess[0][0]

#insert a new flashcard object to the database
def insert_new_card( _card ):

    cursor.execute('''
        INSERT INTO cards (word, translation, deck, tier) VALUES (?, ?, ?, ?)
        ''', (_card.word, _card.translation, deck.CURRENT, _card.tier))

    database.commit()
    print('quit and restart')


#updates the deck value of a given card object in the database
def update_card( _card ):

    cursor.execute('''
        UPDATE cards SET deck = ?, tier = ? WHERE ID = ?
        ''', (_card.deckNo, _card.tier, _card.ID))

    database.commit()



