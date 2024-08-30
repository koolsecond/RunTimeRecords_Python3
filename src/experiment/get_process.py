# プロセス取得
# 以下の３つが必要
# プロセスID、開始時刻、実行ファイルパス、ウィンドウ名
# pip install psutil pywin32
import psutil
from win32 import win32gui
from win32 import win32process
import datetime

def get_window_title(pid):
    """プロセスIDに関連付けられたウィンドウ名を取得"""
    def callback(hwnd, titles):
        # すべてのウィンドウを列挙し、指定されたPIDに対応するウィンドウタイトルを検索
        if win32gui.IsWindowVisible(hwnd):
            _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
            if found_pid == pid:
                titles.append(win32gui.GetWindowText(hwnd))
        return True

    titles = []
    win32gui.EnumWindows(callback, titles)
    return titles[0] if titles else None

def main():
    # 実行中のすべてのプロセスを繰り返し処理
    for proc in psutil.process_iter(['pid', 'create_time', 'exe']):
        try:
            pid = proc.info['pid']
            
            # 実行ファイルパスの取得と絞り込み
            exe_path = proc.info['exe']
            if not str(exe_path).startswith('D:') : continue
            
            # ウィンドウタイトルの取得と絞り込み（取得できないものはスキップ）
            window_title = get_window_title(pid)
            if window_title is None : continue
            
            # プロセスの開始時刻を取得し、読みやすい形式に変換
            create_time = datetime.datetime.fromtimestamp(proc.info['create_time']).strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"PID: {pid}, 開始時刻: {create_time}, 実行ファイルパス: {exe_path}, ウィンドウ名: {window_title}")

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # アクセス拒否などのケースは処理無し
            pass
    return

if __name__ == "__main__":
    main()
