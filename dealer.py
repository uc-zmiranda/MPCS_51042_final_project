"""
This class defines the dealer, which will handle the game logic and
logistics.
"""
from card import Card
from deck import Deck
from player import Player 

import random as rd


class Dealer:
    def __init__(self, players:list):
        self._players = players
        self._deck = Deck()
    
    def game_set_up(self) -> None:
        self._seat_players()
        self._assign_blinds()
        self.prepare_deck()
        
    
    def run_game(self):
        pass 
    
    
    def _run_round(self):
        pass 
    
    
    def _seat_players(self) -> None:
        """
        Helper method to seat players randomly.
        """
        self.player_order = rd.shuffle(self.players)
        
    
    def _assign_blinds(self, small_player:Player, large_player:Player) -> None:
        """
        Helper method to assign blinds to players
        """
        # assigning blinds to players
        small_player.blind = "small"
        large_player.blind = "large"

    
        
        
        
def main():
    test = Player(10)
    test2 = Player(50)
    test_card = Card('2', 'diamond')
    test_card2 = Card('A', "diamond")
    
    Dealer([test, test2])
        
if __name__ == '__main__':
    main()
        
        
        
        
    
        
        
        
    
        
        
        
    
        

            
    
    
    
    
    
        
    
        
        
    
