# tests/test_hand.py
import pytest
from src import Card
from src import Hand

def test_hand_initialization():
    """Checking hand is initialized correctly"""
    card1 = Card("A", "spade")
    card2 = Card("10", "heart")
    hand = Hand([card1, card2])
    assert len(hand) == 2
    assert hand.cards == [card1, card2]

def test_add_card():
    """Test that add_card correctly adds a card"""
    card1 = Card("A", "spade")
    card2 = Card("10", "heart")
    hand = Hand([card1])
    hand.add_card(card2)
    assert len(hand) == 2
    assert hand.cards == [card1, card2]


def test_cards_setter_valid():
    """Test that the cards setter works"""
    card1 = Card("A", "spade")
    card2 = Card("10", "heart")
    hand = Hand([])
    hand.cards = [card1, card2]
    assert hand.cards == [card1, card2]

def test_cards_setter_invalid_type():
    """Test that setting cards as non-list raises a TypeError"""
    card1 = Card("A", "spade")
    hand = Hand([card1])
    with pytest.raises(TypeError):
        hand.cards = "not a list"

def test_cards_setter_invalid_item():
    """Test that setting cards to a list with a non-Card raises a TypeError"""
    card1 = Card("A", "spade")
    hand = Hand([card1])
    with pytest.raises(TypeError):
        hand.cards = [card1, "not a card"]
