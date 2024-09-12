using TensorOperations, LinearAlgebra

function random_dm(n)
	rho = randn(ComplexF64, n, n)
	rho = rho' * rho
	rho ./= tr(rho)
	# println(tr(rho))
	return rho
end

# right canonical
function generate_site_mpdo(d, D, R=d^2*D^2)
	L = d * D
	Vs = randn(ComplexF64, L, L * R)
	u, s, v = svd(Vs)
	Vs = reshape(Matrix(v'), d, D, d, D, R) 
	return Vs
end

function compute_cptp(Vs)
	@tensor r[2,7,1,6,3,8,4,9] := Vs[1,2,3,4,5] * conj(Vs[6,7,8,9,5])
	return r
end

function generate_cptp(d, D, R)
	# L = d * D
	# Vs = randn(ComplexF64, L*4, L)
	# u, s, v = svd(Vs)
	# Vs = reshape(Matrix(u), 4,d, D, d, D)
	# @tensor r[1,2,6,7,3,4,8,9] := Vs[5,1,2,3,4] * conj(Vs[5,6,7,8,9])
	Vs = generate_site_mpdo(d, D, R)
	return compute_cptp(Vs)
end


function check_cptp()
	d = 2
	D = 3
	R = 3
	E = generate_cptp(d, D, R)
	rho = permutedims(reshape(random_dm(d*D), d, D, d, D), (2,4,1,3))

	L = d * D * d * D
	rho_out = permutedims(reshape(reshape(rho, 1,L) * reshape(E, L, L), d,d,D,D), (3,1,4,2))
	rho2 = reshape(rho_out, d*D, d*D)
	return tr(rho2), maximum(abs.(rho2 - rho2'))
end

function check_causal()
	d = 2
	D = 3
	R = 5
	E = generate_cptp(d, D, R)
	@tensor r[1,3,2,4] := E[1,2,3,4,5,5,6,6]
	# r = permutedims(r, (1,3,2,4))
	return reshape(r, d*D, d*D) ≈ Matrix(I, d*D, d*D)
end

function eigen_decomp(rhoj; tol::Real=1.0e-10)
	eigvalues, eigvectors = eigen(Hermitian(rhoj))
	# println(eigvalues)
	# println("Hermitian check: $(maximum(abs.(rhoj - rhoj')))")
	pos = 1
	for i in 1:length(eigvalues) 
		if eigvalues[i] >= tol
			pos = i
			break
		end
	end
	pos_required = pos
	# err = (pos == 1) ? 0. : eigvalues[pos-1]
	err = (pos == 1) ? 0. : sum(eigvalues[1:pos-1])
	# println("smallest Schmidt number $(eigvalues[1]), largest $(eigvalues[end])")
	# println("mixed truncation D required: $(length(eigvalues) - pos_required + 1), actual: $(length(eigvalues))->$(length(eigvalues) - pos + 1), error: $err")

	eigvalues_r = eigvalues[pos:end]
	eigvectors_r = eigvectors[:, pos:end]

	eigvalues_r ./= sum(eigvalues_r)

	return eigvalues_r, eigvectors_r * Diagonal(sqrt.(eigvalues_r))
end

struct ProcessTensor
	mpdo::Array{ComplexF64, 5}
	Λ::Array{ComplexF64, 8}
	ρ₀::Array{ComplexF64, 4}
end


function ProcessTensor(mpdo::AbstractArray{<:Number, 5}, env_state::AbstractArray{<:Number, 4})
	# @assert size(env_state, 1) == size(env_state, 2)
	d, D = size(mpdo, 1), size(mpdo, 2)
	((size(env_state, 1) == d) && (size(env_state, 2) == D)) || throw(DimensionMismatch("environment size mismatch."))
	return ProcessTensor(convert(Array{ComplexF64, 5}, mpdo), compute_cptp(mpdo), convert(Array{ComplexF64, 4}, env_state))
end

function ProcessTensor(Λ::AbstractArray{<:Number, 8}, env_state::AbstractArray{<:Number, 4})
	m = permutedims(Λ, (1,3,5,7,2,4,6,8))
	L = prod(size(m)[1:4])
	m2 = reshape(m, L, L)
	eigvalues, eigvectors = eigen_decomp(m2, tol=1.0e-12)
	println("R==============$(length(eigvalues))")
	mpdo = permutedims(reshape(eigvectors, size(m)[1:4]..., length(eigvalues)), (2,1,3,4,5))
	return ProcessTensor(mpdo, Λ, env_state)
end

get_d(x::ProcessTensor) = size(x.mpdo, 1)
get_D(x::ProcessTensor) = size(x.mpdo, 2)
get_R(x::ProcessTensor) = size(x.mpdo, 5)


function Base.getindex(x::ProcessTensor, i::Int)
	(i < 1) && throw(BoundsError("error."))
	if i == 1
		d, D = get_d(x), get_D(x)
		r = permutedims(reshape(x.ρ₀, (d, D, d, D)), (1,3,2,4))
		return r
	else
		return x.Λ
	end
end

function get_site_dm(x::ProcessTensor, i::Int)
	d, D = get_d(x), get_D(x)
	if i == 1
		r = permutedims(reshape(x.ρ₀, (d, D, d, D)), (1,3,2,4))
		return r
	else
		r = permutedims(x.Λ, (1,2,3,5,4,6,7,8))
		return reshape(r, (D,D, d^2, d^2, D,D))
	end
end

# function _update_left(hold, Λ)
# 	@tensor tmp[5,6] := hold[1,2] * Λ[1,2,3,3,4,4,5,6]
# 	return tmp
# end

function partial_dm(x::ProcessTensor, pos_start::Int, pos_end::Int)
	d = get_d(x)
	hold = get_site_dm(x, 1)
	for i in 1:pos_start-1
		# hold = _update_left(hold, x[i])
		xj = get_site_dm(x, i+1) / d
		@tensor tmp[4,5,6,7] := hold[1,1,2,3] * xj[2,3,4,5,6,7]
		hold = tmp
	end
	dm = hold
	for i in pos_start+1:pos_end-1
		xi = get_site_dm(x, i) / d
		@tensor tmp[1,5,2,6,7,8] := dm[1,2,3,4] * xi[3,4,5,6,7,8]
		dm = reshape(tmp, size(tmp,1)*size(tmp,2), size(tmp,3)*size(tmp, 4), size(tmp, 5), size(tmp, 6))
	end
	xi = get_site_dm(x, pos_end) / d
	@tensor tmp[1,5,2,6] := dm[1,2,3,4] * xi[3,4,5,6,7,7] 

	# return reshape(tmp, size(tmp,1)*size(tmp,2), size(tmp,3)*size(tmp,4))
	return reshape(tmp, size(tmp,1)*size(tmp,2), size(tmp,3)*size(tmp, 4))	
end

_fidelity(x::AbstractMatrix, y::AbstractMatrix) = real(tr(sqrt(x) * sqrt(y)))

function _entropy(v::AbstractVector{<:Real}) 
    a = v
    s = sum(a)
    a ./= s
    return -dot(a, log2.(a))
end


