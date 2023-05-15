import numpy as np


def loop_count(p):
    p = round(p, 4)

    while True:
        r = p % 1
        if r == 0:
            break

        p = round(p * 10, 4)

    p = int(p)
    
    win_loop = p
    if p < 10:
        loss_loop = 10 - p
    elif p < 100:
        loss_loop = 100 - p
    elif p < 1000:
        loss_loop = 1000 - p
    elif p < 10000:
        loss_loop = 10000 - p
    else:
        raise

    return (win_loop, loss_loop)


def simulation(p, win, loss, money=100, loop=1):
    win_loop, loss_loop = loop_count(p)
    
    money_list = list()
    for bet in np.arange(0, 1.001, 0.001):
        money = 100
        for _ in range(loop):
            for _ in range(win_loop):
                money += (money * bet * win)

            for _ in range(loss_loop):
                money -= (money * bet * loss)

        money_list.append(money)

    max_money = max(money_list)
    best_bet = money_list.index(max_money) / 1000
    bet_10 = round(money_list[100])
    bet_20 = round(money_list[200])
    bet_30 = round(money_list[300])
    bet_40 = round(money_list[400])
    bet_50 = round(money_list[500])
    bet_60 = round(money_list[600])
    bet_70 = round(money_list[700])
    bet_80 = round(money_list[800])
    bet_90 = round(money_list[900])
    bet_100 = round(money_list[1000])

    data = {
        'game_count': win_loop + loss_loop,
        'best_bet': best_bet,
        'best_money': round(max_money),
        'bet_10': bet_10,
        'bet_20': bet_20,
        'bet_30': bet_30,
        'bet_40': bet_40,
        'bet_50': bet_50,
        'bet_60': bet_60,
        'bet_70': bet_70,
        'bet_80': bet_80,
        'bet_90': bet_90,
        'bet_100': bet_100
    }

    return data


if __name__ == '__main__':
    p = 0.6 # 확률(승률, 0.3 = 30%)
    win = 0.05 # 수익률(수익이 발생했을 때, 0.1 = 10%, 2 = 200%)
    loss = 0.02 # 손실률(손실이 발생했을 때, 0.1 = 10%, 2 = 200%)

    print(f'p: {p}, win: {win}, loss: {loss}')
    data = simulation(p, win, loss)
    print(data)

