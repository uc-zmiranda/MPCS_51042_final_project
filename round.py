from deck import Deck
from winner import WinnerFinder
from player import Player
from human_player import HumanPlayer


class GameRound:
    def __init__(self, 
                 players:list[Player], 
                 small_blind_amt:int, 
                 large_blind_amt:int):
        
        self._players = players
        self._active_players = players
        self._small_blind_amt = small_blind_amt
        self._large_blind_amt = large_blind_amt
        self.pot = 0
        self.community_cards = []
        self.winners = None

        
    def set_up_round(self) -> None: 
        self._shuffle_deck()
        self._take_blinds()
        
        
    def deal_hand(self) -> None:
        self._deal_cards(2, True)
        return self._game_state_dict()
        
        
    def deal_flop(self) -> None:
        self._deal_cards(3, False)
        return self._game_state_dict()
    
    def deal_turn(self) -> None:
        self._deal_cards(1, False)
        return self._game_state_dict()
    
    def deal_river(self) -> None:
        self._deal_cards(1, False)
        return self._game_state_dict()   
                
    
    def take_bets(self) -> None: 
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
            
            
            # if a player cannot afford bank
            if call_amt > player.bank:
                for player in self._active_players:
                    player.action_str = 'fold'
            

            # if player folds, make them inactive and tell table
            if player.action_str == 'fold': 
                print(f'Player {player.id} folded.')
                player._active = False
            
            # if player check/calls, 
            elif player.action_str == 'check':
                if call_amt > 0:
                    player.check(call_amt)
                    self.pot = self.pot + call_amt
                    print(f"Player {player.id} calls for {call_amt}.")
                else:
                    print(f"Player {player.id} checks.")
            # if player is betting
            else:
                if isinstance(player, HumanPlayer):
                    player.bet(player_amt)
                else:
                    player.bet(player_amt)
                self.pot = self.pot + current_bet
                print(f"Player {player.id} raises by {call_amt} for a total of {call_amt + current_bet}")
            
        # clear betting info
        for player in self._active_players:
            player._clear_action()
            player._clear_bet_amount()
            
        #print(f'Betting round complete. Pot is ${self.pot}')
        
        return self._game_state_dict()
        
        
    def finish_round(self) -> None:
        self._get_winner()
        self._pay_out_pot()
        print(self._make_winner_str)
        return self._game_state_dict()
        
        
        
    def _shuffle_deck(self) -> None:
        """
        This method will shuffle the deck in preparation for
        running the game
        """
        self.deck = Deck()
        self.deck.shuffle()
        
    def _take_blinds(self) -> None:
        """
        This method takes the blind amount and removes
        it from the player bank
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
        Deals cards directly to player or community hand

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
        for player in self._active_players:
            player.hand._cards.extend(self.community_cards)
        
        self.winners = WinnerFinder(self._active_players).winner
        
        
    def _make_winner_str(self) -> None: 
        winner_str = f'The final pot was {self.pot}\n'
        winner_str = winner_str + 'The winners are:\n'
        for winner in self.winners:
            winner_str = winner_str + f" {winner.id}\n"
        
        return winner_str
        
        
    def _pay_out_pot(self) -> None:
        # splitting pot by number of players
        split_pot = self.pot/len(self.winners)
        for winner in self.winners:
            winner._bank += int(split_pot)
        

    def _print_community_cards(self) -> None: 
        print([str(card) for card in self.community_cards])
        
        
    def _print_human_hand(self) -> None:
        for player in self._active_players:
            if isinstance(player, HumanPlayer): 
                player.hand.print_hand()
                
            
                
    def _game_state_dict(self) -> None: 
        
        # pulling player hand
        for player in self._active_players:
            if isinstance(player, HumanPlayer) is True: 
                human_hand = player.hand
        
        game_state_dict = {
            'player_cards': human_hand,
            'community_cards': self.community_cards,
            'pot': self.pot,
        }
                
        if self.winners != None: 
            game_state_dict['winner_str'] = self._make_winner_str()
            game_state_dict['opponent_cards'] = [player.hand for player in self._active_players if (isinstance(player, HumanPlayer) is False)],
            
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
        
        
        
        
def main(): 
    player1 = HumanPlayer(100, 1)
    player1.active = True
    
    player2 = Player(100, 2)
    player2.active = True
    
    round = GameRound([player1, player2], 2,4)
    
    round.take_bets()
    
if __name__ == '__main__': 
    main()