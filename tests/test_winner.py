from src.card import Card
from src.player import Player
from src.hand import Hand
from src.winner import WinnerFinder, HandClassifier


# Utility function to create a Hand from a list of (rank, suit) tuples.
def create_hand(card_tuples:list[tuple]) -> Hand:
    """
    Helper function to create a hand

    Args:
        card_tuples (list[tuple]): list of tuples of (rank, suite)

    Returns:
        Hand: hand object containing cards specified by card_tuples
    """
    cards = [Card(rank, suit) for rank, suit in card_tuples]
    return Hand(cards)

def test_hand_classifier_high():
    """
    Check that a hand with "high card" is classified as "high"
    """
    # A high card hand: no pair, flush, straight, etc.
    card_tuples = [
        ("2", "heart"),
        ("5", "spade"),
        ("7", "club"),
        ("9", "diamond"),
        ("J", "heart")
    ]
    hand = create_hand(card_tuples)
    classifier = HandClassifier(hand)
    score, rank_str = classifier.calc_hand_rank()
    assert score == 0
    assert rank_str == "high"

def test_hand_classifier_pair():
    """
    Check that a hand containing one pair is classified as a 'pair'
    """
    card_tuples = [
        ("2", "heart"),
        ("2", "club"),
        ("5", "spade"),
        ("7", "diamond"),
        ("J", "heart")
    ]
    hand = create_hand(card_tuples)
    classifier = HandClassifier(hand)
    score, rank_str = classifier.calc_hand_rank()
    assert score == 1
    assert rank_str == "pair"

def test_hand_classifier_full_house():
    """
    Check that a full house is classified correctly
    """
    card_tuples = [
        ("2", "heart"),
        ("2", "club"),
        ("2", "diamond"),
        ("7", "diamond"),
        ("7", "heart")
    ]
    hand = create_hand(card_tuples)
    classifier = HandClassifier(hand)
    score, rank_str = classifier.calc_hand_rank()
    assert score == 6
    assert rank_str == "full_house"

def test_winner_finder_single_winner():
    """
    Create two players with different hand strengths, the player with a pair should win over a high card hand.
    """
    # Player 1: hand with a pair
    pair_cards = [
        ("2", "heart"),
        ("2", "club"),
        ("5", "spade"),
        ("7", "diamond"),
        ("J", "heart")
    ]
    # Player 2: high card hand
    high_cards = [
        ("2", "heart"),
        ("5", "spade"),
        ("7", "club"),
        ("9", "diamond"),
        ("J", "heart")
    ]
    hand_pair = create_hand(pair_cards)
    hand_high = create_hand(high_cards)
    
    player1 = Player(100, 1, strategy="strict")
    player2 = Player(100, 2, strategy="strict")
    player1.hand = hand_pair
    player2.hand = hand_high

    wf = WinnerFinder([player1, player2])
    winners = wf.winner
    # The player with the pair (score 1) should win.
    assert len(winners) == 1
    assert winners[0].id == 1

def test_winner_finder_tie():
    """
    Create two players with identical hands, the WinnerFinder should return both players as winners
    """
    pair_cards = [
        ("2", "heart"),
        ("2", "club"),
        ("5", "spade"),
        ("7", "diamond"),
        ("J", "heart")
    ]
    hand1 = create_hand(pair_cards)
    hand2 = create_hand(pair_cards)
    
    player1 = Player(100, 1, strategy="strict")
    player2 = Player(100, 2, strategy="strict")
    player1.hand = hand1
    player2.hand = hand2

    wf = WinnerFinder([player1, player2])
    winners = wf.winner
    # Both players have the same hand ranking.
    assert len(winners) == 2
    winner_ids = {p.id for p in winners}
    assert winner_ids == {1, 2}