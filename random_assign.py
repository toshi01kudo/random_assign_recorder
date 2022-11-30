import logging
import random
import os
import sys
from dotenv import load_dotenv


# Main ---
def main(assign_num=1):
    logging.basicConfig(level=logging.INFO,
                        format=' %(asctime)s - %(levelname)s - %(message)s')
    logging.info('#=== Start program ===#')
    usage_text = '\n Usage: \n' +\
                 ' - Assign: python3 random_assign.py N \n   - Ex: python3 random_assign.py 2 \n' +\
                 ' - Check pool: python3 random_assign.py read\n' +\
                 ' - Pool reset: python3 random_assign.py reset\n'

    if len(sys.argv) >= 2:
        if sys.argv[1] == 'read':
            logging.info('#=== Read mode ===#')
            rar = random_assign_recorder()
            print(f'Unassigned: {rar.candidate_pool}')
            print(f'Assigned: {rar.done_pool}')
            logging.info('#=== Read finished ===#')
            sys.exit()
        elif sys.argv[1] == 'init' or sys.argv[1] == 'reset':
            logging.info('#=== Reset action ===#')
            rar = random_assign_recorder()
            rar.file_init()
            print(f'Unassigned: {rar.candidate_pool}')
            print(f'Assigned: {rar.done_pool}')
            logging.info('#=== Reset finished ===#')
            sys.exit()
        elif sys.argv[1] == '-v':
            # unittest から呼ばれてると想定
            pass
        else:
            try:
                assign_num = int(sys.argv[1])
            except Exception as e:
                logging.error(f'{usage_text} {e}')
                sys.exit()

    rar = random_assign_recorder(assign_num)
    rar.select()

    logging.info('#=== Finish program ===#')
    return rar.selected


# functions ---
# def get_member_list():
#     logging.info('#=== Get Member list ===#')
#     with open('unassigned.txt', 'r', encoding="utf-8") as f:
#         candidate_pool = f.read().split(',')
#     with open('assigned.txt', 'r', encoding="utf-8") as f:
#         done_pool = f.read().split(',')
#     return candidate_pool, done_pool


# def pool_reset():
#     with open('assigned.txt', 'r', encoding="utf-8") as f:
#         assigned = f.read()
#     with open('unassigned.txt', 'w', encoding="utf-8") as f:
#         f.write(assigned)
#     with open('assigned.txt', 'w', encoding="utf-8") as f:
#         f.write('')


# def make_pool_text(pool_list):
#     write_text = ''
#     for member in pool_list:
#         write_text += f'{member},'
#     logging.info(write_text[:-1])
#     return write_text[:-1]

def filepath_at_repodir(filename1):
    """ リポジトリのルートディレクトリを視点としてファイルパスを指定する関数 """
    logging.info(f"Filepath: {os.path.abspath(os.path.join(os.path.dirname(__file__), filename1))}")
    return os.path.abspath(os.path.join(os.path.dirname(__file__), filename1))


# Class ---
class random_assign_recorder():
    """ Random アサインを行うクラス """

    # Initial: ---
    def __init__(self, assign_num=1):
        self.assign_num = assign_num  # アサインメンバー数
        self.candidate_pool = []  # アサイン前メンバー
        self.staged_pool = []  # アサインメンバー
        self.done_pool = []  # 他タスクへアサイン済みメンバー
        self.selected = []

        self._file_exist_check()
        self._file_validation()

    # Private Functions: ---
    def _file_exist_check(self):
        """ 必要ファイルが存在するか確認し、無ければ作成する """
        if not os.path.isfile(filepath_at_repodir('.env')):
            raise Exception
        load_dotenv()
        if not os.path.isfile(filepath_at_repodir('unassigned.txt')):
            members = os.getenv('MEMBERS')
            with open(filepath_at_repodir('unassigned.txt'), 'w', encoding="utf-8") as f:
                f.write(members)
        if not os.path.isfile(filepath_at_repodir('assigned.txt')):
            with open(filepath_at_repodir('assigned.txt'), 'w', encoding="utf-8") as f:
                f.write('')

    def _file_validation(self):
        """ 必要ファイルの中身を確認し、適切に処理する """
        self.load()
        if len(self.candidate_pool) == 0:
            if len(self.done_pool) == 0:
                self.file_init()
            else:
                self.reset()
            self.load()

    def _make_pool_text(self, pool_list):
        write_text = ''
        for member in pool_list:
            write_text += f'{member},'
        return write_text[:-1]

    # Global Functions: ---
    def file_init(self):
        """ メンバーリストファイルの初期化 """
        if not os.path.isfile('.env'):
            raise Exception
        load_dotenv()
        logging.info('#=== member initilization ===#')
        members = os.getenv('MEMBERS')
        with open(filepath_at_repodir('unassigned.txt'), 'w', encoding="utf-8") as f:
            f.write(members)
        with open(filepath_at_repodir('assigned.txt'), 'w', encoding="utf-8") as f:
            f.write('')
        self.load()
        if len(self.candidate_pool) == 0:
            raise Exception
        logging.info('#=== initilization finished ===#')

    def load(self):
        """ メンバーリスト読み込み unassigned, assigned のファイルから各 Pool へ保存 """
        with open(filepath_at_repodir('unassigned.txt'), 'r', encoding="utf-8") as f:
            self.candidate_pool = f.read().split(',')
        with open(filepath_at_repodir('assigned.txt'), 'r', encoding="utf-8") as f:
            self.done_pool = f.read().split(',')
        if self.candidate_pool == ['']:
            self.candidate_pool = []
        if self.done_pool == ['']:
            self.done_pool = []

    def pop(self):
        """ メンバーを staged_pool へ移動 """
        if len(self.candidate_pool) == 0:
            self.reset()
        selected = random.choice(self.candidate_pool)
        self.candidate_pool.remove(selected)
        self.staged_pool.append(selected)

    def push(self):
        """ staged_pool のメンバーを done_pool へ移動 """
        self.done_pool.extend(self.staged_pool)
        self.staged_pool = []

    def reset(self):
        """ done_pool を全て candidate_pool へ移動 """
        self.candidate_pool = self.done_pool
        self.done_pool = []

    def save(self):
        """ メンバーリスト保存 """
        with open(filepath_at_repodir('unassigned.txt'), 'w', encoding="utf-8") as f:
            f.write(self._make_pool_text(self.candidate_pool))
        with open(filepath_at_repodir('assigned.txt'), 'w', encoding="utf-8") as f:
            f.write(self._make_pool_text(self.done_pool))

    def select(self):
        """ メンバーを選出する関数 """
        self.selected = []
        for i in range(self.assign_num):
            self.pop()
        print(f'Selected: {self.staged_pool}')
        logging.info(f'selected: {self.staged_pool}')
        self.selected = self.staged_pool
        self.push()
        self.save()
        logging.info(f'unassigned: {self.candidate_pool}')
        logging.info(f'assigned: {self.done_pool}')


# Global ---
if __name__ == "__main__":
    main()
