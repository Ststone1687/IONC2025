#!/usr/bin/env python3
"""
helper_obfuscate_key.py ── 產生 _PERM / _SALT / _OBF

步驟：
  1. 修改 PLAINTEXT_KEY（bytes）
  2. python helper_obfuscate_key.py
  3. 將輸出結果貼到 savecode.py，覆蓋原有常數
"""

import os
import random
import textwrap

# --- 1) 設定明文祕鑰 -------------------------------------------------
PLAINTEXT_KEY = b"ionc2025_imoto_daisuki_by_Ststone_copy_right"  # ← 換成自己的 bytes
# ---------------------------------------------------------------------

L = len(PLAINTEXT_KEY)
random.seed(os.urandom(16))        # 真隨機
perm = list(range(L))
random.shuffle(perm)
salt = [random.randint(0, 255) for _ in range(L)]
obf  = [PLAINTEXT_KEY[p] ^ salt[i] for i, p in enumerate(perm)]

def fmt(name, arr):
    body = ", ".join(map(str, arr))
    body = textwrap.fill(body, width=78)
    return f"{name}: List[int] = [\n    {body}\n]"

print("# ───── 下面貼進 savecode.py ─────\n")
print(fmt("_PERM", perm), "\n")
print(fmt("_SALT", salt), "\n")
print(fmt("_OBF",  obf),  "\n")
print("# ──────────────────────────────")
