using Zygote
using Zygote: @adjoint
import LinearAlgebra: tr

shape(m::AbstractArray) = size(m)
shape(m::AbstractArray, j::Int) = size(m, j)

# export move_selected_index_forward, move_selected_index_backward

"""	
	move_selected_index_forward(a, I)
	move the indexes specified by I to the front of a
	# Arguments
	@ a::NTuple{N, Int}: the input tensor.
	@ I: tuple or vector of integer.
"""
function move_selected_index_forward(a::Vector{T}, I) where {T}
    na = length(a)
    nI = length(I)
    b = Vector{T}(undef, na)
    k1 = 0
    k2 = nI
    for i=1:na
        s = 0
        while s != nI
        	if i == I[s+1]
        		b[s+1] = a[k1+1]
        	    k1 += 1
        	    break
        	end
        	s += 1
        end
        if s == nI
        	b[k2+1]=a[k1+1]
        	k1 += 1
            k2 += 1
        end
    end
    return b
end

function move_selected_index_forward(a::NTuple{N, T}, I) where {N, T}
    return NTuple{N, T}(move_selected_index_forward([a...], I))
end

"""	
	move_selected_index_backward(a, I)
	move the indexes specified by I to the back of a
	# Arguments
	@ a::NTuple{N, Int}: the input tensor.
	@ I: tuple or vector of integer.
"""
function move_selected_index_backward(a::Vector{T}, I) where {T}
	na = length(a)
	nI = length(I)
	nr = na - nI
	b = Vector{T}(undef, na)
	k1 = 0
	k2 = 0
	for i = 1:na
	    s = 0
	    while s != nI
	    	if i == I[s+1]
	    		b[nr+s+1] = a[k1+1]
	    		k1 += 1
	    		break
	    	end
	    	s += 1
	    end
	    if s == nI
	        b[k2+1] = a[k1+1]
	        k2 += 1
	        k1 += 1
	    end
	end
	return b
end

function move_selected_index_backward(a::NTuple{N, T}, I) where {N, T}
	return NTuple{N, T}(move_selected_index_backward([a...], I))
end

permute(m::AbstractArray, perm) = PermutedDimsArray(m, perm)

function _group_extent(extent::NTuple{N, Int}, idx::NTuple{N1, Int}) where {N, N1}
    ext = Vector{Int}(undef, N1)
    l = 0
    for i=1:N1
        ext[i] = prod(extent[(l+1):(l+idx[i])])
        l += idx[i]
    end
    return NTuple{N1, Int}(ext)
end


function tie(a::AbstractArray{T, N}, axs::NTuple{N1, Int}) where {T, N, N1}
    (sum(axs) != N) && error("total number of axes should equal to tensor rank.")
    return reshape(a, _group_extent(shape(a), axs))
end

function contract(a::AbstractArray{Ta, Na}, b::AbstractArray{Tb, Nb}, axs::Tuple{NTuple{N, Int}, NTuple{N, Int}}) where {Ta, Na, Tb, Nb, N}
    ia, ib = axs
    seqindex_a = move_selected_index_backward(collect(1:Na), ia)
    seqindex_b = move_selected_index_forward(collect(1:Nb), ib)
    ap = permute(a, seqindex_a)
    bp = permute(b, seqindex_b)
    return reshape(tie(ap, (Na-N, N)) * tie(bp, (N, Nb-N)), shape(ap)[1:(Na-N)]..., shape(bp)[(N+1):Nb]...)
end

function tr(a::AbstractArray, i::Int, j::Int)
    (i == j) && error("trace dimensions can not be the same.")
    (i >= 1 && i <= ndims(a)) || error("dim $i out of bound.")
    (j >= 1 && j <= ndims(a)) || error("dim $j out of bound.")
    (shape(a, i)==shape(a, j)) || error("dim $i and $j size mismatch.")
    (ndims(a) == 2) && return tr(a)
    ranges = Any[1:shape(a, l) for l in 1:ndims(a)]
    rest_sizes = [shape(a, l) for l in 1:ndims(a) if ((l != i) && (l != j))]
    r = zeros(eltype(a), rest_sizes...)
    for l in 1:size(a, i)
        ranges[i] = l
        ranges[j] = l
        r .+= view(a, ranges...)
    end
    return r
end

@adjoint tr(a::AbstractArray, i::Int, j::Int) = begin
    (i == j) && error("trace dimensions can not be the same.")
    (i >= 1 && i <= ndims(a)) || error("dim $i out of bound.")
    (j >= 1 && j <= ndims(a)) || error("dim $j out of bound.")
    (shape(a, i)==shape(a, j)) || error("dim $i and $j size mismatch.")
    if ndims(a) == 2
        r, back = Zygote.pullback(tr, a)
        return r, z -> (back(z)[1], nothing, nothing)
    end
    ranges = Any[1:shape(a, l) for l in 1:ndims(a)]
    rest_sizes = [shape(a, l) for l in 1:ndims(a) if ((l != i) && (l != j))]
    r = zeros(eltype(a), rest_sizes...)
    for l in 1:size(a, i)
        ranges[i] = l
        ranges[j] = l
        r .+= view(a, ranges...)
    end
    return r, z -> begin
        br = zeros(promote_type(eltype(z), eltype(a)), shape(a))
        for l in 1:size(a, i)
        	ranges[i] = l
        	ranges[j] = l           
        	br[ranges...] = z
        end
        return br, nothing, nothing
    end
end

@adjoint tie(a::AbstractArray{T, N}, axs::NTuple{N1, Int}) where {T, N, N1} = tie(a, axs), z -> (reshape(z, shape(a)), nothing)

@adjoint contract(a::AbstractArray{Ta, Na}, b::AbstractArray{Tb, Nb}, axs::Tuple{NTuple{N, Int}, NTuple{N, Int}}) where {Ta, Na, Tb, Nb, N} = begin
	ia, ib = axs
	seqindex_a = move_selected_index_backward(collect(1:Na), ia)
	seqindex_b = move_selected_index_forward(collect(1:Nb), ib)
	ap, ap_back = Zygote.pullback(permute, a, seqindex_a)
	bp, bp_back = Zygote.pullback(permute, b, seqindex_b)
	am = tie(ap, (Na-N, N))
	bm = tie(bp, (N, Nb-N))
	c, c_back = Zygote.pullback(*, am, bm)
	r = reshape(c, shape(ap)[1:(Na-N)]..., shape(bp)[(N+1):Nb]...)
	return r, z -> begin
	    c_v = reshape(z, shape(c))
	    am_v, bm_v = c_back(c_v)
	    r1 = ap_back(reshape(am_v, shape(ap)...))[1]
	    r2 = bp_back(reshape(bm_v, shape(bp)...))[1]
	    return (r1, r2, nothing)
	end
end
