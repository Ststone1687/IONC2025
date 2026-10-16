
import json, random, pathlib, operator
from typing import List, Dict, Any
from ionc.paths import asset_dir

from ionc.card import Card
from ionc.problem import Problem
from ionc.engine import BattleEngine

CMP_OPS = {
    "eq": operator.eq,
    "ne": operator.ne,
    "gt": operator.gt,
    "gte": operator.ge,
    "lt": operator.lt,
    "lte": operator.le,
}

class StoryRunner:
    """Main story engine. It now supports:
       * flag assignment (set) and arithmetic (add)
       * branch blocks that choose the next id based on flag conditions
       * scene blocks can reference an external txt file through `lines_file`
       * battle blocks can record a numeric score to a flag and use score‑based branches
    """

    def __init__(self, assets: pathlib.Path, player, ui):
        self.assets = assets
        # Load narrative data
        self.blocks: Dict[str, Dict[str, Any]] = {b["id"]: b for b in json.load(open(assets / "story_blocks.json", encoding="utf-8"))}
        # Cards / problems
        self.cards_db = {c["id"]: c for c in json.load(open(assets / "cards.json", encoding="utf-8"))}
        self.probsets = json.load(open(assets / "problems.json", encoding="utf-8"))
        self.player = player
        self.ui = ui

    # --------------------------------------------------------------------- #
    # Helpers
    # --------------------------------------------------------------------- #
    def _resolve_lines(self, blk: Dict[str, Any]) -> List[str]:
        """Return the list of dialogue lines for a scene.
        If `lines_file` is present, read that file (UTF‑8) under assets/lines/.
        """
        if "lines" in blk:
            return blk["lines"]
        if "lines_file" in blk:
            txt_path = self.assets / "lines" / blk["lines_file"]
            with open(txt_path, "r", encoding="utf-8") as fp:
                return [ln.rstrip("\n") for ln in fp]
        return []

    def _apply(self, eff: Dict[str, Any]) -> None:
        """Apply the effect dict to the player (flags, cards, etc.)."""
        # ---- flags ----
        if "flags" in eff:
            for k, v in eff["flags"].items():
                # Support structured {"set": x} / {"add": y} format
                if isinstance(v, dict):
                    if "set" in v:
                        self.player.flags[k] = v["set"]
                    if "add" in v:
                        self.player.flags[k] = self.player.flags.get(k, 0) + v["add"]
                    if "sub" in v:
                        self.player.flags[k] = self.player.flags.get(k, 0) - v["sub"]
                else:
                    # Original behaviour (+= v)
                    self.player.flags[k] = self.player.flags.get(k, 0) + v

        # ---- cards ----
        if "give_cards" in eff:
            for cid in eff["give_cards"]:
                self.player.add_card(Card(self.cards_db[cid]))
                self._announce_card(cid)
        if "give_random" in eff:
            cid = random.choice(eff["give_random"])
            self.player.add_card(Card(self.cards_db[cid]))
            self._announce_card(cid)

    def _announce_card(self, cid: str) -> None:
        self.ui.msg("獎勵".center(23, "="))
        self.ui.msg(f"獲得卡片：{self.cards_db[cid]['name']}")
        self.ui.msg(f"卡片描述：{self.cards_db[cid]['description']}")
        stats = self.cards_db[cid]
        self.ui.msg(f"卡片數值：\ntime:{stats['time']}  mem:{stats['memory']}  correct:{stats['correct']}")
        self.ui.msg("".center(23, "="))

    # --------------------------------------------------------------------- #
    # Block handlers
    # --------------------------------------------------------------------- #
    def start(self, start="story01"):
        nid = start
        while nid:
            blk = self.blocks[nid]
            t = blk["type"]
            if t == "scene":
                nid = self._scene(blk)
            elif t == "choice":
                nid = self._choice(blk)
            elif t == "battle":
                nid = self._battle(blk)
            elif t == "branch":
                nid = self._branch(blk)
            else:
                self.ui.msg(f"[WARN] Unknown block type: {t}")
                nid = None

    # ---------------------- scene ---------------------- #
    def _scene(self, blk: Dict[str, Any]) -> str:
        # ---- 妹妹線特殊卡片 ----
        if blk["id"] == "story78": # 進入 story78 立即檢查
            has_daisuki = any(c.id == "imoto_daisuki" for c in self.player.draw_pile)
            love_cnt = sum(1 for c in self.player.draw_pile if c.id == "imoto_love")
            if love_cnt >= 3 and not has_daisuki:
                self.ui.msg("💖 你因為持有 3 張 [妹妹 Love]，獲得了卡片[超級妹控]！")
                self.player.add_card(Card(self.cards_db["imoto_daisuki"]))
        for line in self._resolve_lines(blk):
            self.ui.msg(line)
            input()
        self._apply(blk.get("effects", {}))
        return blk.get("next")

    # ---------------------- choice --------------------- #
    def _choice(self, blk: Dict[str, Any]) -> str:
        self.ui.msg(blk["question"])
        for i, opt in enumerate(blk["options"]):
            self.ui.msg(f"  {i}. {opt['text']}")
        try:
            s = int(input("輸入選項編號>> "))
        except Exception:
            self.ui.msg("無效選擇，請輸入數字")
            return blk["id"]
        if not (0 <= s < len(blk["options"])):  # validate
            self.ui.msg("無效選擇，請重新輸入")
            return blk["id"]
        opt = blk["options"][s]
        self._apply(opt.get("effects", {}))
        return opt["next"]

    # ---------------------- battle --------------------- #
    def _battle(self, blk: Dict[str, Any]) -> str:
        pset = [Problem(pd, self.player.flags) for pd in self.probsets[blk["problem_set"]]]
        total_score = 0
        self.player.reset()
        for pb in pset:
            win_score = BattleEngine(self.player, pb, self.ui).run()
            # print(win_score)
            # print(pb.reward)
            # Basic scoring: AC gives 100, otherwise give subtask score
            gained = win_score
            total_score += gained
            if win_score == 100 and pb.reward:
                self._apply(pb.reward)
            # print(total_score)

        # Optionally write score into a flag
        score_flag = blk.get("score_flag", "last_score")
        self.player.flags[score_flag] = total_score

        # Handle score based branching
        if "score_branches" in blk:
            for br in blk["score_branches"]:
                cond_min = br.get("min", -float("inf"))
                cond_max = br.get("max", float("inf"))
                if cond_min <= total_score <= cond_max:
                    return br["next"]

        return blk.get("next")

    # ---------------------- branch --------------------- #
    def _branch(self, blk: Dict[str, Any]) -> str:
        """Evaluate a list of conditional branches and return the first match."""
        for br in blk["branches"]:
            cond: Dict[str, Dict[str, Any]] = br["condition"]
            if self._evaluate_condition(cond):
                return br["next"]
        # fallback
        self._apply(blk.get("effects", {}))
        return blk.get("default_next")

    # --------------------------------------------------------------------- #
    # Condition evaluation
    # --------------------------------------------------------------------- #
    def _evaluate_condition(self, cond: Dict[str, Dict[str, Any]]) -> bool:
        """Return True if *all* flag comparisons pass."""
        for flag, cmp_dict in cond.items():
            cur = self.player.flags.get(flag, 0)
            for op, rhs in cmp_dict.items():
                if op not in CMP_OPS:
                    continue
                if not CMP_OPS[op](cur, rhs):
                    return False
        return True
