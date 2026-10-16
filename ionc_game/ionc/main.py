import json, pathlib
from ionc.card import Card
from ionc.player import Player
from ionc.story import StoryRunner
from ionc.ui_cli import CLI
from ionc.savecode import encode, decode
from ionc.const import LIMITED_CARDS

PROJECT = pathlib.Path(__file__).resolve().parent.parent
ASSETS  = PROJECT / "assets"
def load(name: str):
    return json.load(open(ASSETS / name, encoding="utf-8"))
def ask_save_codes(ui):
    codes = []
    while len(codes) < 3:
        line = input(f"輸入第 {len(codes)+1} 組存檔碼（-1 跳過）：").strip()
        if line == "-1" or line == "":
            break
        if line in codes:
            ui.msg("⚠️  這個存檔碼已輸入過，請重新輸入。")
            continue
        try:
            decode(line)          # 先驗證
            codes.append(line)
        except Exception as e:
            ui.msg(f"⚠️  存檔碼無效（{e}），請重新輸入或輸入 -1 跳過。")
    return codes
def build_player(codes):
    cards_db={c['id']:c for c in load('cards.json')}
    deck=[]
    flags=load('config.json')['basic_flags'].copy()
    for code in codes:
        try:
            data=decode(code)
            flags.update(data['flags'])
            for cid in data['inherit_cards']:
                if cid in cards_db:
                    deck.append(Card(cards_db[cid]))
        except Exception as e:
            print('存檔碼無效:',e)
    for limit_cid, limit in LIMITED_CARDS.items():
        cnt = sum(1 for c in deck if c.id == limit_cid)
        if cnt > limit:
            ui.msg(f"⚠️  卡片 {limit_cid} 超出上限（{cnt}/{limit}），已自動裁切至上限。")
            # 保留前 limit 張
            deck = [c for c in deck if c.id != limit_cid] + [Card(cards_db[limit_cid])]*limit
    deck += [Card(cards_db[c]) for c in load('config.json')['initial_deck']]
    return Player(deck,flags)
def pick_inherit(player, ui):
    from collections import Counter
    all_cards = player.draw_pile + player.hand + player.discard
    unique = {c.id: c for c in all_cards}
    deck   = list(unique.values())

    while True:
        ui.msg("選擇一張要帶到下一周目的卡（輸入索引）：")
        for i, c in enumerate(deck):
            ui.msg(f" {i}. {c}")
        try:
            idx = int(input("> "))
            if idx < 0 or idx >= len(deck):
                raise ValueError
            pick = deck[idx]
            # 檢查限量
            current_counter = Counter([c.id for c in all_cards])
            if current_counter[pick.id] >= LIMITED_CARDS.get(pick.id, 99):
                ui.msg(f"⚠️  {pick.id} 已達上限，請選擇其他卡。")
                continue
            return pick.id
        except ValueError:
            ui.msg("無效輸入，請重新輸入索引。")
def main():
    ui=CLI()
    codes = ask_save_codes(ui)
    player=build_player(codes)
    StoryRunner(ASSETS,player,ui).start()
    inherit=pick_inherit(player,ui)
    payload={'flags':player.flags,'inherit_cards':[inherit]}
    code=encode(payload)
    ui.msg("=== 你的存檔碼 ===")
    ui.msg(code)
if __name__=='__main__':
    main()
