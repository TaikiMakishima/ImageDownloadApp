import configparser
import sqlite3
import os
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read()
        result = chardet.detect(rawdata)
        return result['encoding']

# ���݂̃X�N���v�g�̐�΃p�X���擾
current_dir = os.path.dirname(os.path.abspath(__file__))

# �e�ݒ�t�@�C���ւ̐�΃p�X���쐬
config_path = os.path.join(current_dir, '..', '..', 'config')
common_config = os.path.join(config_path, 'config.ini')
local_config_path = os.path.join(config_path, 'localConfig.ini')

# config.ini�̓ǂݍ���
config = configparser.ConfigParser()
config_encoding = detect_encoding(common_config)
config.read(common_config, encoding=config_encoding)

# localConfig.ini�̓ǂݍ���
local_config = configparser.ConfigParser()
local_config_encoding = detect_encoding(local_config_path)
local_config.read(local_config_path, encoding=local_config_encoding)

# localConfig.ini�̐ݒ��config.ini�̐ݒ�Ƀ}�[�W����
for section in local_config.sections():
    if not config.has_section(section):
        config.add_section(section)
    for key, val in local_config.items(section):
        config.set(section, key, val)

# �g�p��: �}�[�W��̃f�[�^�x�[�X�����擾
db_name = config['database']['name']
print(db_name)

# SQLite�f�[�^�x�[�X���쐬 (�܂��͐ڑ�)
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# �T���v���e�[�u�����쐬
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
