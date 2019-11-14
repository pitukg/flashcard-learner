#class for representing a deck of flashcards
#           see the Leitner system (Wikipedia)
#   a list of Flashcard objects

import flashcard

class Deck:

    #constructor
    def __init__( self ):
        self.flashcards = []

    #inserts a FLashcard into the deck
    def push( self, _card ):
        self.flashcards.append(_card)

    #deletes a given Flashcard from the deck
    def remove( self, _card ):
        self.flashcards.remove(_card)

    def get_flashcards( self ):
        return self.flashcards


#constants
CURRENT = -1
RETIRED = -2


# deck current:
#   for the words least known - Tier 0
deckCurrent = Deck()
#deck retired:
#   for the mastered words - Tier 4
deckRetired = Deck()

# progress decks
# each deck has the 4 digit header as in the sessions list at the same index
progressDeck = []
#constructs the empty decks
for i in range(10):
    newDeck = Deck()
    progressDeck.append(newDeck)

#function to display the content of all progress decks
def print_deck_contents():
    for i in range(10):
        for card in progressDeck[i].get_flashcards():
            print(card.word + ' ' + card.translation)
        print('|')
