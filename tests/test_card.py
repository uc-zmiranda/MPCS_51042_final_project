import pytest
from src import Card

def test_card_str_spade():
    """Test that a spade card returns the correct string """
    card = Card("A", "spade")
    # Unicode for spade is \u2660
    assert str(card) == "A\u2660"

def test_card_str_heart():
    """Test that a heart card returns the correct string """
    card = Card("10", "heart")
    # Unicode for heart is \u2665
    assert str(card) == "10\u2665"

def test_invalid_rank():
    """Test that an invalid rank raises a ValueError"""
    with pytest.raises(ValueError):
        Card("B", "heart")

def test_invalid_suit():
    """Test that an invalid suit raises a ValueError
    """
    with pytest.raises(ValueError):
        Card("A", "invalid")

def test_rank_type_error():
    """Test that providing a non-string rank raises TypeError"""
    with pytest.raises(TypeError):
        Card(10, "heart")  # rank must be a string

def test_suit_type_error():
    """Test that providing a non-string suit raises TypeError"""
    with pytest.raises(TypeError):
        Card("A", 10)  # suit must be a string