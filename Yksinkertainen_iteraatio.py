# Ratkaistaan rekursiivinen yhtälö z_{n + 1} = z_n**2 + 1, z_0 = 0

# _ = alaindexi

import matplotlib.pyplot as plt

# Määritellään alkuarvo
z_0 = 0

# Maksimiarvo n:lle
n_max = 5

# Alustetaan muuttuja z
z = z_0

# Luodaan taulukko z:lle
z_array = [z_0]

for n  in range(n_max):
    # Lasketaan uusi arvo z:lle
    z_new = z**2 + 1
    print(z**2 +1)
    # Päivitetään z
    z = z_new
    #print(z_new)
    # Lisätään z taulukkoon
    z_array.append(z)

    
# Luodaan kuva 
fig, ax = plt.subplots()

#plotataan data
ax.scatter(range(n_max + 1), z_array)

# Lisätään kuvaajan otsikko ja akseleiden nimet
ax.set_xlabel("n")
ax.set_ylabel("z_n")
ax.set_title("Yksinkertainen iteraatio")
ax.grid(True)

# Näytetään kuvaaja
plt.show()