import math


def calculate_weight(n1, n2):
    """
    PDF formülü: 1 / (1 + sqrt((a1-a2)^2 + (e1-e2)^2 + (b1-b2)^2))
    Benzer özellikler → yüksek ağırlık, farklı özellikler → düşük ağırlık.
    """
    d1 = (n1.aktiflik - n2.aktiflik) ** 2
    d2 = (n1.etkilesim - n2.etkilesim) ** 2
    d3 = (n1.baglanti_sayisi - n2.baglanti_sayisi) ** 2

    return 1 / (1 + math.sqrt(d1 + d2 + d3))
