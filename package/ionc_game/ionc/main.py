import json, pathlib
from ionc.card import Card
from ionc.player import Player
from ionc.story import StoryRunner
from ionc.ui_cli import CLI
from ionc.savecode import encode, decode
from ionc.const import LIMITED_CARDS
from ionc.paths import asset_dir
import os

PROJECT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = asset_dir()

def _canonical(code: str) -> str:
    """驗簽後回傳唯一表示（same payload → same string）。"""
    return encode(decode(code))

def load(name: str):
    path = ASSETS / name
    return json.load(open(path, encoding="utf-8"))
def ask_save_codes(ui):
    codes, seen = [], set()
    while len(codes) < 3:
        raw = input(f"\033[31m輸入第 {len(codes)+1} 組存檔碼（-1 跳過）：\033[0m").strip()
        if raw in {"", "-1"}:
            break
        try:
            canon = _canonical(raw)       # ① 驗證並正規化
            if canon in seen:             # ② 用唯一表示判重
                ui.msg("⚠️  這個存檔碼已輸入過，請重新輸入。",31)
                continue
            codes.append(canon)
            seen.add(canon)
        except Exception as e:
            ui.msg(f"⚠️  存檔碼無效（{e}），請重新輸入或輸入 -1 跳過。",31)
    return codes
def build_player(codes):
    cards_db={c['id']:c for c in load('cards.json')}
    deck=[]
    flags=load('config.json')['basic_flags'].copy()
    for code in codes:
        try:
            data=decode(code)
            # flags.update(data['flags'])
            for cid in data['inherit_cards']:
                if cid in cards_db:
                    deck.append(Card(cards_db[cid]))
        except Exception as e:
            print('存檔碼無效:',e)
    for limit_cid, limit in LIMITED_CARDS.items():
        cnt = sum(1 for c in deck if c.id == limit_cid)
        if cnt > limit:
            ui.msg(f"⚠️  卡片 {limit_cid} 超出上限（{cnt}/{limit}），已自動裁切至上限。",31)
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
        ui.msg("選擇一張繼承卡片（輸入索引）：",36)
        for i, c in enumerate(deck):
            ui.msg(f" {i}. {c}")
        try:
            idx = int(input("> "))
            if idx < 0 or idx >= len(deck):
                raise ValueError
            pick = deck[idx]
            # # 檢查限量
            # current_counter = Counter([c.id for c in all_cards])
            # if current_counter[pick.id] >= LIMITED_CARDS.get(pick.id, 99):
            #     ui.msg(f"⚠️  {pick.id} 已達上限，請選擇其他卡。")
            #     continue
            return pick.id
        except ValueError:
            ui.msg("無效輸入，請重新輸入索引。",31)
def main():
    broken = False
    try:
        with open("./secret.txt", "r") as f:
            secret = f.read().strip()
        if secret != "ok":
            broken = True
    except:
        f = open("./secret.txt", "w")
        secret = "ok"
        f.write(secret)
        f.close()
        filename = "./secret.txt"
        os.system(f'attrib +h "{filename}"')
    ui=CLI()
    if broken:
        ui.msg("⚠️  ？？？？？。",31)
        ui.msg("⚠️  你為什麼又回來了？",31)
        ui.msg("⚠️  檔案已經被我刪除了。",31)
        ui.msg("⚠️  你已經無法逃跑了。",31)
        while True:
            x = input()
            ui.msg("⚠️  你已經無法逃跑了。",31)
        return
    codes = ask_save_codes(ui)
    player=build_player(codes)
    StoryRunner(ASSETS,player,ui).start()
    inherit=pick_inherit(player,ui)
    payload={'flags':player.flags,'inherit_cards':[inherit]}
    for i in player.flags:
        if("end_extra_dead_end" in i or "end_extra_true_end" in i):
            filename = "./secret.txt"
            os.system(f'attrib -h "{filename}"')
            os.remove(filename)
            f = open("./secret.txt", "w")
            secret = "broken"
            f.write(secret)
            f.close()
            os.system(f'attrib +h "{filename}"')
    code=encode(payload)
    ui.msg("=== 你的存檔碼 ===",33)
    ui.msg(code,33)
    ui.msg("輸入 -1 退出遊戲。",31)
    end_game = input()
    while end_game != "-1":
        ui.msg("輸入 -1 退出遊戲。",31)
        end_game = input()
if __name__=='__main__':
    main()
