using UnitaryMatrices

include("contract.jl")
include("unitary_process_tensor.jl")

using Optim
using JSON
using Zygote


function _predict(init_state, U, unitaries::Vector)
	k = length(unitaries)
	d, D = size(U, 1), size(U, 2)
	state2 = reshape(init_state, d, D)
	state = contract(U, state2, ((1,2), (1,2)))
	for i in 1:k
		state2 = contract(unitaries[i], state, ((2,), (1,)))
		state = contract(U, state2, ((1,2), (1,2)))
	end
	return state 
end

function read_basis(nbasis::Int)
	paras = JSON.parsefile("fig1data/basis$(nbasis).json")
	# println(paras)
	return [unitary_mat(paras[i]...) for i in 1:nbasis]
end

unitary_mat(lamba::Real, theta::Real, phi::Real) = [cos(theta/2) -exp(im * lamba) * sin(theta/2); exp(im * phi) * sin(theta/2) exp(im * (lamba + phi)) * cos(theta/2)]



_predict_u(ρ₀, Λ, inds, cliffords) = _predict(ρ₀, Λ, [cliffords[ind+1] for ind in inds])

Zygote.@adjoint _predict_u(ρ₀, Λ, inds, cliffords) = begin
	unitaries = [cliffords[ind+1] for ind in inds]
	r, back = Zygote.pullback(_predict, ρ₀, Λ, unitaries)
	return r, z -> begin
		a, b, c = back(z)
		return nothing, b, nothing, nothing
	end
end

function recover_pt_util(init_state::Vector{ComplexF64}, U::AbstractArray{<:Real}, all_unitaries::Vector, M::AbstractMatrix, cliffords_gates::Vector, d::Int, D::Int)

	cliffords = cliffords_gates

	LL = d*D

	loss(v) = begin
		ansatz = Matrix(UnitaryMatrix(v, LL))
		ansatz = reshape(ansatz, d, D, d, D)


		r = 0.
		for (inds, p) in all_unitaries
			# unitaries = [cliffords[ind+1] for ind in inds]
			# rhof = _predict(ρ, ansatz, unitaries)
			rhof = _predict_u(init_state, ansatz, inds, cliffords)
			p_predicted = dot(rhof, M, rhof)

			r += abs2(p_predicted - p)
		end

		return r / length(all_unitaries)
	end
	g!(storage, x) = begin
		grad = gradient(loss, x)
		storage .= grad[1]
	end

	# x0 = U
 #    println("initial loss is $(loss(x0))")

	x0 = U
	_loss = loss(x0)
	for i in 1:50
		x_tmp = randn(length(x0))
		_loss_tmp = loss(x_tmp)
		if _loss_tmp < _loss
			_loss = _loss_tmp
			x0 = x_tmp
		end
	end

	println("initial loss is $(_loss)")

    # grad = gradient(loss, x0)


    # println("ideal loss loss is $(loss(reshape(mpdo, length(mpdo))))")
    results = Optim.optimize(loss, g!, x0, BFGS(), Optim.Options(g_tol=1e-10, iterations=200,
        store_trace=true, show_trace=true))

    x_opt, ls = Optim.minimizer(results), Optim.minimum(results)

    f_values = Optim.f_trace(results)

    println("Optim used $(Optim.iterations(results)) to converge.")
    println("final loss is $(ls).")

    # return reshape(scale .* unitary_mat(d*D, x_opt[1:L1]), (d, D, d, D) )
    return x_opt, f_values
end

function recover_pt(init_state::Vector{ComplexF64}, U::AbstractArray{<:Real}, all_unitaries::Vector, M::AbstractMatrix, cliffords_gates::Vector, d::Int, D::Int, ntrials::Int=3)
	x_opt = [] 
	f_values = []
	losses = Float64[]
	for i in 1:ntrials
		x_opt_j, f_values_j = recover_pt_util(init_state, randn(length(U)), all_unitaries, M, cliffords_gates, d, D)
		push!(x_opt, x_opt_j)
		push!(f_values, f_values_j)
		push!(losses, f_values_j[end])
	end
	println("all losses $(losses)")
	ls_pos = argmin(losses)
	return x_opt[ls_pos], f_values[ls_pos]
end

