#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文字RPG游戏 - 图形界面版本入口
"""
import tkinter as tk
from src.gui import GameGUI


def main():
    """主函数"""
    root = tk.Tk()
    game = GameGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
