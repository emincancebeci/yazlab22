def calculate_weight(n1, n2):
    d1 = (n1.aktiflik - n2.aktiflik) ** 2
    d2 = (n1.etkilesim - n2.etkilesim) ** 2
    d3 = (n1.baglanti_sayisi - n2.baglanti_sayisi) ** 2

    return 1 / (1 + d1 + d2 + d3)
