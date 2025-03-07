"""
This file defines the player class, which will represent the player of the
game.
"""

import random as rd

from .hand import Hand

class Player:
    def __init__(self, starting_bank:int, id:int, strategy:str = 'strict'):
        """
        This class represents a player in the game.

        Args:
            starting_bank (int): starting bank amount
            id (int): numeric ID
            strategy (str, optional): string specifying strategy. Can be 'strict', 'soft', 'rand'. Defaults to 'strict'.
        """
        self._id = id
        self._bank = starting_bank
        self._strategy = strategy
        
        # will be str, assigned by dealer
        self._blind = None
        
        # will be a Hand instance, assigned by dealer
        self._hand = None
        
        # will be bool if player is in game or not, assigned by dealer
        self._active = None
        
        # action string to pass to round
        self.action_str = None
        
        # amount to pass along with bet
        self.bet_amount =  0
        
        
        
    def bet(self, amount:int):
        """
        method to execute a bet action

        Args:
            amount (int): amount to bet
        """
        self.bank = self._bank - amount
        self.bet_amount = self.bet_amount + amount
        
        
    def check(self, amount:int):
        """
        method to execute a check action

        Args:
            amount (int): amount to check
        """
        if amount > 0:
            self.bank = self._bank - amount
            self.bet_amount = self.bet_amount +  amount
        
        
    def earn(self, amount:int): 
        """
        method to add value to bank after a win

        Args:
            amount (int): amount won to add to bank
        """
        self.bank = self.bank + amount 
        
        
    def get_action(self, min_bet:int) -> tuple:
        """
        This method gets the computer action based on the
        initialized strategy.

        Returns:
            str: action to be taken by computer 'fold', 'raise', 'call/check'
        """
        
        actions = ['check', 'bet', 'fold']
        
        if self._strategy == 'strict':
            weight = [0.90, 0.05, 0.05]
            bet_max = int(self.bank * 0.05)
        elif self._strategy == 'soft':
            weight = [0.70, 0.25, 0.05]
            bet_max = int(self.bank * 0.1)
        elif self._strategy == 'rand':
            weight = [0.34, 0.33, 0.33]
            bet_max = int(self.bank * 0.15)
   
        self.action_str = rd.choices(actions, weight)[0]    
        return rd.randint(min_bet, min_bet + bet_max)
    
        
        
    def _set_action(self, action_str: str) -> None:
        """
        Action str to pass to round to specify action

        Args:
            action_str (str): action string to act on when entering betting round

        Raises:
            ValueError: Error raised if arg is not a valid action
        """
        if (isinstance(action_str, str) is True) and (action_str in ['fold', 'bet', 'check']):
            self.action_str = action_str            
        else:
            raise ValueError('Please pass a valid action string, "bet", "raise", "fold".')
        
        
    def _clear_action(self):
        """
        Helper method to clear action string
        """
        self.action_str = None
        
        
    def _clear_bet_amount(self): 
        """
        Helper method to clear bet amount
        """
        self.bet_amount = 0
        
        
    @property
    def id(self): 
        return self._id
    
    @id.setter
    def id(self, value):
        if isinstance(value, int) is False:
            raise TypeError("Please pass a valid integer for id")
        
        self._id = value
        
        
    @property
    def bank(self):
        return self._bank
        
    @bank.setter
    def bank(self, value):
        if isinstance(value, int) is False:
            raise TypeError("Please pass a valid integer for starting bank")
        
        self._bank = value
        
    @property
    def blind(self):
        return self._blind
        
    @blind.setter
    def blind(self, value):
        if value != None:
            if (isinstance(value, str) is False): 
                raise TypeError("Please pass a valid blind size")
            
            if value not in ['small', 'large']:
                raise ValueError('Please assign "small" or "large" blind only')
        
        self._blind = value
        
        
    @property
    def hand(self):
        return self._hand
    
    @hand.setter
    def hand(self, value): 
        if value != None:
            if (isinstance(value, Hand) is False) and (value != None):
                raise TypeError("Please pass a valid instance of Hand")
        
        self._hand = value
        
        
    @property
    def strategy(self):
        return self._strategy
        
    @strategy.setter
    def strategy(self, value):
        if value != None:
            if (isinstance(value, str) is False): 
                raise TypeError("Please pass a valid strategy string")
            
            if value not in ['soft', 'strict', 'rand']:
                raise ValueError('Please assign "soft", "strict", "rand" strategy only')
        
        self._blind = value