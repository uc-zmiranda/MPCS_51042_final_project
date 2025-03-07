#!/usr/bin/env python3

from src import Player
from src import Dealer
from src import HumanPlayer


        
def main():
    players = [Player(1000,2, "rand"), HumanPlayer(1000,1), Player(1000,3), Player(1000,4, "soft")]
    dealer = Dealer(players)
    
    
    
if __name__ == '__main__':
    main()     
        
        