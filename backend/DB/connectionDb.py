import configparser
import sqlite3
import os
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read()
        result = chardet.detect(rawdata)
        return result['encoding']

# 現在のスクリプトの絶対パスを取得
current_dir = os.path.dirname(os.path.abspath(__file__))

# 各設定ファイルへの絶対パスを作成
config_path = os.path.join(current_dir, '..', '..', 'config')
common_config = os.path.join(config_path, 'config.ini')
local_config_path = os.path.join(config_path, 'localConfig.ini')

# config.iniの読み込み
config = configparser.ConfigParser()
config_encoding = detect_encoding(common_config)
config.read(common_config, encoding=config_encoding)

# localConfig.iniの読み込み
local_config = configparser.ConfigParser()
local_config_encoding = detect_encoding(local_config_path)
local_config.read(local_config_path, encoding=local_config_encoding)

# localConfig.iniの設定をconfig.iniの設定にマージする
for section in local_config.sections():
    if not config.has_section(section):
        config.add_section(section)
    for key, val in local_config.items(section):
        config.set(section, key, val)

# 使用例: マージ後のデータベース名を取得
db_name = config['database']['name']
print(db_name)

# SQLiteデータベースを作成 (または接続)
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# サンプルテーブルを作成
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
)
''')

conn.commit()
conn.close()

print(f"Database '{db_name}' has been created and initialized.")
