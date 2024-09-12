
using JSON, Random


function main(p_train::Real, gamma::Real)


	mpath = "experiment_data/RB_data_20230104/len60/idle100/rb_data_$(gamma)"

	data_path = mpath * "/standard_rb_1q_full_data.json"

	data = JSON.parsefile(data_path)
	data = [([item["cl_ops"]...], item["p0"]) for item in data]


	rb_data = Dict{Int, Vector{Any}}()
	for (k, v) in data
		L = length(k)
		if !haskey(rb_data, L)
			rb_data[L] = []
		end
		push!(rb_data[L], (k, v))
	end
	counts = Dict(k=>length(v) for (k, v) in rb_data)
	println("data counts ", counts)
	println("total number of data ", sum(values(counts)))
	println(sort([keys(counts)...]))
	error("stop here...")

	ks = sort([keys(rb_data)...])
	all_data = [rb_data[x] for x in ks]

	train_data = []
	test_data = []

	for item in all_data
		L = length(item)
		n_train = round(Int, L * p_train)
		Random.shuffle!(item)
		push!(train_data, item[1:n_train])
		push!(test_data, item[n_train+1:end])
	end

	file_path = mpath * "/data.json"

	open(file_path, "w") do f
		write(f, JSON.json(Dict("train_data"=>vcat(train_data...), "test_data"=>vcat(test_data...))))
	end


	# return vs
end


function main_all()
	for gamma in [0.1, 0.2, 0.3, 0.4, 0.5, 0.52, 0.54, 0.56, 0.58, 0.6, 0.61, 0.62, 0.63, 0.64]
		main(0.6, gamma)
	end
end