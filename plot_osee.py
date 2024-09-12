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

fontsize = 20
labelsize = 16
linewidth = 3.
markersize = 12
# colors = ['c', 'g', 'b', 'y', 'r', 'k']

colors = ['lightslategrey', 'powderblue', 'steelblue', 'cadetblue', 'darkcyan', 'darkslategray']


markers = ['^', 'o', 'd', 'X', 's', 'p']

alpha = 0.15


data_path = 'result/RB_data_len40_idle100_unitary_osee_results.json'
Ds, gammas, fidelities, test_fidelities, entropies = read_data(data_path)

# print(entropies[-1][3])
print(len(entropies[0][0]))

kselected = 39

entropies_final = [[item[kselected] for item in fj] for fj in entropies]


fig, ax = plt.subplots(1, 1, figsize=(6, 4.5))



for i in range(len(Ds)):
	D = Ds[i]

	ax.plot(gammas, entropies_final[i], ls='--', marker=markers[i], color=colors[i], markersize=markersize, linewidth=linewidth, markerfacecolor='none', label=r'D=%s'%D)


ax.tick_params(axis='both', which='major', labelsize=labelsize)
ax.tick_params(axis='y', which='both')
# ax.locator_params(nbins=6)
ax.locator_params(nbins=6)


ax.set_ylabel(r'$\mathcal{N}^{osee}$', fontsize=fontsize)
ax.set_xlabel(r'$\gamma$', fontsize=fontsize)

ax.legend(loc='upper left', fontsize=labelsize, ncol=2)


plt.tight_layout(pad=0.5)

# plt.savefig('fig2.pdf', dpi=150)

plt.show()

