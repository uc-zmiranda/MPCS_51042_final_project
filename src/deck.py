"""
This file defines the deck object that will be used when playing the game
"""

import random as rd
from .card import Card

class Deck:
    def __init__(self):
        """
        This class represent the deck of card that will be used
        when playing the game.
        """
        self.reset()
    
    def draw(self) -> tuple:
        """
        draw a card from the deck and return it to user
        """
        return self.cards.pop()
        
    def shuffle(self):
        """
        Randomizes deck
        """
        rd.shuffle(self.cards)
    
    def reset(self):
        """
        Reset deck to un-shuffled start.
        """
        self.cards = self._make_cards()
    
    def _make_cards(self):
        """
        make cards in deck.
        """   
        # setting return list 
        deck_cards = []
        
        # Setting card ranks
        ranks = ['A', 'J', 'Q', 'K']
        ranks.extend([str(x) for x in range(2,11)])
        
        # making cards
        for suit in ['diamond', 'spade', 'club', 'heart']:
            for rank in ranks:
                deck_cards.append(Card(rank, suit))
        
        return deck_cards
    
    
    def __str__(self) -> str:
        return str([str(card) for card in self.cards])


    def __len__(self) -> int:
        return len(self.cards)