
import random
class Player:
    def __init__(self,deck,flags):
        self.draw_pile=list(deck)
        random.shuffle(self.draw_pile)
        self.hand=[]
        self.discard=[]
        self.flags=flags
        self.mountain = []
    def reset(self):
        self.hand=[]
        self.discard=[]
        random.shuffle(self.draw_pile)
        self.mountain = list(self.draw_pile)
        self.draw(5)  # Draw initial hand of 5 cards
    def draw(self,n=1):
        for _ in range(n):
            if not self.mountain:
                break
            self.hand.append(self.mountain.pop())
    def play_card(self,idx):
        return self.hand.pop(idx)
    def add_card(self,card):
        self.draw_pile.append(card)
