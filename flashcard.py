#class for representing a flashcard:
#                       a word with its translation
class Flashcard:

    #constructor
    def __init__( self, _ID = 0, _word = "no_word_error", _translation = "no_translation_error",
             _deckNo = -2, _tier = 0):
        self.ID = _ID
        self.word = _word
        self.translation = _translation
        self.deckNo = _deckNo
        self.tier = _tier

    #getters
    def get_ID( self ):
        return self.ID

    def get_word( self ):
        return self.word

    def get_translation( self ):
        return self.translation
