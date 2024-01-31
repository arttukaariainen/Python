"""
Ratkaistaan liikeyhtälöt jousesta roikkuvalle massalle käyttäen Verlet'n menetelmää.
"""

import matplotlib.pyplot as plt

# Määritellään fysikaaliset vakiot
g = 10
k = 1
m = 1
L = 0

# Alkuarvot paikalle ja nopeudelle
x_0 = 1
v_0 = 0

# Aikaan liittyvät muuttujat
t_0 = 0
t_max = 20
dt = 0.1

# Alustetaan muuttujat
x = x_0
v = v_0
t = t_0

# Taulukot muuttujille
x_array = [x_0]
v_array = [v_0]
t_array = [t_0]

# Iteroidaan aikaa eteenpäin
while t < t_max:
    # Lasketaan uudet arvot
    a = g - k/m * (x - L) - 0.2 * v
    x_new = x + dt * v + 0.5 * dt**2 * a
    v_new = v + dt * a
    a_new = g - k/m * (x_new - L) - 0.2 * v_new
    v_new = v + dt * (a + a_new)/2
    t_new = t + dt

    # Päivitetään
    x = x_new
    v = v_new
    t = t_new

    # Lisätään taulukkoon
    x_array.append(x)
    v_array.append(v)
    t_array.append(t)


# Luodaan kuvaaja liikkeestä
fig, ax = plt.subplots()
ax.scatter(t_array, x_array)
plt.show()