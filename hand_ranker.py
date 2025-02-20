"""
This method defines a class that takes 2 Card instances and returns their rank
"""
from card import Card
from hand import Hand
from collections import Counter
from player import Player
from hand_classifier import HandClassifier


class HandRanker:
    def __init__(self, players:list[Player]):
        self.players = players
        self.hand_ranks = []
        self.winner = self._calc_winner()
        
    
    def _calc_winner(self):
        self._classify_hands()
        return self._get_winner()
        
        
    def _classify_hands(self):
        # iterating through player tuples
        for player in self.players: 
            # calculating hands and appending it
            player._hand._type_int, player._hand._type_str = HandClassifier(player._hand._cards).calc_hand_rank()
            
    
    def _get_winner(self) -> list:
        # getting highest hand rank
        highest_rank = max([player._hand._type_int for player in self.players])
        
        # getting winners
        winners = [player for player in self.players if (player._hand._type_int == highest_rank)]
        
        # if there is a tie in hand types run tie breaker, otherwise return winner
        if len(winners) > 1:
            return TieHandler(winners)
        else:
            return winners
            
            
        
        
class TieHandler:
    def __init__(self, players:list[Player]):    
        self._players = players
        self._winner = self._break_tie()
        self._hand_type = None
        
        
    def _break_tie(self):
        self._set_hand_type()
        self._calc_tie_break()
        
    def _set_hand_type(self):
        
        hand_type = self._players[0]._hand._type_int
        # iterating through players and making sure they all share the
        # same hand type
        for player in self._players[1:]:
            if player._hand._type_int != hand_type:
                raise ValueError("Hand types do not match, you do not need to call TieBreaker")
        
        self._hand_type = hand_type
    
            
    def _calc_tie_break(self):
        if self._hand_type in [4, 8]:
            return self._high_card_tie_break()
            
        elif self._hand_type in [1,2,3,6,7]:
            return self._pair_tie_break()
            
        else:
            return self._card_run_tie_break()
            
        
    # used for straight
    # used for straight flush
    def _high_card_tie_break(self) -> list:
        # setting init values
        highest_straight_rank = 0
        winner = []
                
        # iterating through players and getting highest value
        for player in self.players:
            
            # if straight flush, subset hands to flush else pass normally
            if self._hand_type == 8:
                cards = self._get_flush_cards(player._hand)
            else:
                cards = player._hand
        
            # getting highest straight
            player_highest_rank = self._get_highest_straight(cards)
            # calculating winners
            if player_highest_rank > highest_straight_rank:
                winner = [player]
            elif player_highest_rank < highest_straight_rank:
                continue
            else:
                winner.append(player)
                
        return winner
            
        
        
    # used for high card
    # used for flush
    def _card_run_tie_break(self):
        # setting init values
        hands_ranks = []
        
        # iterating through players 
        for player in self._players:
            # subsetting to only flush cards if a flush hand
            if self._hand_type == 5:
                cards = self._make_rank_idx_list(self._get_flush_cards(player.hand))
            else:
                cards = self._make_rank_idx_list(player._hand._cards)
            
            hands_ranks.append(cards)
        
        # iterating through highest rank of cards
        for idx_tup in zip(*hands_ranks):
            # finding highest rank among all hands
            idx_winner = []
            highest_rank = max(idx_tup)
            # iterating through to find winner
            for idx, rank in enumerate(idx_tup):
                # if idx has highest rank, append them to winner
                if rank == highest_rank:
                    idx_winner.append(idx)
                else:
                    continue
            # if not one winner, continue
            if len(idx_winner) > 1:
                continue
            # if one winner return player
            else:
                return [self._players[idx_winner]]
        
        # if hands completely tie, return both
        return [self._players[idx_winner] for idx_winner in idx_winner]
        
            
    
    # used for all pairs
    # used for two-pairs
    # used for full-house
    def _pair_tie_break(self):
                
        if (self._hand_type == 2) or (self._hand_type == 6):
            hands_ranks = []
            
            # iterating through players
            for player in self._players:
                hands_ranks.append(self._get_pair_ranks(player._hand))                
                
            # iterating through highest rank of pairs
            for idx_tup in zip(*hands_ranks):
                # finding highest rank among all pairs
                idx_winner = []
                highest_rank = max(idx_tup)
                # iterating through to find winner
                for idx, rank in enumerate(idx_tup):
                    # if idx has highest rank, append it to winner
                    if rank == highest_rank:
                        idx_winner.append(idx)
                    else:
                        continue
                # if not one winner, continue
                if len(idx_winner) > 1:
                    continue
                # if one winner return player
                else:
                    return [self._players[idx_winner]]
            
            # if hands completely tie, return both
            return [self._players[idx_winner] for idx_winner in idx_winner]
    
        else:
            
            highest_pair_rank = 0
            for player in self.players:
                player_pair_rank = self._get_pair_ranks(player._hand)
                # calculating winners
                if player_pair_rank > highest_pair_rank:
                    winner = [player]
                elif player_pair_rank < highest_pair_rank:
                    continue
                else:
                    winner.append(player)
                
            return winner
                
    
    
    
    def _get_pair_ranks(self, hand:Hand) -> int:
        """_summary_

        Args:
            kind_count (int): number of matching cards to search for, 5 if two pair.
            hand (Hand): Player hand to return highest pair

        Returns:
            int: index of highest rank
        """
        if self._hand_type == 2: 
            pair_counter = Counter(self._make_rank_idx_list(hand._cards))
            return sorted([rank for (rank, count) in pair_counter if count == 2], reverse=True)
            
        elif self._hand_type == 6:
            pair_counter = Counter(self._make_rank_idx_list(hand._cards))  
            
            max_two_count = max([(rank,count) for (rank, count) in pair_counter if (count == 2)])
            max_three_count = max([(rank,count) for (rank, count) in pair_counter if (count == 3)])
            
            return [max_three_count, max_two_count]
        
            
        else:
            pair_counter = Counter(self._make_rank_idx_list(hand._cards))
            return max([rank for (rank, _) in pair_counter])
        
        
        
    
    def _get_highest_straight(self, hand:Hand) -> int:
        hand_rank_idx = self._make_rank_idx_list(hand)
        best_rank = 0
        consecutive = 1
        
        # iterating through hand ranks
        for idx, rank in [x for x in enumerate(hand_rank_idx)][1:]:
            if rank == hand_rank_idx[idx-1] + 1:
                consecutive += 1
            else:
                consecutive = 1
            # once 5 consective values are found, append highest value to index
            if consecutive >= 5:
                best_rank = hand_rank_idx[idx]
                
        assert best_rank != 0, "Hand does not contain straight"
        return best_rank
    
    

    def _make_rank_idx_list(self, card_list:list[Card]) -> list[int]:
        return sorted([self._calc_rank_idx(card.rank) for card in card_list])
    
    
    @staticmethod
    def _get_flush_cards(hand:Hand) -> list:
        # getting suit of flush
        suits_counter = Counter([card.suit for card in hand._cards])
        
        # returning cards in suit
        return [card for card in hand._cards if card.suit == max(suits_counter) ]
    

    @staticmethod
    def _calc_rank_idx(card_rank:str) -> int:
        return ['2','3','4','5','6','7','8','9','10','J','Q','K','A'].index(card_rank)
    
    
    
def main(): 
    player1 = Player(100, 1)
    player1._hand = Hand([Card('A', 'heart'), Card('A', 'heart'),])   
    
    player2 = Player(200,2)
    player2._hand = Hand([Card('A', 'heart'), Card('A', 'diamond'), Card('A', 'spade')])   
    
    player_list = [player1, player2]
    
    winner_list = HandRanker(player_list).winner
    winner = winner_list[0]
    breakpoint()

    
    
if __name__== "__main__": 
    main()