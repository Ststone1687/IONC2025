
class Problem:
    def __init__(self,data,start_flags):
        self.id=data['id']; self.name=data['name']; self.desc=data.get('desc','')
        self.time_limit=data['time_limit']
        self.memory_limit=data['memory_limit']
        self.perfect=data.get('perfect',0)
        self.turn_limit = data.get('turn_limit', 50)
        self.partial=data.get('partial',[])
        self.reward=data.get('reward_on_ac',{})
        self.score=data.get('score',0)
        self.reset(start_flags)
    def reset(self,start_flags):
        self.time=start_flags['time_basic']
        self.memory=start_flags['memory_basic']
        self.correct=start_flags['correct_basic']
    def apply(self,card):
        self.time+=card.time; self.memory+=card.memory; self.correct+=card.correct
    def is_ac(self):
        return self.correct>=self.perfect and self.time<=self.time_limit and self.memory<=self.memory_limit
