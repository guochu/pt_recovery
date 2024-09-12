import json
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import rc
from numpy import linspace, asarray

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


# def read_single_data(gamma, D):
# 	mpath = "experiment_data/RB_data_20230104/len40/idle100/rb_data_%s"%(gamma)
# 	data_path = mpath + '/unitaryfidelities_test_60_full_D%s.json'%(D)
# 	with open(data_path, 'r') as f:
# 		data = f.read()
# 	data = json.loads(data)
# 	return process_single_data(data['labels']), process_single_data(data['predicted'])

# def read_all_data(D):
# 	gammas = [0.1, 0.2, 0.3,0.4,0.5,0.52,0.54,0.56,0.58,0.6,0.61,0.62, 0.63, 0.64]
# 	data = []
# 	for gamma in gammas:
# 		data.append(read_single_data(gamma, D))
# 	return asarray(gammas) * 0.4, data

def read_all_data(D):
	data_path = 'result/predict_60_full_data_D%s.json'%(D)
	with open(data_path, 'r') as f:
		data = f.read()
	data = json.loads(data)
	Vbias = data['Vbias']
	data = data['data']
	data = [(process_single_data(item['labels']), process_single_data(item['predicted'])) for item in data]
	return Vbias, data

def process_single_data(data):
	ms = [i for i in range(2, 61)]
	vs = []
	for m in ms:
		vs.append(data[str(m)])
	return asarray(vs)



confidence = 0.95

fontsize = 20
labelsize = 16
linewidth = 1.
markersize = 6
# colors = ['c', 'g', 'b', 'y', 'r', 'k']


fig, ax = plt.subplots(2, 2, figsize=(8, 7))


# fig[0,0]

ax[0,0].annotate(r'(a)', xy=(-0.1, 1.1),xycoords='axes fraction', fontsize=fontsize)


D = 5
gammas, data = read_all_data(D)

print(gammas)

colors = ['c', 'g', 'b', 'y', 'r', 'm', 'tab:orange', 'tab:purple',  'k', 'k', 'k',  'k', 'k', 'k']
# colors = list(mcolors.CSS4_COLORS)


markers = ['^', 'o', 'd', 'X', 's', 'p']

ms = [i for i in range(2, 61)]

fidelities_mean_vs_D = []

for j, i in enumerate(range(0, 8)):
	gamma = round(gammas[i], ndigits=2)
	ax[0,1].plot(ms, data[i][0].mean(axis=1), ls='-', marker='+', color=colors[j], markersize=markersize, linewidth=linewidth, markerfacecolor='none', label=r'$V_{{\rm bias}}=%s$'%(gamma))
	ax[0,1].plot(ms, data[i][1].mean(axis=1), ls='--', marker='^', color=colors[j], markersize=markersize, linewidth=linewidth, markerfacecolor='none')
	# ax[1].fill_between(gammas, lowers, uppers, color=colors[i], alpha=alpha)
	# ax[1].plot(gammas, fidelities_mean_i, ls='--', marker=markers[i], color=color, alpha=alphas[i], markersize=markersize, linewidth=linewidth, markerfacecolor='none', label=r'D=%s'%D)

ax[0,1].tick_params(axis='both', which='major', labelsize=labelsize)
ax[0,1].tick_params(axis='y', which='both')
# ax[1].set_ylim(top= 0.1)

ax[0,1].set_ylabel(r'$\bar{M}$', fontsize=fontsize)
ax[0,1].set_xlabel(r'$m$', fontsize=fontsize)

ax[0,1].set_xlim(left=0)

ax[0,1].annotate(r'(b)', xy=(-0.1, 1.1),xycoords='axes fraction', fontsize=fontsize)
# ax[1].set_title(r'$m=60$', fontsize=labelsize)
ax[0,1].legend(loc='upper center', fontsize=10, ncol=2)






data_path = 'result/RB_data_len40_idle100_unitary_results.json'
Ds, gammas, fidelities, test_fidelities, entropies = read_data(data_path)

# gammas_2 = [0.04129362, 0.04555754, 0.05367807, 0.07306159, 0.13014105,
#        0.15165596, 0.17638084, 0.21222032, 0.27536703, 0.38673703,
#        0.47498861, 0.60513891, 0.80223184, 1.00024648]
# print(gammas)
gammas = asarray(gammas) * 0.4


# fidelities_mean = [[asarray(item).mean() for item in fj] for fj in fidelities]
# fidelities_std = [[asarray(item).std() for item in fj] for fj in fidelities]

# test_fidelities_mean = [[asarray(item).mean() for item in fj] for fj in test_fidelities]
# test_fidelities_std = [[asarray(item).std() for item in fj] for fj in test_fidelities]
fidelities_mean, fidelities_lower, fidelities_upper = process_fidelities(fidelities, confidence)
test_fidelities_mean, test_fidelities_lower, test_fidelities_upper = process_fidelities(test_fidelities, confidence)


entropies_final = [[item[-1] for item in fj] for fj in entropies]



colors = ['lightslategrey', 'powderblue', 'steelblue', 'cadetblue', 'darkcyan', 'darkslategray']

markers = ['^', 'o', 'd', 'X', 's', 'p']
# alphas = [1., 0.8, 0.6, 0.45, 0.3, 0.15]
alphas = [0.15, 0.3, 0.45, 0.6, 0.8, 1.]
color = 'k'

alpha = 0.15

fidelities_mean_vs_D = []

for i in range(len(Ds)):
	D = Ds[i]
	fidelities_mean_i = asarray(fidelities_mean[i])
	# fidelities_std_i = asarray(fidelities_std[i])
	# lowers = fidelities_mean_i - fidelities_std_i
	# uppers = fidelities_mean_i + fidelities_std_i
	fidelities_mean_vs_D.append(fidelities_mean_i)
	lowers = fidelities_lower[i]
	uppers = fidelities_upper[i]
	ax[1,0].semilogy(gammas, fidelities_mean_i, ls='--', marker=markers[i], color=colors[i], markersize=markersize, linewidth=linewidth, markerfacecolor='none', label=r'$\chi=%s$'%D)
	# ax[0].plot(gammas, fidelities_mean_i, ls='--', marker=markers[i], color=color, alpha=alphas[i], markersize=markersize, linewidth=linewidth, markerfacecolor='none', label=r'D=%s'%D)
	# ax[0].fill_between(gammas, lowers, uppers, color=colors[i], alpha=alpha)

ax[1,0].tick_params(axis='both', which='major', labelsize=labelsize)
ax[1,0].tick_params(axis='y', which='both')
ax[1,0].locator_params(axis='x', nbins=8)
# ax[0].set_ylim(top= 0.3)
ax[1,0].set_ylim(top= 0.1)

ax[1,0].set_ylabel(r'$\mathcal{L}$', fontsize=fontsize)
ax[1,0].set_xlabel(r'$V_{{\rm bias}}$', fontsize=fontsize)

ax[1,0].annotate(r'(c)', xy=(-0.1, 1.1),xycoords='axes fraction', fontsize=fontsize)
# ax[0].set_title(r'$m=40$', fontsize=labelsize)

ax[1,0].legend(loc='upper left', fontsize=10, ncol=2)


# fontsize_s = 16
# labelsize_s = 14
# markersize_s = 6


# ax1 = ax[0].inset_axes([0.2, 0.25, 0.45, 0.45])

# # fidelities_mean_vs_D = asarray(fidelities_mean_vs_D)

# # print(fidelities_mean_vs_D.shape)

# # pos = [4, 8, 12]


# start_pos = 6

# for i in range(len(Ds)):
# 	ax1.plot(gammas[start_pos:], fidelities_mean_vs_D[i][start_pos:], ls='--', marker=markers[i], markersize=markersize_s, color=colors[i], linewidth=2, markerfacecolor='none')
# 	# ax1.plot(gammas[start_pos:], fidelities_mean_vs_D[i][start_pos:], ls='--', marker=markers[i], markersize=markersize_s, color=color, alpha=alphas[i], linewidth=2, markerfacecolor='none')


# ax1.tick_params(axis='both', which='major', labelsize=labelsize_s)
# ax1.tick_params(axis='y', which='both')
# ax1.locator_params(nbins=6)

# ax1.set_ylabel(r'$\bar{f}$', fontsize=fontsize_s)


fidelities_mean_vs_D = []

for i in range(len(Ds)):
	D = Ds[i]
	fidelities_mean_i = asarray(test_fidelities_mean[i])
	fidelities_mean_vs_D.append(fidelities_mean_i)
	# fidelities_std_i = asarray(fidelities_std[i])
	# lowers = fidelities_mean_i - fidelities_std_i
	# uppers = fidelities_mean_i + fidelities_std_i
	lowers = fidelities_lower[i]
	uppers = fidelities_upper[i]
	ax[1,1].semilogy(gammas, fidelities_mean_i, ls='--', marker=markers[i], color=colors[i], markersize=markersize, linewidth=linewidth, markerfacecolor='none', label=r'D=%s'%D)
	# ax[1].fill_between(gammas, lowers, uppers, color=colors[i], alpha=alpha)
	# ax[1].plot(gammas, fidelities_mean_i, ls='--', marker=markers[i], color=color, alpha=alphas[i], markersize=markersize, linewidth=linewidth, markerfacecolor='none', label=r'D=%s'%D)

ax[1,1].tick_params(axis='both', which='major', labelsize=labelsize)
ax[1,1].tick_params(axis='y', which='both')
ax[1,1].locator_params(axis='x', nbins=8)
ax[1,1].set_ylim(top= 0.1)

ax[1,1].set_ylabel(r'$\mathcal{L}$', fontsize=fontsize)
ax[1,1].set_xlabel(r'$V_{{\rm bias}}$', fontsize=fontsize)
ax[1,1].annotate(r'(d)', xy=(-0.1, 1.1),xycoords='axes fraction', fontsize=fontsize)
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



plt.tight_layout(pad=0.5)

# plt.savefig('fig1.pdf', dpi=150)

plt.show()




