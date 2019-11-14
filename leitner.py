import flashcard
import deck
from deck import deckCurrent, deckRetired, progressDeck
import database_manip as db

#list to store progress deck headers
sessions = [(0, 2, 5, 9),
            (1, 3, 6, 0),
            (2, 4, 7, 1),
            (3, 5, 8, 2),
            (4, 6, 9, 3),
            (5, 7, 0, 4),
            (6, 8, 1, 5),
            (7, 9, 2, 6),
            (8, 0, 3, 7),
            (9, 1, 4, 8)]

def initialize():
    db.load_database()


def commit_card_update(card):
    db.update_card(card)

#function for getting the progress decks to review that has Tier 1-2 cards
def get_session_deck_indices( sessionIndex ):

    indexList = []

    for sessionTuple in sessions:
        if (sessionTuple[0] == sessionIndex or
            sessionTuple[1] == sessionIndex or
            sessionTuple[2] == sessionIndex or
            sessionTuple[3] == sessionIndex):
                indexList.append(sessions.index(sessionTuple))

    return indexList

#function for getting the progress decks to review that has Tier 3 cards
def get_last_deck_index( sessionIndex ):

    for sessionTuple in sessions:
        if sessionTuple[3] == sessionIndex:
            return sessions.index(sessionTuple)



#does the review process for cards in deck current
#for testing without the UI only!
def NOT_review_deck_current( sessionIndex, app ):

    for card in deckCurrent.get_flashcards():

        if card.review_was_successful(app):

            #in case of success the card gets transferred to the progress deck
            # whose header starts with the session index
            progressDeck[ sessionIndex ].push(card)
            deckCurrent.remove(card)
            db.update_deck_number(card, sessionIndex)

            #otherwise it stays in deck current



#does the review process for progress decks at given session index
#for testing without the UI only!
def NOT_review_progress_decks( sessionIndex, app ):

    #first do all Tier 1-2 cards

    deckIndices = get_deck_indices_but_last(sessionIndex)

    for deckIndex in deckIndices:
        deckToReview = progressDeck[ deckIndex ]

        for card in deckToReview.get_flashcards():

            #in case of fail the card gets transferred to deck current
            if not card.review_was_successful(app):
                deckCurrent.push(card)
                deckToReview.remove(card)
                db.update_deck_number(card, deck.CURRENT)

            #otherwise it stays in that progress deck (getting its Tier increased at the next review)


    #tier 3 cards

    deckWithLastNumberMatch = progressDeck[ get_last_deck_index(sessionIndex) ]

    for card in deckWithLastNumberMatch.get_flashcards():

        #in case of success gets transferred to deck retired
        if card.review_was_successful(app):
            print('You have mastered this word: ' + card.word)
            deckRetired.push(card)
            deckWithLastNumberMatch.remove(card)
            db.update_deck_number(card, deck.RETIRED)
        #otherwise move to deck current
        else:
            deckCurrent.push(card)
            deckWithLastNumberMatch.remove(card)
            db.update_deck_number(card, deck.CURRENT)


#tester funciton
def tester_function(app):
    f1 = flashcard.Flashcard(1, 'watch', 'ora')
    f2 = flashcard.Flashcard(2, 'bread', 'kenyer')
    f3 = flashcard.Flashcard(3, 'skull', 'koponya')
    f4 = flashcard.Flashcard(4, 'curse', 'atok')
    db.insert_new_card(f1)
    db.insert_new_card(f2)
    db.insert_new_card(f3)
    db.insert_new_card(f4)
#    deckCurrent.push(f1)
#    deckCurrent.push(f4)
#    deckCurrent.push(f2)
#    deckCurrent.push(f3)
#    deck.print_deck_contents()
#    review_progress_decks(3)
#    deck.print_deck_contents()
    for card in deckCurrent.get_flashcards():
        print(card.word + " " + card.translation)

#tester_function()

