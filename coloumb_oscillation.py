import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

data = np.genfromtxt('QD_80mKG4_182_G7_195_G9_315N0P05m.txt', dtype=float)
Vg = data[:, 0]
original_G = data[:, 5]
G = np.zeros_like(original_G)

# method1--Prof.Liang's method ###
# mean_size = 50
# for i in range(len(original_G)-mean_size):
#     G[i] = original_G[i]-np.mean(original_G[range(i, i+mean_size)])


# method2--adjacent averaging w/ Yi Fang's method
## 1.find the adjacent averages ###
mean_radius = 25
for i in range(len(original_G)):
    if i < mean_radius:  ## lower limit
        G[i] = np.mean(original_G[range(0, i + mean_radius)])
    elif len(G) - i < mean_radius:  ## upper limit
        G[i] = np.mean(original_G[range(i - mean_radius, len(G))])
    else:  ## anything in between
        G[i] = np.mean(original_G[range(i - mean_radius, i + mean_radius)])
## 2.subtract mean from original data ###
G = original_G - G
# ## 3.then find the local minimas of G ###
vg_minima = []
g_minima = []
for i in range(2, len(G) - 2):
    if G[i] < 0 and G[i - 2] > G[i - 1] > G[i] \
            and G[i] < G[i + 1] < G[i + 2]:
        vg_minima.append(Vg[i])  ## X-axis minimas
        g_minima.append(G[i])  ## Y-axis minimas
# ## 4.then use interpolate to fit a curve ###
f = interpolate.interp1d(vg_minima, g_minima, kind='quadratic',
                         fill_value='extrapolate')
vg_new = Vg
g_new = f(vg_new)
# ## 5. remove the base value and plot ###
G = G - g_new


plt.plot(Vg, G, 'r-', label='measured')
# plt.plot(vg_minima,g_minima, 'b.', label='measured')
# plt.plot(vg_minima, g_minima,'o', vg_new, g_new,'-')
plt.xlabel('Vg')
plt.ylabel('G')
plt.show()