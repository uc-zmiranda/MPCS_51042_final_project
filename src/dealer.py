"""
This class defines the dealer, which will bridges the GUI and game logic in GameRound
"""

import time

from .player import Player 
from .round import GameRound
from .hand import Hand
from .gui import TexasHoldemDisplay



import random as rd


class Dealer:
    def __init__(self, players:list[Player]):
        """
        This class  defines the dealer class that bridges the game logic in
        GameRound and visualization aspects in GUI.

        Args:
            players (list[Player]): List of players
        """
        self.display = TexasHoldemDisplay()
        self._players = players
        self.phase = 'not_started'
        self.game_state = None    
        self._set_up_game()
        self._run_game()
        
        
    def _set_up_game(self) -> None:
        """
        Pipeline to set up game
        """
        self._seat_players()
        self._make_player_hands()
        self._make_players_active()
        
        
    def _run_game(self) -> None:
        """
        This method manages the between round logic and bridges the visualization and game progression
        """ 
        idx = 0
        game_flag = True
        small_blind = 2
        big_blind = 4
        
        # setting game flag
        while game_flag:
            
            # if only one player, they are winner
            if len(self._players) == 1:
                print(f"Player {self._players[0].id} wins the game!")
                break
            
            
            # finding blind idx
            small_blind_player = self._players[(idx % len(self._players))]
            big_blind_player = self._players[((idx+1) % len(self._players))]
 
            
            # assigning blinds
            self._assign_blinds(small_blind_player, big_blind_player)
            
            # running game round
            round = GameRound(self._players, small_blind, big_blind)
            while self.phase != 'exit':
                self._advance_phase(round)
                if self.phase != 'round_start':
                    self.display.run(self.game_state)
                else: 
                    continue
                
            # sleeping so user can see result
            time.sleep(5)
                            
              
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
            self._make_players_active()
            
            
    def _advance_phase(self, round:GameRound) -> None: 
        """
        This method breaks a GameRound into its distinct steps
        and returns a game state to be passed to TexasHoldEmDisplay

        Args:
            round (GameRound): round instance to play
        """
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
        """
        Helper method to reset actions of each player
        """
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
    
    
        
        
        
    
        

            
    
    
    
    
    
        
    
        
        
    
