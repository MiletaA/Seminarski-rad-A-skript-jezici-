from random import randint, randrange
from Data import data

def tekuci_racun_gen(ime_prezime):
    d = data()
    alphabets = 'abcdefghijklmnopqrstuvwxyz'
    t_r = ''
    t_r += str(len(d.keys()) + 10)
    for alpha in ime_prezime:
        if (len(t_r) < 12):
            if alpha in alphabets:
                index = alphabets.rfind(alpha)
                t_r += str(index + 1)

            else:
                t_r += '0'

        else:
            break

    if len(t_r) > 12:
        final_t_r = ''
        for index in t_r:
            if len(final_t_r) < 12:
                final_t_r += index

        t_r = final_t_r
        return t_r

    if len(t_r) < 12:
        remain_index = 12 - len(t_r)
        for index in range(remain_index):
            t_r += str(randint(0,9))

        return t_r

    else:
        return t_r

