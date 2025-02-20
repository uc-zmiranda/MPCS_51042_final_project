"""
This class defines a player in Texas Code Em'
"""

from hand import Hand

class Player:
    def __init__(self, starting_pot:int, id:int):
        """
        This class defines a player in the game. It has a pot.

        Args:
            starting_pot (int): The starting pot of the player
        """
        self._id = id
        self._pot = starting_pot
        
        # will be int
        self._blind = None
        
        # will be list of [Card]
        self._hand = None
        
        
    def bet(self, amount:int):
        self._pot = self._pot - amount
        
    def earn(self, amount:int): 
        self._pot = self.pot + amount 
        
    @property
    def id(self, value):
        if isinstance(value, int) is False:
            raise TypeError("Please pass a valid integer for id")
        
        self._id = value
        
    @property
    def pot(self, value):
        if isinstance(value, int) is False:
            raise TypeError("Please pass a valid integer for starting pot")
        
        self._pot = value
        
    @property
    def blind(self, value):
        if isinstance(value, str) is False: 
            raise TypeError("Please pass a valid blind size")
        
        if value not in ['small', 'large']:
            raise ValueError('Please assign "small" or "large" blind only')
        
        self._blind = value
        
    @property
    def hand(self, value): 
        if isinstance(value, Hand) is False:
            raise TypeError("Please pass a valid instance of Hand")
        
        self._hand = value