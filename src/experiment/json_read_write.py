import json
import os

def json_read(file_path : str):
    # JSONファイルを読み込む
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 読み込んだデータを表示
    print(data)
    return

def json_write_1(file_path:str):
    # 書き込むデータ
    data = {
        "MasterFolderPath":".\master"
        ,"MasterFiles":{
            "WhiteListFileName":"whiteList.txt",
            "BlackListFileName":"blackList.txt",
            "DictListFileName":"dictList.txt"
        }
    }

    # JSONファイルに書き込む
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    # ensure_ascii=False: 日本語などの非ASCII文字をそのままにします。
    # indent=4: 見やすいようにインデントを設定します（オプション）。
        
    # 呼び出しサンプル
    # JSONファイルを読み込む
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    print(data)
    print(f'MasterFolderPath:{data["MasterFolderPath"]}')
    print(f'MasterFiles:{data["MasterFiles"]}')
    print(f'WhiteListFileName:{data["MasterFiles"]["WhiteListFileName"]}')
    return

def json_write_2(file_path:str):
    # 書き込むデータ
    data = {
        "name": "Alice",
        "age": 25,
        "city": "Wonderland",
        "is_student": True,
        "courses": ['Philosophy', 'Physics']
    }

    # JSONファイルに書き込む
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    # ensure_ascii=False: 日本語などの非ASCII文字をそのままにします。
    # indent=4: 見やすいようにインデントを設定します（オプション）。
    return

def read_file(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.replace('\r','').replace('\n','')
            if line == "" : continue
            print(line)
    return

def main():
    # このpyファイルが存在するディレクトリのパスとファイルパスを結合
    file_path = 'sample_files\sample.ini'
    file_path = os.path.join(os.path.dirname(__file__), file_path)
    # JSON読込サンプル
    print('file read')
    read_file(file_path)
    print('json read')
    json_read(file_path)
    # JSON書込サンプル
    print('json write')
    json_write_1(file_path)
    print('file read')
    read_file(file_path)
    print('json read')
    json_read(file_path)
    #json_write_2(file_path) # データ戻し
    return

if __name__ == '__main__':
    main()
