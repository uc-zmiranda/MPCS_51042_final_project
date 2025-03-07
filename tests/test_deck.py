import pytest
from src import Deck
from src import Card


def test_deck_initial_length():
    """Checking deck has 52 cards."""
    deck = Deck()
    assert len(deck) == 52

def test_draw_decreases_length():
    """Checking draw correctly removes card"""
    deck = Deck()
    card = deck.draw()
    assert isinstance(card, Card)
    assert len(deck) == 51

def test_draw_all_cards():
    """Checking drawing all 52 cards and making sure they are all unique"""
    deck = Deck()
    drawn_cards = [deck.draw() for _ in range(52)]
    assert len(deck) == 0
    card_strs = [str(card) for card in drawn_cards]
    # Ensure we got 52 unique cards
    assert len(set(card_strs)) == 52

def test_reset_deck():
    """Checking reset"""
    deck = Deck()
    deck.draw()
    assert len(deck) == 51
    deck.reset()
    assert len(deck) == 52

def test_shuffle_changes_order():
    """Checking that shuffling correct randomizes cards"""
    deck = Deck()
    original_order = deck.cards.copy()
    deck.shuffle()
