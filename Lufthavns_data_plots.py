"""
@author: Mikkel Hviid Thorn og Rebekka Engelund Balle

Lufthavnen:
- Har en landingsbane.
- Vil måske have to landingsbaner.

Ordbog
- ventetider er tiden et fly skal vente før det kan lande, hvor tiden kun tælles, hvis den er forskelligt for nul.
- fly_der_venter er brøkdelen af fly som venter.
- over_lukketid er den tid, hvor sidste fly er landet, relativt til de 13 timer.

Vær opmærksom på at koden gemmer seks figurer når den køres!
"""


import Lufthavns_simulation_module as lsm
import matplotlib.pyplot as plt
import numpy as np


"""
Data, som skal plottes kommer fra simulationen i Lufthavns_simulation_module
"""


år = 12 #antal år 

#gemmer data fra simuleringer med en landingsbane
ventetider, fly_der_venter, over_lukketid = lsm.l_år(år,300,200)

#gemmer data fra simuleringer med to landingsbaner
ventetider2, fly_der_venter2, over_lukketid2 = lsm.l_år_2LB(år,300,200)


"""
Plot udseende
"""


plt.style.use('seaborn')

plt.rc('font', size=20)          # controls default text sizes
plt.rc('axes', titlesize=20)     # fontsize of the axes title
plt.rc('axes', labelsize=20)     # fontsize of the x and y labels
plt.rc('xtick', labelsize=12)    # fontsize of the tick labels
plt.rc('ytick', labelsize=12)    # fontsize of the tick labels
plt.rc('legend', fontsize=15)    # legend fontsize
plt.rc('figure', titlesize=25)   # fontsize of the figure title


"""
Danner et plot over gennemsnitlige ventetider over et antal år.
"""


plt.figure()
plt.plot(np.arange(år+1)+np.repeat(2020,år+1), np.mean(ventetider, axis=1), 'o-', color='firebrick', label='En landingsbane')
plt.plot(np.arange(år+1)+np.repeat(2020,år+1), np.mean(ventetider2, axis=1), 'o-', color='navy', label='To landingsbaner')
plt.xticks(np.linspace(2020, 2020+år, int(år/2+1)))
plt.title('Gennemsnitlig ventetid over 12 år'); plt.legend(loc = 'upper left')
plt.xlabel('Årstal'); plt.ylabel('Ventetid i sekunder')

plt.savefig('gns_ventetider.png', dpi = 500, bbox_inches = 'tight')


"""
Danner et plot over gennemsnitlige antal fly der venter over et antal år.
"""


plt.figure()
plt.plot(np.arange(år+1)+np.repeat(2020,år+1), np.mean(fly_der_venter, axis=1), 'o-', color='firebrick', label='En landingsbane')
plt.plot(np.arange(år+1)+np.repeat(2020,år+1), np.mean(fly_der_venter2, axis=1), 'o-', color='navy', label='To landingsbaner')
plt.xticks(np.linspace(2020, 2020+år, int(år/2+1)))
plt.title('Andel fly som venter med at lande over 12 år'); plt.legend(loc = 'upper left')
plt.xlabel('Årstal'); plt.ylabel('Andel fly som venter')

plt.savefig('gns_andel_fly_der_venter.png', dpi = 500, bbox_inches = 'tight')


"""
Danner et plot over gennemsnitlige lukketid over et antal år.
"""


plt.figure()
plt.plot(np.arange(år+1)+np.repeat(2020,år+1), np.mean(over_lukketid, axis=1), 'o-', color='firebrick', label='En landingsbane')
plt.plot(np.arange(år+1)+np.repeat(2020,år+1), np.mean(over_lukketid2, axis=1), 'o-', color='navy', label='To landingsbaner')
plt.xticks(np.linspace(2020, 2020+år, int(år/2+1)))
plt.title('Relativ lukketid over 12 år'); plt.legend(loc = 'upper left')
plt.xlabel('Årstal'); plt.ylabel('Lukketid i sekunder')

plt.savefig('gns_lukketid.png', dpi = 500, bbox_inches = 'tight')


"""
Histogram over fordelingen af de daglige gennemsnitlige ventetider for en landingsbane.
"""


fig, axs = plt.subplots(2, 2)
fig.suptitle('Fordelingen af ventetider med en landingsbane')

(ax1, ax2), (ax3, ax4) = axs
ax1.hist(ventetider[0], bins=20, density=True, color='firebrick', label='2020')
ax1.legend(loc = 'upper right')

ax2.hist(ventetider[3], bins=20, density=True, color='navy', label='2023')
ax2.legend(loc = 'upper right')

ax3.hist(ventetider[6], bins=20, density=True, color='forestgreen', label='2026')
ax3.legend(loc = 'upper right')

ax4.hist(ventetider[9], bins=20, density=True, color='darkorange', label='2029')
ax4.legend(loc = 'upper right')

fig.text(0.5, 0.02, 'Ventetid i sekunder', ha='center')
fig.text(0.02, 0.5, 'Tæthed', va='center', rotation='vertical')

plt.savefig('hist_ventetider_1LB.png', dpi = 500, bbox_inches = 'tight')


"""
Histogram over fordelingen af de daglige gennemsnitlige ventetider for to landingsbaner.
"""


fig, axs = plt.subplots(2, 2)
fig.suptitle('Fordelingen af ventetider med to landingsbaner')

(ax1, ax2), (ax3, ax4) = axs
ax1.hist(ventetider2[0], bins=20, density=True, color='firebrick', label='2020')
ax1.legend(loc = 'upper right')

ax2.hist(ventetider2[3], bins=20, density=True, color='navy', label='2023')
ax2.legend(loc = 'upper right')

ax3.hist(ventetider2[6], bins=20, density=True, color='forestgreen', label='2026')
ax3.legend(loc = 'upper right')

ax4.hist(ventetider2[9], bins=20, density=True, color='darkorange', label='2029')
ax4.legend(loc = 'upper right')

fig.text(0.5, 0.02, 'Ventetid i sekunder', ha='center')
fig.text(0.02, 0.5, 'Tæthed', va='center', rotation='vertical')

plt.savefig('hist_ventetider_2LB.png', dpi = 500, bbox_inches = 'tight')


"""
Histogram over fordelingen af lukketider for en og to landingsbaner
"""


fig, axs = plt.subplots(2, 2)
fig.suptitle('Fordelingen af lukketider med en og to landingsbaner')

(ax1, ax2), (ax3, ax4) = axs
ax1.hist(over_lukketid[0], bins=20, density=True, color='firebrick', label='2020')
ax1.legend(loc = 'upper left')
ax1.set_title('En landingsbane')

ax2.hist(over_lukketid2[0], bins=20, density=True, color='navy', label='2020')
ax2.legend(loc = 'upper left')
ax2.set_title('To landingsbaner')

ax3.hist(over_lukketid[6], bins=20, density=True, color='forestgreen', label='2026')
ax3.legend(loc = 'upper left')

ax4.hist(over_lukketid2[6], bins=20, density=True, color='darkorange', label='2026')
ax4.legend(loc = 'upper left')

fig.text(0.5, 0.02, 'Lukketid i sekunder', ha='center')
fig.text(0.02, 0.5, 'Tæthed', va='center', rotation='vertical')

plt.savefig('hist_lukketider.png', dpi = 500, bbox_inches = 'tight')