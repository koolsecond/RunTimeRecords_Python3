import os
from abc import ABC, abstractmethod
from datetime import datetime
import sqlite3

class run_time_records_database_manager():
    @abstractmethod
    def create(self, table_name, columns: dict):
        raise NotImplementedError('必ず実装すること')

    @abstractmethod
    def insert(self, table_name, data: dict):
        raise NotImplementedError('必ず実装すること')

    @abstractmethod
    def update(self, table_name, data_dict : dict):
        raise NotImplementedError('必ず実装すること')
    
    @abstractmethod
    def delete(self, table_name, criteria: dict):
        raise NotImplementedError('必ず実装すること')

    @abstractmethod
    def select(self, table_name, criteria: dict = None, order_by = None):
        raise NotImplementedError('必ず実装すること')

class DatabaseManager_sqlite3(run_time_records_database_manager):
    def __init__(self, database_filename) -> None:
        self.connection = sqlite3.connect(database_filename)
        return

    def __del__(self):
        self.connection.close()
        return
    
    def __enter__(self):
        print('open database OK!')
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            print('close database OK!')
        else:
            print('--------')
            print(exc_type)
            print('--------')
            return True


    def _execute(self, statement, values : tuple = None):
        with self.connection: # トランザクション制御
            cursor = self.connection.cursor()
            cursor.execute(statement, values or [])
            return cursor
    
    def create(self, table_name, columns: dict):
        columns_with_types = [
            f'{column_name} {data_type}'
            for column_name, data_type in columns.items()
        ]
        query = f'CREATE TABLE IF NOT EXISTS {table_name} '
        columns_for_query = ', '.join(columns_with_types)
        query += f'({columns_for_query})'
        self._execute(query)
        
    def insert(self, table_name, data: dict):
        column_name = ', '.join(data.keys())
        placeholders = ', '.join('?' * len(data))
        column_values = tuple(data.values())
        query = f'INSERT INTO {table_name} '
        query += f'({column_name}) '
        query += f'VALUES ({placeholders})'
        self._execute(query, column_values)

    def update(self, table_name, data : dict, key_data : dict):
        # print('create set_placeholders')
        set_placeholders = [ f'{column_name} = ?' for column_name in data.keys() ]
        set_placeholders = ', '.join(set_placeholders)
        # print('create where_placeholders')
        where_placeholders = [ f'{column} = ?' for column in key_data.keys() ]
        where_placeholders = ' AND '.join(where_placeholders)
        # print('create query')
        query = f'UPDATE {table_name} '
        query += 'SET '
        query += f'{set_placeholders}'
        query += f'WHERE {where_placeholders}'
        # print('create placeholders pre')
        all_data = list(data.values()) + list(key_data.values())
        # print('create placeholders')
        placeholders = tuple(all_data)
        # print('execute')
        self._execute(query, placeholders)

    def delete(self, table_name, criteria: dict):
        placeholders = [ f'{column} = ?' for column in criteria.keys() ]
        delete_criteria = ' AND '.join(placeholders)
        query = f'DELETE FROM {table_name} '
        query += f'WHERE {delete_criteria}'
        self._execute(query, tuple(criteria.values()))

    def select(self, table_name, criteria: dict = None, order_by = None):
        criteria = criteria or {}
        query = f'SELECT * FROM {table_name} '
        if criteria:
            placeholders = [f'{column} = ?' for column in criteria.keys() ]
            select_criteria = ' AND '.join(placeholders)
            query += f' WHERE {select_criteria}'
        if order_by:
            query += f' ORDER BY {order_by}'

        return self._execute(query, tuple(criteria.values()))

class run_time_records_table_manager(ABC):
    @abstractmethod
    def create(self):
        raise NotImplementedError('必ず実装すること')

    @abstractmethod
    def insert(self, data : dict):
        raise NotImplementedError('必ず実装すること')

    @abstractmethod
    def update(self, data : dict):
        raise NotImplementedError('必ず実装すること')
    
    @abstractmethod
    def delete(self, key_list : list):
        raise NotImplementedError('必ず実装すること')

    @abstractmethod
    def select(self, order_by=None):
        raise NotImplementedError('必ず実装すること')

class table_process_history(run_time_records_table_manager):
    ID = 'id'
    PROCESS_ID = 'process_id'
    PROCESS_START_TIME = 'process_start_time'
    EXECUTABLE_PATH = 'executable_path'
    WINDOW_NAME = 'window_name'
    RUN_TIME = 'run_time'
    def __init__(self, db: run_time_records_database_manager) -> None:
        self.table_name = 'process_history'
        self.db = db
        return
    
    def create(self):
        columns = {
             self.ID : 'INTEGER PRIMARY KEY AUTOINCREMENT'
            ,self.PROCESS_ID : 'INTEGER not null'
            ,self.PROCESS_START_TIME : 'TEXT not null'
            ,self.EXECUTABLE_PATH : 'TEXT not null'
            ,self.WINDOW_NAME : 'TEXT not null'
            ,self.RUN_TIME: 'INTEGER not null'
        }
        self.db.create(self.table_name, columns)
        return

    def insert(self, process_id, process_start_time, executable_path, window_name, run_time):
        data = dict()

        if process_id is None: return
        data[self.PROCESS_ID] = process_id

        if process_start_time is None: return
        data[self.PROCESS_START_TIME] = process_start_time

        if executable_path is None: return
        data[self.EXECUTABLE_PATH] = executable_path

        if window_name is None: return
        data[self.WINDOW_NAME] = window_name

        if run_time is None: return
        data[self.RUN_TIME] = run_time

        self.db.insert(self.table_name, data)

    def update(self, id, process_id = None, process_start_time = None, executable_path = None, window_name = None, run_time = None):
        # print('check id')
        if id is None: return
        key_data = dict()
        key_data[self.ID] = id

        data = dict()
        # print('check process_id')
        if process_id is not None:
            data[self.PROCESS_ID] = process_id

        # print('check process_start_time')
        if process_start_time is not None:
            data[self.PROCESS_START_TIME] = process_start_time

        # print('check executable_path')
        if executable_path is not None:
            data[self.EXECUTABLE_PATH] = executable_path

        # print('check window_name')
        if window_name is not None:
            data[self.WINDOW_NAME] = window_name

        # print('check run_time')
        if run_time is not None:
            data[self.RUN_TIME] = run_time
        
        # print(f'check len(data):{len(data)}')
        if len(data) == 0 : return

        # print('execute update')
        self.db.update(self.table_name, data, key_data)
    
    def delete(self, id):
        self.db.delete(self.table_name, {
              self.ID: id
        })

    def select(self, order_by=None):
        rows = self.db.select(self.table_name).fetchall()
        return rows

def use_database_sample():
    # このpyファイルが存在するディレクトリのパスとファイルパスを結合
    file_path = 'sample_files\process_history_sample.db'
    file_path = os.path.join(os.path.dirname(__file__), file_path)
    # サンプル用の時刻データ
    #now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    now_time = '2024-09-02 16:47:50'
    # db接続オブジェクトの生成～使用
    with DatabaseManager_sqlite3(file_path) as db:
        print('＜テーブルオブジェクトの生成＞') 
        process_history = table_process_history(db)
        
        print('＜テーブルの作成＞')
        process_history.create()
        
        print('＜データの追加・表示＞')
        process_history.insert(1111, now_time, "/path/to/executable_1", "Window Name_1", 120)
        process_history.insert(2222, now_time, "/path/to/executable_2", "Window Name_2", 120)
        processes = process_history.select()
        for process in processes:
            print(process)

        print('＜データの変更・表示＞')
        process_history.update(1, 1111, now_time, "/path/to/executable_1_change", "Window Name_1", 120)
        processes = process_history.select()
        for process in processes:
            print(process)

        print('＜データの削除・表示＞')
        process_history.delete(1)
        processes = process_history.select()
        for process in processes:
            print(process)

    return

if __name__ == '__main__':
    use_database_sample()
