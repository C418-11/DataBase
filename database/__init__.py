# -*- coding: utf-8 -*-
__author__ = "C418____11 <553515788@qq.com>"
__version__ = "BT 0.0.0.2f"

# 版本名称规则
# R 正式版
# B | A 测试版
# T 临时版
# 版本最后面英文字母小写表小版本 a~z

"""

DataBase Lib

"""


import sys

__RUN_VERSION = 3.10
if float(sys.winver) < __RUN_VERSION:
    raise ImportError("Python version Error (at lease {0} now {1})".format(__RUN_VERSION, sys.winver))

print(f"DataBase {__version__}")

__all__ = ["DataBase", "Event"]


if __name__ == '__main__':
    pass