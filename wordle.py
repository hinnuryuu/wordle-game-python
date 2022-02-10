import linecache
import random

word = ""
count = 0


def prepare():
    file = open('wordle_words.txt', 'r')
    global count
    count = 0
    for line in file:
        count += 1
    file.close()

    rand = random.randint(1, count)
    global word
    word = linecache.getline('wordle_words.txt', rand).strip()
