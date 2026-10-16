
class BattleEngine:
    def __init__(self,player,problem,ui):
        self.p=player; self.prob=problem; self.ui=ui
    def run(self) -> int:
        self.ui.msg("")
        self.ui.msg("")
        self.ui.msg("")
        self.ui.msg(("題目 ： "+(self.prob.name)).center(23,'='),31)
        self.ui.msg(self.prob.desc,31)
        self.ui.msg("".center(23,'='),31)
        self.ui.msg("")
        self.ui.msg("AC條件".center(23,'='),32)
        self.ui.msg(f"Correct ≥ {self.prob.perfect}",32)
        self.ui.msg(f"Time ≤ {self.prob.time_limit}",32)
        self.ui.msg(f"Memory ≤ {self.prob.memory_limit}",32)
        self.ui.msg(f"Turns ≤ {self.prob.turn_limit}",32)
        self.ui.msg("".center(23,'='),32)
        self.ui.msg("")
        if self.prob.partial:
            self.ui.msg("Partial".center(23,'='),33)
            for sub in self.prob.partial:
                self.ui.msg(f" - {sub['name']}:",33)
                self.ui.msg(f"    Correct ≥ {sub['correct_req']}",33)
                self.ui.msg(f"    Time ≤ {sub['time_limit']}",33)
                self.ui.msg(f"    Memory ≤ {sub['memory_limit']}",33)
                self.ui.msg(f"    Score: {sub['score']}",33)
        self.ui.msg("".center(23,'='),33)
        self.ui.msg("")
        turn=1
        sub_accept = [0] * len(self.prob.partial)
        while True:
            self.ui.display_status(self.prob,turn)
            self.ui.display_hand(self.p.hand)
            idx=self.ui.ask_idx(len(self.p.hand))
            if idx!=-1 and idx!=-10:
                card = self.p.play_card(idx)
                self.prob.apply(card)
                self.p.next_turn()
                # self.p.discard.append(card)
                # self.p.draw(1)
            elif idx==-1:
                self.ui.msg("放棄本回合",31)
                self.ui.msg("跳過",31)
                self.p.next_turn()
            elif idx==-10:
                self.ui.msg("放棄本題",31)
                turn = self.prob.turn_limit + 1
                self.p.next_turn()
            if self.prob.is_ac() and self.prob.time <= self.prob.time_limit and self.prob.memory <= self.prob.memory_limit:
                self.ui.msg("".center(23,'='),32)
                self.ui.msg("AC!",32)
                self.ui.msg("".center(23,'='),32)
                return self.prob.score
            turn+=1
            now_score = 0
            for i,sub in enumerate(self.prob.partial):
                if self.prob.correct >= sub['correct_req'] and self.prob.time <= sub['time_limit'] and self.prob.memory <= sub['memory_limit']:
                    sub_accept[i] = True
            for i,sub in enumerate(self.prob.partial):
                if sub_accept[i] == True:
                    now_score += sub['score']
            if turn > self.prob.turn_limit:
                if self.prob.correct >= self.prob.perfect and self.prob.time > self.prob.time_limit:
                    self.ui.msg("".center(23,'='),36)
                    self.ui.msg("TLE：回合耗盡",36)
                    self.ui.msg("本題獲得分數：{}".format(now_score),36)
                    self.ui.msg("".center(23,'='),36)
                    return now_score
                elif self.prob.correct >= self.prob.perfect and self.prob.memory > self.prob.memory_limit:
                    self.ui.msg("".center(23,'='),33)
                    self.ui.msg("MLE：回合耗盡",33)
                    self.ui.msg("本題獲得分數：{}".format(now_score),33)
                    self.ui.msg("".center(23,'='),33)
                    return now_score
                else:
                    self.ui.msg("".center(23,'='),31)
                    self.ui.msg("WA：回合耗盡",31)
                    self.ui.msg("本題獲得分數：{}".format(now_score),31)
                    self.ui.msg("".center(23,'='),31)
                    return now_score
                self.ui.msg("")
