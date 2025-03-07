"""
This file defines a sub-class to the player class that will be used by HumanPlayers 
"""

from .player import Player

class HumanPlayer(Player):
    """
    A subclass of player that adds functionality for user input. 
    """
    def get_action(self, bet_min:int, call_amt:int)-> int:
        """
        Method to get user input for action.

        Args:
            bet_min (int): minimum bet amount to pass to user for decision making
            call_amt (int): call amount to pass to user for decision making

        Returns:
            int: player decision amount
        """
        action_flag = True
        while action_flag: 
            # getting action
            print(f'The current bet minimum is {str(bet_min)} and call amount is {str(call_amt)}.')
            print('What would you like to do?: [b]et, [c]heck/call, [f]old')
            action = input("Action: ")
            action = self._clean_input(action)
            # if not valid action
            if action not in ['bet', 'check', 'fold', 'b', 'c', 'f']:
                print('Please pass a valid action')
                continue
            else:
                amt_flag = True
                # if bet action, ask user how much
                if (action == 'bet') or (action == 'b'):
                    print('How much would you like to bet? Please enter an integer or [b]ack to change command.')
                    while amt_flag:
                        amt = input("$ Amount: ")
                        amt = self._clean_input(amt)
                        # if player chose to go back, return to top, else validate amount
                        if (amt != 'b') and (amt != 'back'):
                            try:
                                int_amt = int(amt)
                            except:
                                print('Please enter a valid integer for how much you would like to bet.')
                                continue
                            # checking to make sure player has enough money in back
                            if int_amt > self.bank:
                                print(f'That bet is larger than your bank, you currently have a bank of ${str(self.bank)}')
                                continue
                            elif int_amt < bet_min:
                                print(f'That bet is less than the minimum bet amount, the current minimum bet is ${bet_min}')
                                continue
                            else:
                                self.action_str = 'bet'
                                return int_amt
                        else:
                            amt_flag = False
                        
                # if not betting, write action
                if (action == 'c') or (action == 'check'):
                    self.action_str = 'check'
                    return call_amt
                                        
                else:
                    self.action_str = 'fold'
                    return 0
        

                        
                    
    @staticmethod
    def _clean_input(action_str:str) -> str:
        """
        Helper method to clean user input

        Args:
            action_str (str): action str to clean 

        Returns:
            str: cleaned action str
        """
        return action_str.strip().lower()
