import json
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import rc
from numpy import linspace, asarray, sqrt, exp
import numpy as np
# from scipy.optimize import curve_fit
from numpy import polyfit, poly1d

rc('text', usetex=True)


def read_data(data_path):
	with open(data_path, 'r') as f:
		data = f.read()
	data = json.loads(data)
	return data['Ds'], data['gammas'], data['fidelities'], data['test_fidelities'], data['entropies']

def find_single_errors(a, confidence):
    a = sorted(a.reshape(a.size))
    L = len(a)
    m = a[L//2]
    p = (1-confidence) / 2
    s1 = int(L * p)
    s2 = int(L * (1-p))
    return m, a[s1], a[s2]

def process_fidelities(fidelities, confidence):
	fidelities_mean = []
	fidelities_lower = []
	fidelities_upper = []
	for fj in fidelities:
		fidelities_mean_tmp = []
		fidelities_lower_tmp = []
		fidelities_upper_tmp = []
		for item in fj:
			m, b, c = find_single_errors(asarray(item), confidence)
			fidelities_mean_tmp.append(m)
			fidelities_lower_tmp.append(b)
			fidelities_upper_tmp.append(c)

		fidelities_mean.append(fidelities_mean_tmp)
		fidelities_lower.append(fidelities_lower_tmp)
		fidelities_upper.append(fidelities_upper_tmp)
		
	return fidelities_mean, fidelities_lower, fidelities_upper

confidence = 0.95

fontsize = 24
annotation_size = 26
labelsize = 20
legendsize = 16
linewidth = 2.
markersize = 10
# colors = ['c', 'g', 'b', 'y', 'r', 'k']

colors = ['lightslategrey', 'powderblue', 'steelblue', 'cadetblue', 'darkcyan', 'darkslategray']


markers = ['^', 'o', 'd', 'X', 's', 'p']

alpha = 0.15


data_path = 'result/RB_data_len40_idle100_unitary_results.json'
Ds, gammas, fidelities, test_fidelities, entropies = read_data(data_path)

gammas = asarray(gammas) * 0.4

kselected = 39

entropies_final = [[item[kselected] for item in fj] for fj in entropies]


fig, ax = plt.subplots(2, 2, figsize=(8, 7.5))



for i in range(len(Ds)):
	D = Ds[i]

	ax[0,0].plot(gammas, entropies_final[i], ls='--', marker=markers[i], color=colors[i], markersize=markersize, linewidth=linewidth, markerfacecolor='none', label=r'$\chi=%s$'%D)
ax[0,0].tick_params(axis='both', which='major', labelsize=labelsize)
ax[0,0].tick_params(axis='y', which='both')
# ax.locator_params(nbins=6)
ax[0,0].locator_params(nbins=6)


ax[0,0].set_ylabel(r'$\mathcal{M}_j$', fontsize=fontsize)
ax[0,0].set_xlabel(r'$V_{bias} (V)$', fontsize=fontsize)
ax[0,0].annotate(r'(a)', xy=(-0.27, 1.02),xycoords='axes fraction', fontsize=annotation_size)

# ax[0].legend(loc='upper left', fontsize=14, ncol=2)


data_path = 'result/RB_data_len40_idle100_unitary_osee_results.json'
Ds, gammas, fidelities, test_fidelities, entropies = read_data(data_path)

gammas = asarray(gammas) * 0.4

entropies_final = [[item[kselected] for item in fj] for fj in entropies]

for i in range(len(Ds)):
	D = Ds[i]
	ax[0,1].plot(gammas, entropies_final[i], ls='--', marker=markers[i], color=colors[i], markersize=markersize, linewidth=linewidth, markerfacecolor='none', label=r'$\chi=%s$'%D)


ax[0,1].tick_params(axis='both', which='major', labelsize=labelsize)
ax[0,1].tick_params(axis='y', which='both')
# ax.locator_params(nbins=6)
ax[0,1].locator_params(nbins=6)


ax[0,1].set_ylabel(r'$\mathcal{N}_j$', fontsize=fontsize)
ax[0,1].set_xlabel(r'$V_{bias} (V)$', fontsize=fontsize)
ax[0,1].annotate(r'(b)', xy=(-0.27, 1.02),xycoords='axes fraction', fontsize=annotation_size)


ax[0,1].legend(loc='upper left', fontsize=legendsize, ncol=1)

colors = ['darkred', 'red', 'tomato', 'lightcoral', 'mistyrose']


cor_mat = np.load('result/cor_mat_D4_gamma0.1.npy')
NSTEPS = 59

delta_2 = [cor_mat[i+1,i] for i in range(NSTEPS - 2)]
delta_3 = [cor_mat[i+2,i] for i in range(NSTEPS - 3)]
delta_4 = [cor_mat[i+3,i] for i in range(NSTEPS - 4)]
delta_5 = [cor_mat[i+4,i] for i in range(NSTEPS - 5)]

# ax[1,0].plot(cor_mat.T[0][1:])
ax[1,0].plot(range(len(cor_mat.T[0][1:])), cor_mat.T[0][1:], label=r'$\mathcal{I}(1, i)$', linewidth=linewidth, color=colors[0], ls='-')

ax[1,0].plot(delta_2,label = r'$\mathcal{I}(i, i+1)$', linewidth=linewidth, color=colors[1], ls='--')
ax[1,0].plot(delta_3,label = r'$\mathcal{I}(i, i+2)$', linewidth=linewidth, color=colors[2], ls='--')
ax[1,0].plot(delta_4,label = r'$\mathcal{I}(i, i+3)$', linewidth=linewidth, color=colors[3], ls='--')
ax[1,0].plot(delta_5,label = r'$\mathcal{I}(i, i+4)$', linewidth=linewidth, color=colors[4], ls='--')

ax[1,0].tick_params(axis='both', which='major', labelsize=labelsize)
ax[1,0].tick_params(axis='y', which='both')
ax[1,0].locator_params(nbins=7)
ax[1,0].legend(loc='upper left', fontsize=legendsize)

ax[1,0].set_ylabel(r'Mutual information', fontsize=fontsize)
ax[1,0].set_xlabel(r'$k$', fontsize=fontsize)
ax[1,0].annotate(r'(c)', xy=(-0.27, 1.05),xycoords='axes fraction', fontsize=annotation_size)
ax[1,0].set_title(r'$V_{bias}=0.04$', fontsize=fontsize)


cor_mat = np.load('result/cor_mat_D4_gamma0.58.npy')
NSTEPS = 59

delta_2 = [cor_mat[i+1,i] for i in range(NSTEPS - 2)]
delta_3 = [cor_mat[i+2,i] for i in range(NSTEPS - 3)]
delta_4 = [cor_mat[i+3,i] for i in range(NSTEPS - 4)]
delta_5 = [cor_mat[i+4,i] for i in range(NSTEPS - 5)]

# ax[1,1].plot(cor_mat.T[0][1:])
ax[1,1].plot(range(len(cor_mat.T[0][1:])), cor_mat.T[0][1:], label=r'$\mathcal{E}_i - \mathcal{E}_1$', linewidth=linewidth, color=colors[0], ls='-')

ax[1,1].plot(delta_2,label = r'$\mathcal{I}(i, i+1)$', linewidth=linewidth, color=colors[1], ls='--')
ax[1,1].plot(delta_3,label = r'$\mathcal{E}_{i+2} - \mathcal{E}_i$', linewidth=linewidth, color=colors[2], ls='--')
ax[1,1].plot(delta_4,label = r'$\mathcal{E}_{i+3} - \mathcal{E}_i$', linewidth=linewidth, color=colors[3], ls='--')
ax[1,1].plot(delta_5,label = r'$\mathcal{E}_{i+4} - \mathcal{E}_i$', linewidth=linewidth, color=colors[4], ls='--')

ax[1,1].set_ylim(top=1)
ax[1,1].tick_params(axis='both', which='major', labelsize=labelsize)
ax[1,1].tick_params(axis='y', which='both')
ax[1,1].locator_params(nbins=8)


ax[1,1].set_ylabel(r'Mutual information', fontsize=fontsize)
ax[1,1].set_xlabel(r'$k$', fontsize=fontsize)
ax[1,1].annotate(r'(d)', xy=(-0.27, 1.05),xycoords='axes fraction', fontsize=annotation_size)
ax[1,1].set_title(r'$V_{bias}=0.232$', fontsize=fontsize)

# ax[1,1].grid(ls='--')


plt.tight_layout(pad=1)

plt.savefig('fig2.pdf', dpi=150)


plt.show()

