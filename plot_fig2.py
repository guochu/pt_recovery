import json
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import rc
from numpy import linspace, asarray, sqrt, exp
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

fontsize = 22
labelsize = 20
linewidth = 3.
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


fig, ax = plt.subplots(1, 2, figsize=(8, 4))



for i in range(len(Ds)):
	D = Ds[i]

	ax[0].plot(gammas, entropies_final[i], ls='--', marker=markers[i], color=colors[i], markersize=markersize, linewidth=linewidth, markerfacecolor='none', label=r'$\chi=%s$'%D)
ax[0].tick_params(axis='both', which='major', labelsize=labelsize)
ax[0].tick_params(axis='y', which='both')
# ax.locator_params(nbins=6)
ax[0].locator_params(nbins=6)


ax[0].set_ylabel(r'$\mathcal{M}_j$', fontsize=fontsize)
ax[0].set_xlabel(r'$V_{bias}$', fontsize=fontsize)
ax[0].annotate(r'(a)', xy=(0.05, 0.9),xycoords='axes fraction', fontsize=fontsize)

# ax[0].legend(loc='upper left', fontsize=14, ncol=2)


data_path = 'result/RB_data_len40_idle100_unitary_osee_results.json'
Ds, gammas, fidelities, test_fidelities, entropies = read_data(data_path)

gammas = asarray(gammas) * 0.4

entropies_final = [[item[kselected] for item in fj] for fj in entropies]

for i in range(len(Ds)):
	D = Ds[i]
	ax[1].plot(gammas, entropies_final[i], ls='--', marker=markers[i], color=colors[i], markersize=markersize, linewidth=linewidth, markerfacecolor='none', label=r'$\chi=%s$'%D)


ax[1].tick_params(axis='both', which='major', labelsize=labelsize)
ax[1].tick_params(axis='y', which='both')
# ax.locator_params(nbins=6)
ax[1].locator_params(nbins=6)


ax[1].set_ylabel(r'$\mathcal{N}^{osee}_j$', fontsize=fontsize)
ax[1].set_xlabel(r'$V_{bias}$', fontsize=fontsize)
ax[1].annotate(r'(b)', xy=(0.05, 0.9),xycoords='axes fraction', fontsize=fontsize)


ax[1].legend(loc='center left', fontsize=12, ncol=2)

plt.tight_layout(pad=0.5)

# plt.savefig('fig2.pdf', dpi=150)

plt.show()

