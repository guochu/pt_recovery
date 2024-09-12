include("recoverL_rb_unitary.jl")
using JSON, Random, Serialization, TensorOperations
using QuantumSpins

const parent_path = "experiment_data/RB_data_20230104/len40/idle100/"

function to_site_mps(mpsj::AbstractArray{<:Number, 3})
	Dl, d, Dr = size(mpsj)
	@tensor tmp[1,4,2,5,3,6] := mpsj[1,2,3] * conj(mpsj[4,5,6])
	return reshape(tmp, (Dl^2, d^2, Dr^2))
end
function to_site_mps_end(mpsj::AbstractArray{<:Number, 3})
	Dl, d, Dr = size(mpsj)
	@tensor tmp[1,4,2,5] := mpsj[1,2,3] * conj(mpsj[4,5,3])
	return reshape(tmp, (Dl^2, d^2, 1))
end

function compute_entropy(x::UnitaryProcessTensor, k::Int)
	mps = MPS([x[i] for i in 1:k])
	println("mps norm is $(norm(mps))")
	trunc = MPSTruncation(ϵ=1.0e-8, D=10000)
	canonicalize!(mps, alg = Orthogonalize(QuantumSpins.SVD(), trunc, normalize=true))
	# println(mps.s[2])
	ents2 = [ _entropy((mps.s[i]).^2) for i in 2:length(mps)] 
	return ents2
end

function compute_osee(x::UnitaryProcessTensor, k::Int)
	data = [x[i] for i in 1:k]
	ndata = [to_site_mps(data[i]) for i in 1:k-1]
	push!(ndata, to_site_mps_end(data[end]))
	mps = MPS(ndata)
	trunc = MPSTruncation(ϵ=1.0e-8, D=10000)
	canonicalize!(mps, alg = Orthogonalize(QuantumSpins.SVD(), trunc, normalize=true))
	return [_entropy( (mps.s[i]).^2 ) / 2 for i in 2:k]	
end

function compute_fidelity(D::Int, gamma::Real)

	mpath = parent_path * "rb_data_$(gamma)"

	data_path = mpath * "/unitaryfidelities_D$(D).json"

	println("read results from path $data_path")

	results = JSON.parsefile(data_path)

	test_data_path = mpath * "/unitaryfidelities_test_D$(D).json"

	println("read results from path $test_data_path")

	test_results = JSON.parsefile(test_data_path)


	return results["fidelities"], test_results["fidelities"]
end

function compute_entropy(D::Int, gamma::Real)

	mpath = parent_path * "rb_data_$(gamma)"
	
	pt_path = mpath * "/unitaryprocesstensor_D$(D).json"

	println("read process tensor from path $pt_path")

	pt_learned, v0 =  Serialization.deserialize(pt_path)

	k = 50

	# entropies = compute_entropy_osee(pt_learned, k)

	entropies = compute_entropy(pt_learned, k)

	return entropies

	# return pt_learned
end

function compute_osee(D::Int, gamma::Real)

	mpath = parent_path * "rb_data_$(gamma)"
	
	pt_path = mpath * "/unitaryprocesstensor_D$(D).json"

	println("read process tensor from path $pt_path")

	pt_learned, v0 =  Serialization.deserialize(pt_path)

	k = 50

	# entropies = compute_entropy_osee(pt_learned, k)

	entropies = compute_osee(pt_learned, k)

	return entropies

	# return pt_learned
end


function compute_all()
	Ds = [1,2,3,4,5,6]
	gammas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.52, 0.54, 0.56, 0.58, 0.6, 0.61, 0.62, 0.63, 0.64]

	fidelities = []
	test_fidelities = []
	entropies = []
	for D in Ds
		fidelities_tmp = []
		test_fidelities_tmp = []
		entropies_tmp = []
		for gamma in gammas
			f, ft = compute_fidelity(D, gamma)
			push!(fidelities_tmp, f)
			push!(test_fidelities_tmp, ft)
			ent = compute_entropy(D, gamma)
			push!(entropies_tmp, ent)
		end
		push!(fidelities, fidelities_tmp)
		push!(test_fidelities, test_fidelities_tmp)
		push!(entropies, entropies_tmp)
	end
	path_name = "result/RB_data_len40_idle100_unitary_results.json"
	results = Dict("fidelities"=>fidelities, "test_fidelities"=>test_fidelities, "entropies"=>entropies, "Ds"=>Ds, "gammas"=>gammas)

	println("save results to path $path_name")
	open(path_name, "w") do f
		write(f, JSON.json(results))
	end
end

function compute_osee_all()
	Ds = [1,2,3,4,5,6]
	gammas = [0.1, 0.2, 0.3, 0.4, 0.5, 0.52, 0.54, 0.56, 0.58, 0.6, 0.61, 0.62, 0.63, 0.64]

	fidelities = []
	test_fidelities = []
	entropies = []
	for D in Ds
		fidelities_tmp = []
		test_fidelities_tmp = []
		entropies_tmp = []
		for gamma in gammas
			f, ft = compute_fidelity(D, gamma)
			push!(fidelities_tmp, f)
			push!(test_fidelities_tmp, ft)
			ent = compute_osee(D, gamma)
			push!(entropies_tmp, ent)
		end
		push!(fidelities, fidelities_tmp)
		push!(test_fidelities, test_fidelities_tmp)
		push!(entropies, entropies_tmp)
	end
	path_name = "result/RB_data_len40_idle100_unitary_osee_results.json"
	results = Dict("fidelities"=>fidelities, "test_fidelities"=>test_fidelities, "entropies"=>entropies, "Ds"=>Ds, "gammas"=>gammas)

	println("save results to path $path_name")
	open(path_name, "w") do f
		write(f, JSON.json(results))
	end
end

