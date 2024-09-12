import json
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import rc
from numpy import linspace, asarray, sqrt, exp
import numpy as np
# from scipy.optimize import curve_fit
from numpy import polyfit, poly1d

rc('text', usetex=True)


def read_single_data(gamma, D):
	mpath = 'experiment_data/RB_data_20230104/len40/idle100/rb_data_%s'%(gamma)
	data_path = mpath + "/unitaryfidelities_D%s.json"%(D)
	with open(data_path, 'r') as f:
		data = f.read()
		data = json.loads(data)

	return data['loss_values']


fontsize = 22
labelsize = 20
linewidth = 2.
markersize = 6
# colors = ['c', 'g', 'b', 'y', 'r', 'k']

colors = ['lightslategrey', 'powderblue', 'steelblue', 'cadetblue', 'darkcyan', 'darkslategray']


markers = ['^', 'o', 'd', 'X', 's', 'p']




gammas = [0.1, 0.2, 0.3,0.4,0.5,0.52,0.54,0.56,0.58,0.6,0.61,0.62, 0.63, 0.64]
Ds = [1,2,3,4,5,6]


gamma1 = gammas[0]
gamma2 = gammas[8]

fig, ax = plt.subplots(1, 2, figsize=(8, 3.5))


for i, D in enumerate(Ds):
	losses = read_single_data(gamma1, D)

	ax[0].semilogy(losses, ls='--', color=colors[i], markersize=markersize, linewidth=linewidth, markerfacecolor='none', label=r'$\chi=%s$'%D)

ax[0].tick_params(axis='both', which='major', labelsize=labelsize)
ax[0].tick_params(axis='y', which='both')
# ax[0].locator_params(nbins=6)


ax[0].set_ylabel(r'$\mathcal{L}$', fontsize=fontsize)
ax[0].set_xlabel(r'iterations', fontsize=fontsize)
ax[0].annotate(r'(a)', xy=(-0.15, 1.05),xycoords='axes fraction', fontsize=fontsize)
ax[0].set_title(r'$V_{\rm bias} = %s$'%(round(gamma1 * 0.4, ndigits=2)), fontsize=fontsize)
ax[0].legend(fontsize=12)




for i, D in enumerate(Ds):
	losses = read_single_data(gamma2, D)

	ax[1].semilogy(losses, ls='--', color=colors[i], markersize=markersize, linewidth=linewidth, markerfacecolor='none', label=r'$\chi=%s$'%D)

ax[1].tick_params(axis='both', which='major', labelsize=labelsize)
ax[1].tick_params(axis='y', which='both')
# ax[0].locator_params(nbins=6)


ax[1].set_ylabel(r'$\mathcal{L}$', fontsize=fontsize)
ax[1].set_xlabel(r'iterations', fontsize=fontsize)
ax[1].annotate(r'(b)', xy=(-0.15, 1.05),xycoords='axes fraction', fontsize=fontsize)
ax[1].set_title(r'$V_{\rm bias} = %s$'%(round(gamma2 * 0.4, ndigits=4)), fontsize=fontsize)
# ax[1].legend(fontsize=12)




plt.tight_layout(pad=0.5)

plt.savefig('fig3.pdf', dpi=150)

plt.show()
