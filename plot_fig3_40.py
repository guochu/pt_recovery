import json
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import rc
from numpy import linspace, asarray
import matplotlib.colors as mcolors

rc('text', usetex=True)


def read_single_data(gamma, D):
	mpath = "experiment_data/RB_data_20230104/len40/idle100/rb_data_%s"%(gamma)
	data_path = mpath + '/unitaryfidelities_test_40_full_D%s.json'%(D)
	with open(data_path, 'r') as f:
		data = f.read()
	data = json.loads(data)
	return process_single_data(data['labels']), process_single_data(data['predicted'])

def read_all_data(D):
	gammas = [0.1, 0.2, 0.3,0.4,0.5,0.52,0.54,0.56,0.58,0.6,0.61,0.62, 0.63, 0.64]
	data = []
	for gamma in gammas:
		data.append(read_single_data(gamma, D))
	return asarray(gammas) * 0.4, data

def process_single_data(data):
	ms = [i for i in range(2, 41)]
	vs = []
	for m in ms:
		vs.append(data[str(m)])
	return asarray(vs)

gammas, data = read_all_data(6)

# confidence = 0.95

fontsize = 20
labelsize = 16
linewidth = 1.
markersize = 6
# colors = ['c', 'g', 'b', 'y', 'r', 'm', 'k', 'k',  'k', 'k', 'k',  'k', 'k', 'k']
colors = list(mcolors.CSS4_COLORS)


markers = ['^', 'o', 'd', 'X', 's', 'p']


ms = [i for i in range(2, 41)]

print(len(gammas))

fig, ax = plt.subplots(1, 1, figsize=(6, 5))

fidelities_mean_vs_D = []

for j, i in enumerate(range(8)):
	gamma = gammas[i]
	ax.plot(ms, data[i][0].mean(axis=1), ls='-', marker='o', color=colors[j], markersize=markersize, linewidth=linewidth, markerfacecolor='none', label=r'$\gamma=%s$'%(gamma))
	ax.plot(ms, data[i][1].mean(axis=1), ls='--', marker='+', color=colors[j], markersize=markersize, linewidth=linewidth, markerfacecolor='none')
	# ax[1].fill_between(gammas, lowers, uppers, color=colors[i], alpha=alpha)
	# ax[1].plot(gammas, fidelities_mean_i, ls='--', marker=markers[i], color=color, alpha=alphas[i], markersize=markersize, linewidth=linewidth, markerfacecolor='none', label=r'D=%s'%D)

ax.tick_params(axis='both', which='major', labelsize=labelsize)
ax.tick_params(axis='y', which='both')
# ax[1].set_ylim(top= 0.1)

ax.set_ylabel(r'$\bar{M}$', fontsize=fontsize)
ax.set_xlabel(r'$m$', fontsize=fontsize)

# ax[1].set_title(r'$m=60$', fontsize=labelsize)
# ax[1].legend(loc='upper left', fontsize=labelsize)


# ax1 = ax[1].inset_axes([0.2, 0.25, 0.45, 0.45])

# start_pos = 6

# for i in range(len(Ds)):
# 	ax1.plot(gammas[start_pos:], fidelities_mean_vs_D[i][start_pos:], ls='--', marker=markers[i], markersize=markersize_s, color=colors[i], linewidth=2, markerfacecolor='none')
# 	# ax1.plot(gammas[start_pos:], fidelities_mean_vs_D[i][start_pos:], ls='--', marker=markers[i], markersize=markersize_s, color=color, alpha=alphas[i], linewidth=2, markerfacecolor='none')


# ax1.tick_params(axis='both', which='major', labelsize=labelsize_s)
# ax1.tick_params(axis='y', which='both')
# ax1.locator_params(nbins=6)

# ax1.set_ylabel(r'$\bar{f}$', fontsize=fontsize_s)

# ax.legend(fontsize=labelsize)


plt.tight_layout(pad=0.5)

# plt.savefig('fig1.pdf', dpi=150)

plt.show()



