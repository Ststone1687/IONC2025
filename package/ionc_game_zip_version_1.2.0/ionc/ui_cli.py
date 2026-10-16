
class CLI:
    def msg(self,s): print(s)
    def display_hand(self,hand):
        print("手牌:")
        for i,c in enumerate(hand):
            print(f" [{i}] {c}")
    def display_status(self,prob,turn):
        print(f"Turn : {turn}/{prob.turn_limit}")
        print(f"Time {prob.time}/{prob.time_limit} | Memory {prob.memory}/{prob.memory_limit} | Correct {prob.correct}/{prob.perfect}")
    def ask_idx(self,size):
        while True:
            ans=input("出牌索引(-1 跳過本回合/-10 跳過本題): ")
            if ans.lstrip('-').isdigit():
                v=int(ans)
                if v==-1 or v==-10 or 0<=v<size:
                    return v
            print("無效")
