"""
savecode.py  ——  IONC 模擬器  存檔碼 Encode / Decode（混淆加強版）

► Encode：dict  → savecode 字串（zlib + HMAC-SHA256 + Base64 URL-safe）
► Decode：savecode → dict（驗簽＋還原）

CLI 範例：
  python savecode.py encode payload.json
  python savecode.py decode <SAVE_CODE>

‼️  本檔已移除任何明文祕鑰，只留下多層混淆常數。
      若需更換祕鑰，請使用文末「helper_obfuscate_key.py」重新產生
      _PERM / _SALT / _OBF 後，覆蓋到本檔對應區塊即可。
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import sys
import zlib
from pathlib import Path
from typing import Any, Dict, List

# ────────────────────────────────────────────────────────────────────
#  ↓↓↓ 這三組常數由 helper_obfuscate_key.py 自動產生  ↓↓↓
#      若要更換祕鑰，請刪除下面區塊，跑一次 helper 後貼回。
# ────────────────────────────────────────────────────────────────────
# 祕鑰長度 len = 26 ；原始明文例如 b"ionc_super_secret_key_2025"
_PERM: List[int] = [
    32, 33, 42, 27, 6, 9, 1, 10, 18, 43, 39, 11, 28, 4, 12, 24, 38, 7, 35, 37, 0,
16, 22, 3, 15, 34, 25, 26, 19, 5, 8, 2, 13, 40, 17, 20, 29, 30, 23, 31, 21,
41, 14, 36
]

_SALT: List[int] = [
    168, 20, 40, 102, 131, 144, 42, 113, 50, 231, 249, 243, 196, 66, 134, 246,
252, 85, 255, 27, 16, 165, 229, 186, 28, 151, 210, 7, 8, 159, 9, 107, 69, 54,
62, 94, 12, 158, 31, 2, 95, 44, 21, 64
]

_OBF: List[int] = [
    205, 75, 64, 18, 177, 249, 69, 28, 65, 147, 139, 156, 183, 112, 242, 143, 163,
96, 144, 98, 121, 196, 186, 217, 120, 244, 141, 84, 125, 175, 86, 5, 42, 95,
87, 53, 120, 241, 125, 108, 54, 75, 74, 48
]  # 混淆後位元組：KEY[_PERM[i]] ^ _SALT[i]
# ────────────────────────────────────────────────────────────────────


def _get_secret() -> bytes:
    """將 _OBF / _SALT / _PERM 逆運算 → 還原原始 key（bytes）。"""
    if not (_PERM and _SALT and _OBF):
        raise RuntimeError("祕鑰資料缺失")
    if not (len(_PERM) == len(_SALT) == len(_OBF)):
        raise RuntimeError("祕鑰長度不一致")

    # 1) 先 XOR 還原出『亂序後』位元組
    tmp = [o ^ s for o, s in zip(_OBF, _SALT)]

    # 2) 依 _PERM 將位元組放回正確位置
    key_bytes = [0] * len(tmp)
    for i, p in enumerate(_PERM):
        key_bytes[p] = tmp[i]

    return bytes(key_bytes)


# ────────────────────────────────────────────────────────────────────
# Encode / Decode
# ────────────────────────────────────────────────────────────────────
def encode(payload: Dict[str, Any]) -> str:
    """dict → savecode  (zlib→HMAC→Base64)"""
    raw: bytes = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode()
    comp = zlib.compress(raw)
    sig = hmac.new(_get_secret(), comp, hashlib.sha256).digest()  # 32 bytes
    blob = sig + comp                                             # [sig||data]
    return base64.urlsafe_b64encode(blob).decode()


def decode(code: str) -> Dict[str, Any]:
    """savecode → dict（簽章不符時拋 ValueError）"""
    try:
        blob = base64.urlsafe_b64decode(code)
    except Exception as e:
        raise ValueError("base64 decode failed") from e

    if len(blob) <= 32:
        raise ValueError("blob too short")

    sig, comp = blob[:32], blob[32:]
    ref = hmac.new(_get_secret(), comp, hashlib.sha256).digest()
    if not hmac.compare_digest(sig, ref):
        raise ValueError("signature mismatch")

    try:
        raw = zlib.decompress(comp)
    except Exception as e:
        raise ValueError("zlib decompress failed") from e

    try:
        return json.loads(raw)
    except Exception as e:
        raise ValueError("json parse failed") from e


# ────────────────────────────────────────────────────────────────────
#  簡易 CLI：離線產生 / 解析
# ────────────────────────────────────────────────────────────────────
def _encode_cli(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    print(encode(data))


def _decode_cli(code: str) -> None:
    data = decode(code.strip())
    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in {"encode", "decode"}:
        print(
            "用法:\n  python savecode.py encode payload.json\n"
            "  python savecode.py decode <SAVE_CODE>",
            file=sys.stderr,
        )
        sys.exit(1)

    if sys.argv[1] == "encode":
        _encode_cli(Path(sys.argv[2]))
    else:  # decode
        _decode_cli(sys.argv[2])

