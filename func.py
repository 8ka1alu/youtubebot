import random

def diceroll(cnt, max):
    total = 0
    num_list = []
    for i in range(0, cnt):
        # ランダムに1からサイコロの面数までの和を取得しリストに入れる
        num = random.randint(1, max)
        num_list.append(num)
    # さいころの目の総和を計算しリストに入れる
    total = sum(num_list)
    num_list.append(total)
    return num_list
