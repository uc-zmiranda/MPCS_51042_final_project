import pytest
import random

from src import Player
from src import Hand
from src import Card

def test_initialization():
    """Check that a Player is initialized correctly"""
    p = Player(100, 1, strategy="strict")
    assert p.id == 1
    assert p.bank == 100
    assert p.strategy == "strict"
    
    # These properties are set by the dealer so None on init
    assert p.blind is None
    assert p.hand is None
    assert p._active is None
    assert p.action_str is None
    assert p.bet_amount == 0

def test_bet_method():
    """Check that calling bet decreases bank and increases bet_amount"""
    p = Player(100, 1)
    p.bet(10)
    assert p.bank == 90
    assert p.bet_amount == 10

def test_check_method():
    """Check that calling check decreases bank and increases bet_amount"""
    p = Player(100, 1)
    p.check(15)
    assert p.bank == 85
    assert p.bet_amount == 15

def test_earn_method():
    """Check that earning increases bank"""
    p = Player(100, 1)
    p.earn(50)
    assert p.bank == 150

def test_get_action():
    """Check that get_action returns a valid bet amount and sets action_str"""
    p = Player(100, 1, strategy="strict")
    # For strict strategy, bet_max = int(bank * 0.05)
    # With bank 100, bet_max should be 5. So result should be between min_bet and min_bet+5
    min_bet = 10
    result = p.get_action(min_bet)
    assert isinstance(result, int)
    assert min_bet <= result <= (min_bet + 5)
    assert p.action_str in ["check", "bet", "fold"]

def test_set_action_valid():
    """Check that _set_action sets action_str correctly"""
    p = Player(100, 1)
    p._set_action("fold")
    assert p.action_str == "fold"
    p._set_action("check")
    assert p.action_str == "check"
    p._set_action("bet")
    assert p.action_str == "bet"

def test_set_action_invalid():
    """Check that _set_action raises a ValueError correctly"""
    p = Player(100, 1)
    with pytest.raises(ValueError):
        p._set_action("raise")
    with pytest.raises(ValueError):
        p._set_action("foo")

def test_clear_action():
    """Check that _clear_action resets action_str"""
    p = Player(100, 1)
    p.action_str = "bet"
    p._clear_action()
    assert p.action_str is None

def test_clear_bet_amount():
    """Check that _clear_bet_amount resets bet_amount to 0"""
    p = Player(100, 1)
    p.bet_amount = 50
    p._clear_bet_amount()
    assert p.bet_amount == 0

def test_id_setter_type_error():
    """Check that setting id to a non-int raises a TypeError"""
    p = Player(100, 1)
    with pytest.raises(TypeError):
        p.id = "not an int"

def test_bank_setter_type_error():
    """Check that setting bank to a non-int raises a TypeError"""
    p = Player(100, 1)
    with pytest.raises(TypeError):
        p.bank = "not an int"

def test_blind_setter_valid():
    """Check that setting blind to a valid string works."""
    p = Player(100, 1)
    p.blind = "small"
    assert p.blind == "small"
    p.blind = "large"
    assert p.blind == "large"

def test_blind_setter_invalid():
    """Check that setting blind to an invalid value raises an error."""
    p = Player(100, 1)
    with pytest.raises(ValueError):
        p.blind = "medium"
    with pytest.raises(TypeError):
        p.blind = 123

def test_hand_setter_valid():
    """Check that setting hand to a valid Hand instance works."""
    hand_instance = Hand([])
    p = Player(100, 1)
    p.hand = hand_instance
    assert p.hand is hand_instance

def test_hand_setter_invalid():
    """Check that setting hand to a non-Hand value raises a TypeError."""
    p = Player(100, 1)
    with pytest.raises(TypeError):
        p.hand = "not a hand"

def test_strategy_setter_valid():
    """Check that setting strategy to a valid string works."""
    p = Player(100, 1)
    assert p._strategy == "strict"
    p._strategy = "soft"
    assert p._strategy == "soft"
    p._strategy = "rand"
    assert p._strategy == "rand"

def test_strategy_setter_invalid():
    """Check that setting strategy to an invalid value raises an error."""
    p = Player(100, 1)
    with pytest.raises(TypeError):
        p.strategy = 123
    with pytest.raises(ValueError):
        p.strategy = "aggressive"