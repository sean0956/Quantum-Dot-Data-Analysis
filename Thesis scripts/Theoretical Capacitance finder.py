import numpy as np
from scipy import constants as const

#### Gate Capacitance and  The single-particleenergy level spacing
epi_0 = const.epsilon_0 ## F/m

## GaAs
R= 220*(1e-9)
k_GaAs = 12.9
C = 8*epi_0*k_GaAs*R
E = (const.elementary_charge**2)/C*6.24150913 * 1e18
print(C*1e18,E)

# A = 200*1e-9 * 200*1e-9
# d = 50*1e-9
# C_tot = k_GaAs*epi_0*A/d
# print(C_tot*1e18)


spacing = const.hbar**2/0.067/const.electron_mass/R/R*6.24150913*10e18
print(spacing)
## Bilayer

# k_Si = 3.9
# k_Al2O3 = 9.1

# A = 50*(1e-9) * 100*(1e-9) ## m
# d_Si = 30*1e-9
# d_Al2O3 = 10*1e-9
# Cg = epi_0*A*(k_Si/d_Si+k_Al2O3/d_Al2O3)
# print(Cg)
#
# spacing = 2*const.pi*const.hbar**2/4/0.19/const.electron_mass/A*6.24150913*10e18
# print(spacing)

## Trilayer

#
# k_Si = 3.9
# k_Al2O3 = 9.1
#
# A = 50*(1e-9) * 80*(1e-9) ## m
# d_Si = 30*1e-9
# d_Al2O3 = 30*1e-9
# Cg = epi_0*A*(k_Si/d_Si+k_Al2O3/d_Al2O3)
# print(Cg*1e18)
#
# spacing = 2*const.pi*const.hbar**2/4/0.19/const.electron_mass/A*6.24150913*10e18
# print(spacing)