#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文字RPG游戏 - 命令行版本入口
"""
import sys
sys.path.insert(0, '.')

from game import Game


def main():
    """主函数"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
