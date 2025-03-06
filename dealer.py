"""
This class defines the dealer, which will handle the game logic and
logistics.
"""
from card import Card
from deck import Deck
from player import Player 
from round import GameRound
from hand import Hand
from human_player import HumanPlayer
from gui import TexasHoldemDisplay


import random as rd


class Dealer:
    def __init__(self, players:list[Player]):
        self.display = TexasHoldemDisplay()
        self._players = players
        self.phase = 'not_started'
        self.game_state = None    
        self._set_up_game()
        self._run_game()
        
        
    def _set_up_game(self) -> None:
        self._seat_players()
        self._make_player_hands()
        self._make_players_active()
        
        
    def _run_game(self) -> None: 
        idx = 0
        game_flag = True
        small_blind = 2
        big_blind = 4
        
        while game_flag:
            
            if len(self._players) == 1:
                print(f"Player {self._players[0].id} wins the game!")
                break
            
            
            # finding blind idx
            small_blind_player = self._players[(idx % len(self._players))]
            big_blind_player = self._players[((idx+1) % len(self._players))]
 
            
                        
            # assigning blinds
            self._assign_blinds(small_blind_player, big_blind_player)
            
            round = GameRound(self._players, small_blind, big_blind)
            while self.phase != 'exit':
                print(self.phase)
                self._advance_phase(round)
                if self.phase != 'round_start':
                    self.display.run(self.game_state, True)
                else: 
                    continue
                            
              
            # resetting blinds
            big_blind_player.blind = None
            small_blind_player.blind = None
            
            # incrementing for next iteration
            small_blind = small_blind + 2
            big_blind = big_blind + 2
            idx = idx + 1
            
            # cleaning up round
            self._make_player_hands()
            self._reset_action_str()
            self._elim_players(big_blind)
            self._reset_game_state()
            
            
            
    def _advance_phase(self, round:GameRound) -> None: 
        
        if self.phase == 'not_started':
            round.set_up_round()
            self.phase = 'round_start'
        
        elif self.phase == 'round_start':
            self.game_state = round.deal_hand()
            self.phase = 'pre_flop'
            
        elif self.phase == 'pre_flop':
            self.game_state = round.take_bets()
            self.phase = 'flop'
            
        elif self.phase == 'flop':
            self.game_state = round.deal_flop()
            self.phase = 'pre_turn'
            
        elif self.phase == 'pre_turn':
            self.game_state = round.take_bets()
            self.phase = 'turn'
        
        elif self.phase == 'turn':
            self.game_state = round.deal_turn()
            self.phase = 'pre_river'
            
        elif self.phase == 'pre_river':
            self.game_state = round.take_bets()
            self.phase = 'river'
            
        elif self.phase == 'river':
            self.game_state = round.deal_river()
            self.phase = 'pre_finish'
            
        elif self.phase == 'pre_finish':
            self.game_state = round.take_bets()
            self.phase = 'round_finish'
            
        elif self.phase == 'round_finish':
            self.game_state = round.finish_round()
            self.phase = 'exit'
            
        elif self.phase == 'exit':
            return
            

     
        
    def _seat_players(self) -> None:
        """
        Helper method to seat players randomly.
        """
        
        rd.shuffle(self._players)
    
    
    def _make_player_hands(self) -> None: 
        """
        Helper method to make player hand instances
        """
        
        for player in self._players:
            player.hand = Hand([])
            
    def _make_players_active(self) -> None: 
        """
        Helper method to make players active
        """
        
        for player in self._players:
            player._active = True
            
    def _reset_game_state(self) -> None:
        """
        Helper method to clear game state
        """
        self.phase = 'not_started'
            
            
    def _elim_players(self, elim_blind:int) -> None: 
        """
        Helper method to elim players who cannot make the blind

        Args:
            elim_blind (int): elimination threshold
        """
        self._players = [player for player in self._players if player.bank > elim_blind]
            
        
    def _reset_action_str(self) -> None: 

        for player in self._players:
            player._clear_action()
            
            
    @staticmethod
    def _assign_blinds(small_player:Player, large_player:Player) -> None:
        """
        Helper method to assign blinds to players
        """
        # assigning blinds to players
        small_player.blind = "small"
        large_player.blind = "large"
            

    
    @property
    def players(self):
        return self._players
    
    @players.setter
    def players(self, value):
        
        if isinstance(value, list) is False:
            raise TypeError('Please pass a list of players.')
        
        for player in value: 
            if isinstance(player, Player) is False: 
                raise TypeError(f'{player} is not a valid player object.')

        self._players = value
    

    
        
def main():
    #players = [HumanPlayer(100,2)]
    players = [Player(1000,1, "rand"), HumanPlayer(1000,2), Player(1000,3), Player(1000,4, "soft")]
    dealer = Dealer(players)
    
    
    
if __name__ == '__main__':
    main()     
        
        
    
        
        
        
    
        

            
    
    
    
    
    
        
    
        
        
    
