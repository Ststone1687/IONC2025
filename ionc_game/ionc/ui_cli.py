
class CLI:
    def msg(self,s): print(s)
    def display_hand(self,hand):
        print("手牌:")
        for i,c in enumerate(hand):
            print(f" [{i}] {c}")
    def display_status(self,prob,turn):
        print(f"Turn {turn} | Time {prob.time}/{prob.time_limit} Mem {prob.memory}/{prob.memory_limit} Corr {prob.correct}")
    def ask_idx(self,size):
        while True:
            ans=input("出牌索引(-1 跳過): ")
            if ans.lstrip('-').isdigit():
                v=int(ans)
                if v==-1 or 0<=v<size:
                    return v
            print("無效")
