"""
Ratkaistaan rekusriivinen yhtälö x_{n + 1} = r * x_n * (1-x_n), r = reaaliluku, x_0 = alkuarvo
"""

import matplotlib.pyplot as plt

# Alkuarvot
x_0 = 0.5
r = 2.9

# MaksimiArvo n:lle
n_max = 50

x = x_0

# Tehdään taulukko x:lle
x_array = [x_0]

for n  in range(n_max):
    # Lasketaan uusi arvo x:lle
    x_new = r * x * (1 - x)
    
    # Päivitetään x
    x = x_new

    # Lisätään x taulukkoon
    x_array.append(x)

    # Luodaan kuva 
fig, ax = plt.subplots()

#plotataan data
ax.scatter(range(n_max + 1), x_array)

# Lisätään kuvaajan otsikko ja akseleiden nimet
ax.set_xlabel("n")
ax.set_ylabel("x_n")
ax.set_title("Yksinkertainen iteraatio")
ax.grid(True)

# Näytetään kuvaaja
plt.show()