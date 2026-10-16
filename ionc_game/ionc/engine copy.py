
class BattleEngine:
    def __init__(self,player,problem,ui):
        self.p=player; self.prob=problem; self.ui=ui
    def run(self):
        self.ui.msg(self.prob.name.center(23,'='))
        self.ui.msg(self.prob.desc)
        self.ui.msg("AC條件".center(23,'='))
        self.ui.msg(f"Correct ≥ 100")
        self.ui.msg(f"Time ≤ {self.prob.time_limit}")
        self.ui.msg(f"Memory ≤ {self.prob.memory_limit}")
        self.ui.msg(f"Turns ≤ {self.prob.turn_limit}")
        if self.prob.partial:
            self.ui.msg("Partial".center(23,'='))
            for sub in self.prob.partial:
                self.ui.msg(f" - {sub['name']}:")
                self.ui.msg(f"    Correct ≥ {sub['correct_req']}")
                self.ui.msg(f"    Time ≤ {sub['time_limit']}")
                self.ui.msg(f"    Memory ≤ {sub['memory_limit']}")
        self.ui.msg("".center(23,'='))
        turn=1
        while True:
            self.ui.display_status(self.prob,turn)
            self.ui.display_hand(self.p.hand)
            idx=self.ui.ask_idx(len(self.p.hand))
            if idx!=-1:
                card=self.p.play_card(idx)
                self.prob.apply(card)
                self.p.discard.append(card)
                self.p.draw(1)
            else:
                self.ui.msg("跳過")
            if self.prob.is_ac() and self.prob.time <= self.prob.time_limit and self.prob.memory <= self.prob.memory_limit:
                self.ui.msg("AC!")
                return True
            elif self.prob.is_ac() and self.prob.time > self.prob.time_limit:
                self.ui.msg("TLE...")
            elif self.prob.is_ac() and self.prob.memory>self.prob.memory_limit:
                self.ui.msg("MLE...")
            turn+=1
            if turn > self.prob.turn_limit:
                if self.prob.is_ac() and self.prob.time > self.prob.time_limit:
                    self.ui.msg("TLE：回合耗盡")
                    return False
                elif self.prob.is_ac() and self.prob.memory>self.prob.memory_limit:
                    self.ui.msg("MLE：回合耗盡")
                    return False
                else:
                    self.ui.msg("WA：回合耗盡")
                    return False
            self.ui.msg("".center(23,'='))
