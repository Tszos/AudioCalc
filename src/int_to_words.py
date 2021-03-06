from six import u

from src.config import JEDNOSTKI, SETKI, NASTKI, DZIESIATKI, WIELKIE, GROSZE, ZLOTOWKI
"""Liczba słownie.
kwotaslownie - kwota słownie ("sto pięć złotych 3 grosze")
lslownie - liczba slownie ("dwieście dwadzieścia trzy")
cosslownie - rzecz słownie, odmiana jako argument ("dwadzieścia niedźwiedzi")
"""

def _slownie3cyfry(liczba):
    je = liczba % 10
    dz = (liczba // 10) % 10
    se = (liczba // 100) % 10
    slowa = []

    if se > 0:
        slowa.append(SETKI[se])
    if dz == 1:
        slowa.append(NASTKI[je])
    else:
        if dz > 0:
            slowa.append(DZIESIATKI[dz])
        if je > 0:
            slowa.append(JEDNOSTKI[je])
    retval = u(" ").join(slowa)
    return retval


def _przypadek(liczba):
    je = liczba % 10
    dz = (liczba // 10) % 10

    if liczba == 1:
        typ = 0  # jeden tysiąc"
    elif dz == 1 and je > 1:  # naście tysięcy
        typ = 2
    elif 2 <= je <= 4:
        typ = 1  # [k-dziesiąt/set] [dwa/trzy/czery] tysiące
    else:
        typ = 2  # x tysięcy

    return typ


def lslownie(liczba):
    """Liczba całkowita słownie"""
    trojki = []
    if liczba == 0:
        return u("zero")
    while liczba > 0:
        trojki.append(liczba % 1000)
        liczba = liczba // 1000
    slowa = []
    for i, n in enumerate(trojki):
        if n > 0:
            if i > 0:
                p = _przypadek(n)
                w = WIELKIE[i][p]
                slowa.append(_slownie3cyfry(n) + u(" ") + w)
            else:
                slowa.append(_slownie3cyfry(n))
    slowa.reverse()
    return u(" ").join(slowa)


def cosslownie(liczba, cos):
    """Słownie "ileś cosiów"
    liczba - int
    cos - tablica przypadków [coś, cosie, cosiów]"""

    return lslownie(liczba) + u(" ") + cos[_przypadek(liczba)]


def kwotaslownie(liczba, fmt=0):
    """Słownie złotych, groszy.
    liczba - float, liczba złotych z groszami po przecinku
    fmt - (format) jesli 0, to grosze w postaci xx/100, słownie w p. przypadku
    """
    lzlotych = int(liczba)
    lgroszy = int(liczba * 100 + 0.5) % 100
    if fmt != 0:
        groszslownie = cosslownie(lgroszy, GROSZE)
    else:
        groszslownie = u("%d/100") % lgroszy
    return cosslownie(lzlotych, ZLOTOWKI) + u(" ") + groszslownie

