"""
This file defines a GameRound which represents the stages of a round in poker
"""

from .deck import Deck
from .winner import WinnerFinder
from .player import Player
from .human_player import HumanPlayer


class GameRound:
    def __init__(self, 
                 players:list[Player], 
                 small_blind_amt:int, 
                 large_blind_amt:int):
        """
        This class represents a typical game round of Texas HoldEm. It will be 
        used in conjunction with the Dealer class to run a Texas HoldEm game.

        Args:
            players (list[Player]): list of players to play round.
            small_blind_amt (int): small blind amount (determined by Dealer).
            large_blind_amt (int): large blind amount (determined by Dealer).
        """
        
        self._players = players
        self._active_players = players
        self._small_blind_amt = small_blind_amt
        self._large_blind_amt = large_blind_amt
        self.pot = 0
        self.community_cards = []
        self.winners = None

        
    def set_up_round(self) -> None: 
        """
        Pipeline to set up round to be played 
        """
        self._shuffle_deck()
        self._take_blinds()
        
        
    def deal_hand(self) -> dict:
        """
        Method to deal hand to players

        Returns:
            dict: game state dict for visualization
        """
        self._deal_cards(2, True)
        return self._game_state_dict()
        
        
    def deal_flop(self) -> None:
        """
        Method to deal flop to community

        Returns:
            dict: game state dict for visualization
        """
        self._deal_cards(3, False)
        return self._game_state_dict()
    
    
    def deal_turn(self) -> None:
        """
        Method to deal turn to community

        Returns:
            dict: game state dict for visualization
        """
        self._deal_cards(1, False)
        return self._game_state_dict()
    
    def deal_river(self) -> None:
        """
        Method to deal river to community

        Returns:
            dict: game state dict for visualization
        """
        self._deal_cards(1, False)
        return self._game_state_dict()   
                
    
    def take_bets(self) -> dict: 
        # setting current bet amount        
        idx = 0
             
        # starting bet loop
        while True: 
            # getting/updating active players
            active_players = [player for player in self._active_players if (player._active is True)]
            
            # checking how many active players
            if len(active_players) == 1:
                self.finish_round()
                break
            
            # getting current max bet of active players
            current_bet = max([player.bet_amount for player in active_players])
                        
            # getting bet end flags
            active_players_flag = not active_players
            match_bet_flag = all([(player.bet_amount == current_bet) for player in active_players])
            action_flag = (len([player for player in active_players if player.action_str != None]) == len(active_players))
            

            # if bet end flags are met, end betting round
            if active_players_flag or ((match_bet_flag) and (action_flag)):
                self._active_players = [player for player in active_players if (player._active)]                
                break
            
            # getting player
            player = active_players[idx % len(active_players)]
            idx = idx + 1
            
            # if player already folded, continue
            if player._active is False:
                continue
            
            # getting diff to meet current bet
            call_amt = current_bet - player.bet_amount 
            
            # checking if human player
            if isinstance(player, HumanPlayer):
                player_amt = player.get_action(self.large_blind_amt, call_amt)
            
            # computer action
            else:
                player_amt = player.get_action(self._large_blind_amt)
                        
            
            # if a player cannot afford bank, make them fold
            if call_amt > player.bank:
                player.action_str = 'fold'
                
            print('----------------')
            
            # if player folds, make them inactive and tell table
            if player.action_str == 'fold': 
                if player.id == 1:
                    print(f'You folded.')
                else:
                    print(f'Player {player.id} folded.')
                    
                player._active = False
                print('----------------')
            
            # if player check/calls,
            elif player.action_str == 'check':
                if call_amt > 0:
                    player.check(call_amt)
                    self.pot += call_amt
                    if player.id == 1:
                        print(f"You call for {call_amt}.")
                    else:
                        print(f"Player {player.id} calls for {call_amt}.")
                else:
                    if player.id == 1:
                        print("You checked.")
                    else:
                        print(f"Player {player.id} checks.")
                print('----------------')
                    
            # if player is raising
            else:
                if call_amt > 0: 
                    player.check(call_amt)
                    self.pot += call_amt
                player.bet(player_amt)
                self.pot = self.pot + player_amt
                if player.id == 1:
                    print(f"You raise by {player_amt} for a total of {player.bet_amount}")
                else:
                    print(f"Player {player.id} raises by {player_amt} for a total of {player.bet_amount}")
                print('----------------')
                
            # for other in active_players:
            #     if other != player:
            #         player._clear_action()
            
        # clear betting info
        for player in self._active_players:
            player._clear_action()
            player._clear_bet_amount()
            
        #print(f'Betting round complete. Pot is ${self.pot}')
        
        return self._game_state_dict()
        
        
    def finish_round(self) -> dict:
        """
        Pipe line to run post-round tasks

        Returns:
            dict: game_state_dict for visualization
        """
        self._get_winner()
        self._pay_out_pot()
        return self._game_state_dict()
        
        
        
    def _shuffle_deck(self) -> None:
        """
        method to shuffle deck in prep for game
        """
        self.deck = Deck()
        self.deck.shuffle()
        
    def _take_blinds(self) -> None:
        """
        takes blind from players 
        """
        for player in self._players:
            if player.blind == "large":
                player.bet(self.large_blind_amt)
                self.pot = self.pot + self.large_blind_amt
            elif player.blind == 'small':
                player.bet(self.small_blind_amt)
                self.pot = self.pot + self.small_blind_amt
            else:
                continue
            
        
    def _deal_cards(self, count:int, to_player:bool) -> None: 
        """
        Method to deal cards directly to player or community hand

        Args:
            count (int): number of cards to deal
            to_player(bool): True if deal to player, False deal to community
        """
        
        # dealing to players
        if to_player is True:
            for player in self._active_players:
                i = 0
                while i < count:  
                    i = i + 1
                    card = self.deck.draw()
                    player.hand.add_card(card)
                        
        # dealing to community cards
        else:
            i = 0
            while i < count: 
                i = i + 1
                card = self.deck.draw()
                self.community_cards.append(card)
        
        
    def _get_winner(self) -> list: 
        """
        Method to call WinnerFinder and determine the winner.

        Returns:
            list: list of winner(s)
        """
        for player in self._active_players:
            player.hand._cards.extend(self.community_cards)
        
        self.winners = WinnerFinder(self._active_players).winner
        
        
    def _make_winner_str(self) -> str: 
        """
        Method to make winner string to inform display of winner

        Returns:
            str: string that tells the display of the pot and who the winner was
        """
        winner_str = f'The final pot was {self.pot}\n'
        winner_str = winner_str + 'The winners are:\n'
        for winner in self.winners:
            winner_str = winner_str + f" {winner.id}\n"
        
        return winner_str
        
        
    def _pay_out_pot(self) -> None:
        """
        Method to split pot
        """
        # splitting pot by number of players
        split_pot = self.pot/len(self.winners)
        for winner in self.winners:
            winner.earn(int(split_pot))
        
  
                
    def _game_state_dict(self) -> dict:
        """
        This method crates the state dict to pass to
        the display.

        Returns:
            dict: dictionary of game state
        """
        
        # pulling player hand
        for player in self._players:
            if isinstance(player, HumanPlayer) is True: 
                human_hand = player.hand
                human_bank = player.bank
        
        game_state_dict = {
            'player_cards': human_hand._cards[0:2],
            'player_bank': human_bank,
            'community_cards': self.community_cards,
            'pot': self.pot,
            'left_opp_cards': ['card 1', 'card 2'],
            'top_opp_cards': ['card 1', 'card 2'],
            'right_opp_cards': ['card 1', 'card 2']
        }
                
        if self.winners != None: 
            game_state_dict['winner_str'] = self._make_winner_str()
            game_state_dict['left_opp_cards'] = [player.hand._cards for player in self._players if (player.id == 2)][0][0:2],
            game_state_dict['top_opp_cards'] = [player.hand._cards for player in self._players if (player.id == 3)][0][0:2],
            game_state_dict['right_opp_cards'] = [player.hand._cards for player in self._players if (player.id == 4)][0][0:2]
            
        return game_state_dict
            

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
    
    @property
    def small_blind_amt(self):
        return self._small_blind_amt
    
    @small_blind_amt.setter
    def small_blind_amt(self, value):
        if isinstance(value, int) is False:
            raise TypeError('Please pass valid int for small blind amount')
        
        self._small_blind_amt = value

    @property
    def large_blind_amt(self):
        return self._large_blind_amt
        
    @large_blind_amt.setter
    def large_blind_amt(self, value):
        if isinstance(value, int) is False:
            raise TypeError('Please pass valid int for small blind amount')
        
        self._large_blind_amt = value
