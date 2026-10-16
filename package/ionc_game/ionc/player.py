
import random
class Player:
    def __init__(self,deck,flags):
        self.draw_pile=list(deck)
        random.shuffle(self.draw_pile)
        self.hand = []
        self.discard = []
        self.removed = []
        self.flags=flags
        self.mountain = []
    def reset(self):
        self.hand=[]
        self.discard=[]
        self.now_mountain=[]
        self.removed = []
        random.shuffle(self.draw_pile)
        self.mountain = list(self.draw_pile)
        self.draw()
    def draw(self,n=3):
        for _ in range(n):
            if len(self.mountain) == 0 and len(self.discard) > 0:
                self.mountain = list(self.discard)
                self.discard = []
                random.shuffle(self.mountain)
            self.hand.append(self.mountain.pop())
    def next_turn(self):
        for i in self.hand:
            self.discard.append(i)
        self.hand = []
        self.draw()
    def play_card(self,idx):
        card = self.hand[idx]
        if card.one_use:
            self.removed.append(card)
            self.hand.pop(idx)
        else:
            self.discard.append(card)
            self.hand.pop(idx)
        self.next_turn()
        return card
    def add_card(self,card):
        self.draw_pile.append(card)
