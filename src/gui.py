import pygame
import sys

from .card import Card


class TexasHoldemDisplay:
    def __init__(self, width=800, height=600):
        """
        This class creates the display to inform the player of game information

        Args:
            width (int, optional): width of display window in pixels. Defaults to 800.
            height (int, optional): height of display window in pixels. Defaults to 600.
        """
        
        pygame.init()
        self.WIDTH, self.HEIGHT = width, height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.GREEN = (0, 128, 0)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.CARD_WIDTH = 60 
        self.CARD_HEIGHT = 90
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Texas Hold'em")
        # font that supports card suites
        font_name = pygame.font.match_font("dejavusans")
        self.font = pygame.font.Font(font_name, 24)


    def draw_table(self) -> None:
        """
        method to draw background
        """
        self.screen.fill(self.GREEN)

    def draw_card(self, card_text:str, pos:float) -> None:
        """
        Method to draw cards given with card_text at position pos.

        Args:
            card_text (str): text to put on card
            pos (float): position to draw card
        """
        card_rect = pygame.Rect(pos[0], pos[1], self.CARD_WIDTH, self.CARD_HEIGHT)
        pygame.draw.rect(self.screen, self.WHITE, card_rect)
        pygame.draw.rect(self.screen, self.BLACK, card_rect, 2)
        
        if ('\u2666' in card_text) or  ("\u2665" in card_text):
            text_surface = self.font.render(card_text, True, self.RED)
        else:
            text_surface = self.font.render(card_text, True, self.BLACK)

        text_rect = text_surface.get_rect(center=card_rect.center)
        self.screen.blit(text_surface, text_rect)
        

    def render_game_state(self, game_state:dict) -> None:
        """
        Renders current game state using game state dict, updates the following: 
        * community cards
        * player cards
        * left player cards
        * right player cards
        * top player cards
        * pot
        * player bank
        * game winner string
        
        Args:
            game_state (dict): game state dictionary from GameRound
        """
        self.draw_table()

        # Draw community cards (center of table)
        community_cards = game_state['community_cards']
        n = len(community_cards)
        if n:
            total_width = self.CARD_WIDTH * n + 20 * (n - 1)
            start_x = (self.WIDTH - total_width) // 2
            y = self.HEIGHT // 2 - self.CARD_HEIGHT // 2
            for i, card in enumerate(community_cards):
                pos = (start_x + i * (self.CARD_WIDTH + 20), y)
                self.draw_card(str(card), pos)

        # Draw player's cards at the bottom
        player_cards = game_state['player_cards']
        n = len(player_cards)
        total_width = self.CARD_WIDTH * n + 20 * (n - 1)
        start_x = (self.WIDTH - total_width) // 2
        y = self.HEIGHT - self.CARD_HEIGHT - 50
        for i, card in enumerate(player_cards):
            pos = (start_x + i * (self.CARD_WIDTH + 20), y)
            self.draw_card(str(card), pos)
                
        # drawing left opponent cards
        left_cards = game_state['left_opp_cards']
        if isinstance(left_cards, list) is False:
            left_cards = left_cards[0]
        n_left = len(left_cards)
        total_height = self.CARD_HEIGHT * n_left + 20 * (n_left - 1)
        x = 50  # Left margin
        start_y = (self.HEIGHT - total_height) // 2
        for i, card in enumerate(left_cards):
            pos = (x, start_y + i * (self.CARD_HEIGHT + 20))
            if isinstance(card, Card):
                self.draw_card(str(card), pos)
                
            else:
                self.draw_card("XX", pos)
            
            
        # drawing top opponent cards
        top_cards = game_state['top_opp_cards']
        if isinstance(top_cards, list) is False:
            top_cards = top_cards[0]
        n_top = len(top_cards)
        total_width = self.CARD_WIDTH * n_top + 20 * (n_top - 1)
        start_x = (self.WIDTH - total_width) // 2
        y = 50 
        for i, card in enumerate(top_cards):
            pos = (start_x + i * (self.CARD_HEIGHT + 20), y)
            if isinstance(card, Card):
                self.draw_card(str(card), pos)
            else:
                self.draw_card("XX", pos)
        
            
        # drawing right opponent cards
        right_cards = game_state['right_opp_cards']
        if isinstance(right_cards, list) is False:
            left_cards = left_cards[0]
        n_right = len(right_cards)
        total_height = self.CARD_HEIGHT * n_right + 20 * (n_right - 1)
        x = self.WIDTH - self.CARD_WIDTH - 50  # Right margin
        start_y = (self.HEIGHT - total_height) // 2
        for i, card in enumerate(right_cards):
            pos = (x, start_y + i * (self.CARD_HEIGHT + 20))
            if isinstance(card, Card):
                self.draw_card(str(card), pos)
            else:
                self.draw_card("XX", pos)
        
    
        # Giving pot amount
        pot = game_state['pot']
        pot_text = self.font.render(f"Pot: ${pot}", True, self.WHITE)
        self.screen.blit(pot_text, (self.WIDTH // 2 - pot_text.get_width() // 2,
                                    self.HEIGHT // 2 + self.CARD_HEIGHT // 2 + 20))
        
        # Giving player bank
        bank = game_state['player_bank']
        pot_text = self.font.render(f"Bank: ${bank}", True, self.WHITE)
        self.screen.blit(pot_text, (self.WIDTH // 2 - pot_text.get_width() // 2,
                                    self.HEIGHT // 2 + self.CARD_HEIGHT // 2 + 60))
        
        
        if 'winner_str' in game_state:  
            y = 400  # Starting vertical position for text
            for line in game_state['winner_str'].splitlines():
                text_surface = self.font.render(line, True, (255, 255, 255))
                self.screen.blit(text_surface, (50, y))
                y += text_surface.get_height() + 5
            
        

    def run(self, game_state:dict):
        """
        Method to populate the display and update when called

        Args:
            game_state (dict): game state dict to populate
        """

        # Retrieve the current game state from your backend
        self.render_game_state(game_state)
        pygame.display.flip()
        

        
    
    

