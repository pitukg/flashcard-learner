#!/usr/bin/python
from tkinter import *
import tkinter as tk
import leitner
import flashcard
import database_manip as db


class Application(tk.Frame):

    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.window_setup()
        print('App started.')
        self.create_widgets()
        leitner.initialize()
        print('Database loaded.')
#        leitner.tester_function(self)
        self.mainloop()

    def window_setup(self):
        w = 600
        h = 400
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.place(relx = 0.5, rely = 0.5)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.pack(fill = BOTH, expand = 1)

    def create_widgets(self):
        quitButton = tk.Button(self, text = 'Close')
#        quitButton.pack()
        quitButton.bind('<ButtonRelease-1>', self.quit)
        quitButton.bind('<KeyRelease-Return>', self.quit)
        quitButton.place(relx=0.5, rely=0.75, anchor=CENTER)

        startSessionButton = tk.Button(self, text = 'New session')
        startSessionButton.bind('<ButtonRelease-1>', self.start_a_session)
        startSessionButton.bind('<KeyRelease-Return>', self.start_a_session)
        startSessionButton.place(relx = 0.5, rely = 0.25, anchor = CENTER)

        insertButton = tk.Button(self, text = 'Insert new word')
        insertButton.bind('<ButtonRelease-1>', self.create_insertion_popup)
        insertButton.bind('<KeyRelease-Return>', self.create_insertion_popup)
        insertButton.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        print('Widgets created.')

        

    def quit(self, event):
        print('Quitting...')
        self.master.destroy()

    #start a session
    def start_a_session(self, event):#event

        self.currentSession = leitner.db.get_nextSession()
        print('Session started (number',self.currentSession,').')

        #gather cards

        self.cardsForQuery = []
        for card in leitner.deckCurrent.get_flashcards():
            self.cardsForQuery.append(card)

        #needs editing
        for deckIndex in leitner.get_session_deck_indices(self.currentSession):
            deck = leitner.progressDeck[ deckIndex ]

            for card in deck.get_flashcards():
                self.cardsForQuery.append(card)
        
        self.queryPopup = tk.Toplevel(self, width = 300, height = 200, takefocus = True)

        self.labelWidget = tk.Label(self.queryPopup)
        self.entryWidget = tk.Entry(self.queryPopup)

        closeButton = tk.Button(self.queryPopup, text = 'Check')
        closeButton.bind('<ButtonRelease-1>', self.submit_guess)
        closeButton.bind('<KeyRelease-Return>', self.submit_guess)
        closeButton.place(relx = 0.5, rely = 1, y = -10, anchor = S)

        self.display_next_query()




    def display_next_query(self):

        if len(self.cardsForQuery) == 0:
            #increment nextSession (also in file)
            self.quit_session(None)
        else:

            self.currentCard = self.cardsForQuery.pop()

            self.labelWidget.destroy()
            self.labelWidget = tk.Label(self.queryPopup, text = 'Type in the translation:\n'
                + self.currentCard.word)
            self.labelWidget.place(width = 275, height = 50, relx = 0.5, rely = 0, y = 10, anchor = N)
            
            self.entryWidget.destroy()
            self.entryWidget = tk.Entry(self.queryPopup)
            self.entryWidget.place(width = 250, height = 25, relx = 0.5, y = 70, anchor = N)
            self.entryWidget.bind('<KeyRelease-Return>', self.submit_guess)
            self.entryWidget.focus()

    #check for correctness
    #move on to next query
    def submit_guess(self, event):
        submittedGuess = self.entryWidget.get()
        correct = (submittedGuess == self.currentCard.translation)

        if correct:
            if self.currentCard.deckNo == -1:#current
                leitner.deckCurrent.remove(self.currentCard)
                self.currentCard.tier += 1
                self.currentCard.deckNo = self.currentSession
                leitner.progressDeck[self.currentSession].push(self.currentCard)
                leitner.commit_card_update(self.currentCard)
                self.create_feedback_popup('Correct!')


            elif self.currentCard.tier == 3:#mastered
                leitner.progressDeck[self.currentCard.deckNo].remove(self.currentCard)
                self.currentCard.tier += 1
                self.currentCard.deckNo = -2 #retired
                leitner.deckRetired.push(self.currentCard)
                leitner.commit_card_update(self.currentCard)
                self.create_feedback_popup('Correct!\nYou have mastered this word:' + self.currentCard.word)

            else:
                leitner.progressDeck[self.currentCard.deckNo].remove(self.currentCard)
                self.currentCard.tier += 1
                leitner.progressDeck[self.currentCard.deckNo].push(self.currentCard)
                leitner.commit_card_update(self.currentCard)
                self.create_feedback_popup('Correct!')


        else:
            if self.currentCard.deckNo >= 0:
                leitner.progressDeck[ self.currentCard.deckNo ].remove(self.currentCard)
                self.currentCard.tier = 0
                self.currentCard.deck = -2#current
                leitner.deckCurrent.push(self.currentCard)
                leitner.commit_card_update(self.currentCard)
            
            self.create_feedback_popup('Unfortunately this is incorrect.\nThe answer is:\n'+self.currentCard.translation)

    #meg kell csinalni
    def create_feedback_popup(self, _text):
#        print('feedback popup would have been created: ' + _text)
        self.feedbackPopup = tk.Toplevel(self, width = 150, height = 120, takefocus = True)
        feedbackLabel = tk.Label(self.feedbackPopup, text = _text)
        feedbackLabel.place(width = 130, height = 60, relx = 0.5, y = 40, anchor = CENTER)
        closeFeedbackButton = tk.Button(self.feedbackPopup, text = 'OK')
        closeFeedbackButton.bind('<KeyRelease-Return>', self.close_feedback_popup)
        closeFeedbackButton.bind('<ButtonRelease-1>', self.close_feedback_popup)
        closeFeedbackButton.place(relx = 0.5, rely = 1, y = -20, anchor = CENTER)
        closeFeedbackButton.focus()


    def close_feedback_popup(self, event):
        self.feedbackPopup.destroy()
        self.display_next_query()

    def quit_session(self, event):
        self.queryPopup.destroy()

    def create_insertion_popup(self, event):
        self.insertionPopup = tk.Toplevel(self, width = 300, height = 200, takefocus = True)
        wordLabel = tk.Label(self.insertionPopup, text = 'Word: ')
        wordLabel.place(width = 100, height = 20, relx = 0, rely = 0.33, x=5, anchor = NW)
        
        self.wordInput = tk.Entry(self.insertionPopup)
        self.wordInput.place(width = 150, height = 20, relx = 0, rely = 0.33, x=120, anchor = NW)
        self.wordInput.focus()

        translationLabel = tk.Label(self.insertionPopup, text = 'Translation: ')
        translationLabel.place(width = 100, height = 20, relx = 0, rely = 0.66, x=5, anchor = NW)
        
        self.translationInput = tk.Entry(self.insertionPopup)
        self.translationInput.place(width = 150, height = 20, relx = 0, rely = 0.66, x = 120, anchor = NW)
        self.translationInput.bind('<KeyRelease-Return>', self.insert_flashcard)

        insertButton = tk.Button(self.insertionPopup, text = 'Add')
        insertButton.bind('<ButtonRelease-1>', self.insert_flashcard)
        insertButton.bind('<KeyRelease-Return>', self.insert_flashcard)
        insertButton.place(relx = 0.5, rely = 1, y = -30, anchor = CENTER)

    def insert_flashcard(self, event):
        _word = self.wordInput.get()
        _translation = self.translationInput.get()
        _card = flashcard.Flashcard(0, _word, _translation)
        db.insert_new_card(_card)
        self.insertionPopup.destroy()
        leitner.initialize()
        print('Database reloaded.')


root = tk.Tk()
app = Application(master=root)

