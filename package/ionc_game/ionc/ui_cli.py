
class CLI:
    def msg(self,s,color=None):
        if color:
            print(f"\033[{color}m{s}\033[0m")
        else:
            print(s)
    def display_hand(self,hand):
        print("")
        print("\033[35m手牌:\033[0m")
        for i,c in enumerate(hand):
            print(f"\033[35m [{i}] {c}\033[0m")
    def display_status(self,prob,turn):
        print(f"\033[36mTurn : {turn}/{prob.turn_limit}\033[0m")
        print(f"\033[36mTime {prob.time}/{prob.time_limit} | Memory {prob.memory}/{prob.memory_limit} | Correct {prob.correct}/{prob.perfect}\033[0m")
    def ask_idx(self,size):
        while True:
            ans=input(f"\033[33m出牌索引(-1 跳過本回合/-10 跳過本題): \033[0m")
            if ans.lstrip('-').isdigit():
                v=int(ans)
                if v==-1 or v==-10 or 0<=v<size:
                    return v
            print(f"\033[31m無效\033[0m")
