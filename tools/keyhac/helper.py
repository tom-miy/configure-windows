import sys
import os
import datetime
import fnmatch
import pyauto
from keyhac import *


## キーの1回/2回押しで引数の関数コールを切り替える
#
#  @param func      コールする関数
#
#  引数の func は1回押しなら func(True)、2回連続押しなら func(False)
#  でコールされる
#
def double_key(func, cache_t={}):

    # 2回連続押し判断の許容間隔(ミリ秒)
    TIMEOUT_MSEC = 500

    func_name = func.__name__

    # 前回時刻
    t0 = 0
    if func_name in cache_t:
        t0 = cache_t[func_name]
    # 現在時刻を保存
    import time
    cache_t[func_name] =  time.perf_counter()
    # 前回実行からの経過時間(ミリ秒)
    delta_t = (cache_t[func_name] - t0) * 1000

    # 関数コール
    if delta_t > TIMEOUT_MSEC:
        func(False)     # 1回押し
    else:
        func(True)      # 2回連続押し


# 相対パスを絶対パスに変換する
def resolve_path(rel, root=None):
    if not root:
        root = os.environ.get("USERPROFILE")
    return os.path.join(root, rel)

# 存在しないパスを None に変換する
def to_local_path(s):
    if os.path.exists(s):
        return s
    return None
# ウィンドウを探す
def find_window(exe_name, class_name=None):
    found = [None]
    def _callback(wnd, arg):
        if not wnd.isVisible() : return True
        if not fnmatch.fnmatch(wnd.getProcessName(), exe_name) : return True
        if class_name and not fnmatch.fnmatch(wnd.getClassName(), class_name) : return True
        found[0] = wnd.getLastActivePopup()
        return False
    pyauto.Window.enum(_callback, None)
    return found[0]

# 最大10回アクティブ化にトライする
def activate_window(wnd):
    if wnd.isMinimized():
        wnd.restore()
    trial = 0
    while trial < 10:
        trial += 1
        try:
            wnd.setForeground()
            if pyauto.Window.getForeground() == wnd:
                wnd.setForeground(True)
                return True
        except:
            return False
    return False
