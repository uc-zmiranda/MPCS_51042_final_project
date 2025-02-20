from collections import Counter
from card import Card     


class HandClassifier:
    def __init__(self, cards:list[Card]):
        self.cards = cards
        self._make_counter_lists()
        self._parse_hand_rank()
        
        
    def _is_flush(self) -> None:
        self.is_flush = any([x for x in self._suit_counter.values() if x >= 5])
        
        
    def _is_royal(self) -> None:
        rev_rank_idx = self._rank_idx[::-1]
        self.is_royal = ([12, 11, 10, 9, 8] == rev_rank_idx[0:5])
        
        
    def _is_straight(self) -> None:
        consecutive = 1
        for idx, rank in [x for x in enumerate(self._rank_idx)][1:]:
            if rank == self._rank_idx[idx-1] + 1:
                consecutive += 1
            else:
                consecutive = 1
                
        if consecutive >= 5:
            self.is_straight = True
        else:
            self.is_straight = False        
         
            
    def _is_full_house(self) -> None:
        self.is_full_house = ((2 in self._rank_counter.values()) and (3 in self._rank_counter.values()))
        
        
    def _is_two_pair(self) -> None: 
        ## checking if two pair
        # getting number of pairs
        pair_counter = Counter(self._rank_counter)
        # if there is a pair
        if (2 in pair_counter.keys()):
            # check if there are two pairs
            if 2 == Counter(self._rank_counter)[2]:
                self.is_two_pair = True
            else:
                self.is_two_pair = False
        else:
            self.is_two_pair = False 
        
            
    def _is_pair(self) -> None:
        # finding highest pair
        self.is_four_kind = False
        self.is_three_kind = False
        self.is_pair = False
        
        max_pair_count = max([x for x in self._rank_counter.values()])
        
        if max_pair_count == 4:
            self.is_four_kind = True
        elif max_pair_count == 3: 
            self.is_three_kind = True
        elif max_pair_count == 2:
            self.is_pair = True
               

    def _parse_hand_rank(self) -> str:
        
        self._is_flush()
        self._is_royal()
        self._is_straight()
        self._is_full_house()
        self._is_two_pair()
        self._is_pair()

        
    def calc_hand_rank(self) -> float:
        # royal flush
        if ((self.is_royal) & (self.is_flush)):
            return (self._calc_hand_score('royal_flush'), 'royal_flush', )
        
        # straight flush
        elif ((self.is_straight) & (self.is_flush)):
            return (self._calc_hand_score('straight_flush'), 'straight_flush')
        
        # four kind
        elif (self.is_four_kind):
            return (self._calc_hand_score('four_kind'), 'four_kind')
        
        # full house
        elif (self.is_full_house):
            return (self._calc_hand_score('full_house'), 'full_house')
        
        # straight
        elif (self.is_straight):
            return (self._calc_hand_score('straight'), 'straight')
        
        # three of a kind
        elif (self.is_three_kind):
            return (self._calc_hand_score('three_kind'), 'three_kind')
        
        # two pair
        elif (self.is_two_pair):
            return (self._calc_hand_score('two_pair'), 'two_pair', )

        # pair
        elif (self.is_pair):
            return (self._calc_hand_score('pair'), 'pair', )
        
        # high card
        else:
            return (self._calc_hand_score('high'), 'high')
        
        
    def _make_counter_lists(self) -> None: 
        self._rank_counter = Counter([card.rank for card in self.cards])
        self._suit_counter = Counter([card.suit for card in self.cards])
        self._rank_idx = sorted([self._calc_rank_idx(card.rank) for card in self.cards])
        
    
    @staticmethod
    def _calc_rank_idx(card_rank:str) -> int:
        return ['2','3','4','5','6','7','8','9','10','J','Q','K','A'].index(card_rank)
    
        
    @staticmethod
    def _calc_hand_score(hand_type:str)-> int:
        hand_rank_dict = {
                            'high': 0,
                            'pair': 1,
                            'two_pair': 2,
                            'three_kind': 3,
                            'straight': 4,
                            'flush': 5,
                            'full_house': 6,
                            'four_kind': 7,
                            'straight_flush': 8,
                            'royal_flush': 9,
                        }
        
        return hand_rank_dict[hand_type]        
    
        

def main(): 
    test = HandClassifier(Card('A', 'heart'), Card('3', 'heart'), Card('K', 'spade'), Card('Q', 'heart'), Card('J', 'heart'), Card('10', 'diamond'), Card('8', 'club'))
    print(test.calc_hand_rank())
    
    
if __name__== "__main__": 
    main()