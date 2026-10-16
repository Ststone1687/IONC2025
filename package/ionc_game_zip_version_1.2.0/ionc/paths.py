from pathlib import Path
import sys
import importlib.resources as pkg

def asset_dir() -> Path:
    """回傳打包 / 開發環境下都能用的 assets 目錄 Path。"""
    # ① 打包後（PyInstaller / Nuitka）
    if getattr(sys, "frozen", False):          # ← 這條件比檢查 _MEIPASS 更通用
        return Path(sys._MEIPASS) / "assets"   # 千萬別 .parent
    # ② 套件安裝 / 原始碼
    try:
        return Path(pkg.files(__package__).joinpath("assets"))
    except Exception:
        # 最終保險：回到 ionc/../assets
        return Path(__file__).resolve().parent.parent / "assets"
