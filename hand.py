from card import Card

class Hand:
    def __init__(self, cards:list[Card]): 
        """
        This class creates a hand object, which is a collection
        of card objects. This represents the hand that a player 
        is holding

        Args:
            cards (list[Card]): _description_
        """
        self._cards = cards
        self._type_int = None
        self._type_str = None
    
    def add_card(self, card:Card) -> None:
        """
        This method adds a card to the hand

        Args:
            card (Card): Card object to add to the hand
        """
        self.cards.append(card)
        
        
    def print_hand(self) -> None: 
        print([str(card) for card in self._cards])
                

    @property
    def cards(self):
        return self._cards
    
    
    @cards.setter
    def cards(self, value):
        
        if isinstance(value, list) is False:
            raise TypeError("Please pass a list of Card objects.")
        
        for card in value: 
            if isinstance(card, Card) is False: 
                raise TypeError(f'{card} is not a valid Card object.')
        
        self._cards = value
        
   
    def __len__(self) -> int:
        return len(self.cards)
    
    
    def __str__(self) -> str:
        return str([str(card) for card in self.cards])
    
        
    