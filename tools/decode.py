#!/usr/bin/env python3
"""
decode_savecode.py ── IONC 存檔碼解析工具

用法：
  python decode_savecode.py            # 互動輸入，一行一組，空行結束
  python decode_savecode.py <code1> <code2> ...   # 直接傳參數

依賴：
  - ionc.savecode (專案原本就有的 encode / decode)
"""

import sys
import json
from pprint import pprint
from savecode import decode


def dump(data: dict) -> None:
    """將解碼後的資料印成易讀格式。"""
    # print("=== 基本資料 ===")
    # print(f"  周目      : {data.get('loop',  '?')}")
    # print(f"  日期      : {data.get('date',  '?')}")
    print("\n=== Flags ===")
    for k, v in data.get("flags", {}).items():
        print(f"  {k}: {v}")
    print("\n=== 繼承卡片 ===")
    for cid in data.get("inherit_cards", []):
        print(f"  - {cid}")

    other = {k: v for k, v in data.items()
             if k not in {"loop", "date", "flags", "inherit_cards"}}
    if other:
        print("\n=== 其他欄位 ===")
        pprint(other)
    print()  # 分隔空行


def collect_codes() -> list[str]:
    """互動式讀取多行存檔碼，空行或 EOF 結束。"""
    codes = []
    try:
        while True:
            line = input("存檔碼（空行結束）：").strip()
            if not line:
                break
            codes.append(line)
    except EOFError:  # 支援管線或 Ctrl-D
        pass
    return codes


def main() -> None:
    # 1) CLI 參數優先；2) 否則走互動輸入
    codes = sys.argv[1:] or collect_codes()
    if not codes:
        print("未提供任何存檔碼。")
        return

    for idx, code in enumerate(codes, start=1):
        # print(f"\n===== Code #{idx} =====")
        try:
            payload = decode(code)
            dump(payload)
        except Exception as e:
            print(f"❌ 無法解析：{e}")


if __name__ == "__main__":
    main()

'''

s58W09S3xgkbxwzsYqoKVIKi5Xe5MamPs08c_Uh__ox4nFWOwQrDIAyG3yVnD3W9-SpjSBrjGlaVqTuU0ndfGAjdMd_3wZ8D4obPBu6ALon9gk0I3GQgcSp1vwAqtTL1C5FUegE3Gwi4W9-0YHB2UhWrcA7D3f4crUIvznoZ6IzJj9j-4nnEmir2C_v3B3V70-LU1bxyle4Ja9DH7xBig8f5BU8aQoQ=

4ShbKHPcQbBWD97XWXkB4gjDP51VEFCO5Px4rAxIbAJ4nE2OMQ7DIAxF7-KZoaTtwlWqyqLgtEgBIuwOKMrda6EObNZ_71v_gHXzbwZ3gKRM-PKcAriLgUy5tj4FobZGQaYk5SoV3N1A9N0iq0EDrC1RieCWQZaJ8N7BWQNCPuO_b4d1nSypaSMZp5LbRPQtFkL-6mR76oTyoZYEg29RowdwZYw7PM8fqp1H4g==

7SdvqLNmwMnWwvTQjiZ134Ul1WaBzpK-dNmLG8IvCTp4nE2PwQrDIAyG3yXnHmbHLr7KGGI1XYNVIeZSSt-9QcbwFv4v_0dywrr7bwN7glBGt_hGAexjgoy58jEEoTJjkCGhXKWCfU0Q_WFc0w3sYGXCEsHOncwDiUwlgTWq2ygkLH0W9Nn9bKZ3nkNHKu0onajVLegOn0gqk-JLzygbMokLnqN-8oY__lw3acVKcA==

n_pKVgd7d8YjK6XD-cNBlvJ_nHhF3DJTVowQD2YQf6V4nFWP0QqDMAxF_yXPPqgTBv2VMUrXxhlmW0izgYj_vsxtom_h3nPgZoZ-dPcCZgahiPbmCnkwdQURY-ZpF_jMjF52ifATLaZgfRIw5wqCmxpbFEQwTa0ExSwZTFdBz6QkmHal2gMVmNJDb6WoDOsh6KL92c2qnA6KZBpR_l23da12n0UJN3vRGWlAJrHecdBfL99ddswvhOvyBj0AVQY=
'''