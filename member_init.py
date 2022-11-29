from dotenv import load_dotenv
import logging
import os


# Main ---
def member_init():
    logging.basicConfig(level=logging.INFO,
                        format=' %(asctime)s - %(levelname)s - %(message)s')
    load_dotenv()

    logging.info('#=== member initilization ===#')
    members = os.getenv('MEMBERS')
    with open('unassigned.txt', 'w', encoding="utf-8") as f:
        f.write(members)
    with open('assigned.txt', 'w', encoding="utf-8") as f:
        f.write('')
    logging.info('#=== initilization finished ===#')

# functions ---


# Global ---
if __name__ == "__main__":
    member_init()
