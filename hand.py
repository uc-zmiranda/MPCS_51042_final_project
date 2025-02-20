from card import Card

class Hand:
    def __init__(self, cards:list[Card]): 
        self._cards = cards
        self._type_int = None
        self._type_str = None
    
    def add_card(self, card:Card) -> None:
        self.cards.append(card)
    
    
    def __str__(self):
        return [str(card) for card in self.cards]
        
    