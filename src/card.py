"""
This file defines the Card class that will represent a playing card. 
"""

class Card:
    def __init__(self, rank:str, suit:str):
        """
        This class represents a playing card. It will consist of
        a rank and suit. 

        Args:
            rank (str): Card number or face card as str (Ex. 2,3,4,...,10,J,Q,K,A)
            suit (str): Card suit as lower case spelled out (options are "spade", "club", "heart", "diamond")
        """
        self.rank = rank
        self.suit = suit
      
        
    @staticmethod
    def _get_suit_symbol(suit_str:str) -> str: 
        """
        Helper method to get suit symbol.
        

        Args:
            suite_str(str): suite string to get symbol for

        Returns:
            str: _string representation of suit symbol
        """
        suite_dict = {"heart":"\u2665",
                      "spade":"\u2660",
                      "diamond":"\u2666",
                      "club":"\u2663"}
        
        return suite_dict[suit_str]
        
        
        
    @property
    def rank(self): 
        return self._rank
    
    @rank.setter
    def rank(self, value): 

        if isinstance(value, str) is False:
            raise TypeError("Rank must be a string")
        
        valid_ranks = ['A','J','Q','K']
        valid_ranks.extend([str(x) for x in range(1,11)])
        
        if value not in valid_ranks: 
            raise ValueError("Please provide a valid playing card rank")
        
        self._rank = value
        
    @property
    def suit(self): 
        return self._suit
    
    @suit.setter
    def suit(self, value):
        
        if isinstance(value, str) is False:
            raise TypeError("Suit must be a string")
        
        try:
            self._get_suit_symbol(value)
        except:
            raise ValueError("Please provide a valid playing card suit")
        
        self._suit = value
        
    def __str__(self):
        return f"{self.rank}{self._get_suit_symbol(self.suit)}"