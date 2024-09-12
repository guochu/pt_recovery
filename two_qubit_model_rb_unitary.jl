
include("recoverL_rb_unitary.jl")
using JSON, Random, Serialization

parse_mat(m) = hcat(m...)

function main(D::Int, gamma::Real)

	Random.seed!(13896)

	mpath = "experiment_data/RB_data_20230104/len40/idle100/rb_data_$(gamma)"

	clifford_path = "experiment_data/zhihaodata20220912/withflux/cliffords.json"
	data_path = mpath * "/data.json"

	clifford_data = JSON.parsefile(clifford_path)
	clifford_data_re =parse_mat.(clifford_data["re"])
	clifford_data_im =parse_mat.(clifford_data["im"])

	clifford_gates = [convert(Matrix{ComplexF64}, a + im .* b) for (a, b) in zip(clifford_data_re, clifford_data_im)]

	data = JSON.parsefile(data_path)
	# data = [([item["cl_ops"]...], item["p0"]) for item in data]

	# p_train = 0.8
	# n_train = round(Int, length(data) * p_train)

	# Random.shuffle!(data)

	# train_data = data[1:n_train]
	# test_data = data[n_train+1:end]
	train_data = data["train_data"]
	test_data = data["test_data"]



	results = Dict{String, Any}()

	d = 2
	# D = 2

	LL = d * D

	# function gen_initial_guess()
	# 	pt_path = mpath * "/unitaryprocesstensor_D$(D).json"
	# 	if isfile(pt_path)
	# 		println("read initial pt from path $(pt_path)")
	# 		pt, v0 = Serialization.deserialize(pt_path)
	# 		return v0 + 0.01 .* randn(length(v0))
	# 	else
	# 		println("randomly generate initial guess.")
	# 		return randn(LL^2)
	# 	end
	# end

	gen_initial_guess() = randn(LL^2)

	v0 = gen_initial_guess()

	# v0 = randn(LL^2)
	ρ = zeros(ComplexF64, LL)
	ρ[1] = 1

	println("total number of parameters $(length(v0))")

	println("number of train data $(length(train_data))")
	println("number of test data $(length(test_data))")

	M = [1. 0; 0. 0.]
	v0, ls = recover_pt(ρ, v0, train_data, M, clifford_gates, d, D, 5)

	# U = reshape(Matrix(UnitaryMatrix(v0, LL)), d, D, d, D)
	# pt_learned = UnitaryProcessTensor(U, ρ)

	# println("check the recover precision.")
	# cliffords = clifford_gates
	# losses = []
	# for (inds, p) in test_data
	# 	unitaries = [cliffords[ind+1] for ind in inds]
	# 	rhof = _predict(pt_learned.init_state, pt_learned.U, unitaries)
	# 	p_predicted = dot(rhof, M, rhof)
	# 	# println("predicted is $p_predicted")
	# 	push!(losses, abs2(p - p_predicted))

	# 	println("fidelity for is $(losses[end])")
	# end

	# pt_path = mpath * "/unitaryprocesstensor_D$(D).json"

	# println("save process tensor to path $pt_path")

	# Serialization.serialize(pt_path, (pt_learned, v0))

	# data_path = mpath * "/unitaryfidelities_D$(D).json"

	# println("save results to path $data_path")

	# results = Dict("fidelities"=>losses, "loss_values"=>ls)

	# open(data_path, "w") do f
	# 	write(data_path, JSON.json(results))
	# end

	# return losses
end

# time_per_iterations = [562, 560, 559, 565, 567, 559.7]

function main_all(D::Int)
	# for gamma in [0.1, 0.2, 0.3,0.4,0.5,0.52,0.54,0.56,0.58,0.6,0.61,0.62, 0.63, 0.64]
	# 	main(D, gamma)
	# end

	for gamma in [0.58]
		main(D, gamma)
	end
end
