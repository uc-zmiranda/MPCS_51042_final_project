import pygame
import sys


class TexasHoldemDisplay:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.WIDTH, self.HEIGHT = width, height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Texas Hold'em")
        font_name = pygame.font.match_font("dejavusans")  # or "Arial Unicode MS"
        self.font = pygame.font.Font(font_name, 24)
        self.clock = pygame.time.Clock()
        # Colors and card dimensions
        self.GREEN = (0, 128, 0)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.CARD_WIDTH, self.CARD_HEIGHT = 60, 90
        

    def draw_table(self):
        # Fill background with table color
        self.screen.fill(self.GREEN)

    def draw_card(self, card_text, pos):
        """Draw a card at the given position with card_text (or "XX" for face-down cards)."""
        card_rect = pygame.Rect(pos[0], pos[1], self.CARD_WIDTH, self.CARD_HEIGHT)
        pygame.draw.rect(self.screen, self.WHITE, card_rect)
        pygame.draw.rect(self.screen, self.BLACK, card_rect, 2)
        if ('\u2666' in card_text) or  ("\u2665" in card_text):
            text_surface = self.font.render(card_text, True, self.RED)
        else:
            text_surface = self.font.render(card_text, True, self.BLACK)

        text_rect = text_surface.get_rect(center=card_rect.center)
        self.screen.blit(text_surface, text_rect)

    def render_game_state(self, game_state):
        """
        Render the current game state.
        Expected game_state dictionary keys:
          - 'player_cards': list of strings (e.g., ['A♠', 'K♣'])
          - 'opponent_cards': list of strings or None for face-down cards
          - 'community_cards': list of strings (e.g., ['10♦', 'J♥', 'Q♠'])
          - 'pot': integer or float representing the pot amount
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
        if n:
            total_width = self.CARD_WIDTH * n + 20 * (n - 1)
            start_x = (self.WIDTH - total_width) // 2
            y = self.HEIGHT - self.CARD_HEIGHT - 50
            for i, card in enumerate(player_cards.cards):
                pos = (start_x + i * (self.CARD_WIDTH + 20), y)
                self.draw_card(str(card), pos)


        # Optionally, draw additional game info (e.g., pot)
        pot = game_state['pot']
        pot_text = self.font.render(f"Pot: ${pot}", True, self.WHITE)
        self.screen.blit(pot_text, (self.WIDTH // 2 - pot_text.get_width() // 2,
                                    self.HEIGHT // 2 + self.CARD_HEIGHT // 2 + 20))
        
        
        if 'winner_str' in game_state:  
            y = 400  # Starting vertical position for text
            for line in game_state['winner_str'].splitlines():
                text_surface = self.font.render(line, True, (255, 255, 255))
                self.screen.blit(text_surface, (50, y))
                y += text_surface.get_height() + 5
            
        

    def run(self, game_state:dict, run:bool):
        """
        Main loop: get_game_state_func should be a function that returns the current game state.
        """
        
        # Retrieve the current game state from your backend
        self.render_game_state(game_state)
        pygame.display.flip()
        
        
        # pygame.quit()
        # sys.exit()
        
        
    
    

