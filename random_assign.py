import logging
import random
from member_init import member_init


# Main ---
def random_assign():
    logging.basicConfig(level=logging.INFO,
                        format=' %(asctime)s - %(levelname)s - %(message)s')
    logging.info('#=== Start program ===#')

    candidate_pool, done_pool = get_member_list()
    if candidate_pool[0] == '':
        if done_pool[0] == '':
            member_init()
        else:
            pool_reset()
        candidate_pool, done_pool = get_member_list()
    logging.info(f'Candidate lists: {candidate_pool}')
    logging.info(f'Done lists: {done_pool}')

    selected_member = random.choice(candidate_pool)
    candidate_pool.remove(selected_member)
    if done_pool[0] == '':
        done_pool = [selected_member]
    else:
        done_pool.append(selected_member)
    print(f'Select: {selected_member}')
    with open('unassigned.txt', 'w', encoding="utf-8") as f:
        f.write(make_pool_text(candidate_pool))
    with open('assigned.txt', 'w', encoding="utf-8") as f:
        f.write(make_pool_text(done_pool))

    logging.info('#=== Finish program ===#')


# functions ---
def get_member_list():
    logging.info('#=== Get Member list ===#')
    with open('unassigned.txt', 'r', encoding="utf-8") as f:
        candidate_pool = f.read().split(',')
    with open('assigned.txt', 'r', encoding="utf-8") as f:
        done_pool = f.read().split(',')
    return candidate_pool, done_pool


def pool_reset():
    with open('assigned.txt', 'r', encoding="utf-8") as f:
        assigned = f.read()
    with open('unassigned.txt', 'w', encoding="utf-8") as f:
        f.write(assigned)
    with open('assigned.txt', 'w', encoding="utf-8") as f:
        f.write('')


def make_pool_text(pool_list):
    write_text = ''
    for member in pool_list:
        write_text += f'{member},'
    logging.info(write_text[:-1])
    return write_text[:-1]


# Global ---
if __name__ == "__main__":
    random_assign()
