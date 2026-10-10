"""Reference equations of SGIT-TRC. Input arrays are always provided by caller.
No EEG recordings or frozen spatial assets are invented by this module.
"""
from __future__ import annotations
import numpy as np
from scipy.linalg import null_space


def oriented_relation(x: np.ndarray, edges: np.ndarray, eps: float = 1e-12) -> np.ndarray:
    """x: (trials, samples, nodes) in protocol-matched voltage units.
    edges: (edges, 2), zero-based oriented node indices. Output (trials,samples-1,edges).
    """
    x=np.asarray(x, dtype=float); edges=np.asarray(edges,dtype=int)
    if x.ndim != 3 or edges.ndim != 2 or edges.shape[1]!=2:
        raise ValueError('Expected x[trial,time,node], edges[edge,2]')
    a=x[:,:-1,:]; b=x[:,1:,:]
    i,j=edges[:,0],edges[:,1]
    numerator=a[:,:,i]*b[:,:,j]-a[:,:,j]*b[:,:,i]
    norm_i=a[:,:,i]**2+b[:,:,i]**2
    norm_j=a[:,:,j]**2+b[:,:,j]**2
    return numerator/np.sqrt(norm_i*norm_j+eps)


def incidence(n_nodes: int, edges: np.ndarray, triangles: np.ndarray):
    """Construct B1 and B2 with orientation [i,j,k] -> [j,k]-[i,k]+[i,j]."""
    edges=np.asarray(edges,dtype=int); triangles=np.asarray(triangles,dtype=int)
    b1=np.zeros((n_nodes,len(edges)),float)
    lookup={tuple(map(int,e)):n for n,e in enumerate(edges)}
    if len(lookup)!=len(edges): raise ValueError('Repeated edges')
    for e,(i,j) in enumerate(edges):
        if not (0<=i<j<n_nodes): raise ValueError('Edges must be i<j')
        b1[i,e]=-1; b1[j,e]=1
    b2=np.zeros((len(edges),len(triangles)),float)
    for t,(i,j,k) in enumerate(triangles):
        if not i<j<k: raise ValueError('Triangles must be ordered')
        for pair,sgn in (((j,k),1),((i,k),-1),((i,j),1)):
            if pair not in lookup: raise ValueError(f'Missing triangle edge {pair}')
            b2[lookup[pair],t]=sgn
    if not np.allclose(b1@b2,0): raise ValueError('Boundary of boundary fails')
    return b1,b2


def project(edge_flows: np.ndarray, basis: np.ndarray) -> np.ndarray:
    """edge_flows [...,edges], basis [edges, modes]."""
    return np.asarray(edge_flows) @ np.asarray(basis)


def window_states(coefficients: np.ndarray, sample_times_ms: np.ndarray,
                  windows=((80,240),(240,400),(400,560))):
    """coefficients (trials,samples,modes); return Hellinger energy states (trials,windows,modes)."""
    c=np.asarray(coefficients,float); times=np.asarray(sample_times_ms,float)
    if c.ndim!=3 or len(times)!=c.shape[1]: raise ValueError('Time axis mismatch')
    states=[]
    for lo,hi in windows:
        sel=(times>=lo)&(times<hi)
        if not sel.any(): raise ValueError('Window has no samples')
        energy=np.mean(c[:,sel,:]**2,axis=1)
        total=energy.sum(axis=-1,keepdims=True)
        if np.any(total<=0): raise ValueError('Zero total modal energy; apply locked exclusion rule')
        states.append(np.sqrt(energy/total))
    return np.stack(states,axis=1)


def labelblind_standardize(h: np.ndarray) -> np.ndarray:
    """Pooled over all trials; [trials, windows, modes]."""
    h=np.asarray(h,float)
    mu=h.mean(axis=0); sigma=h.std(axis=0,ddof=0)
    if np.any(sigma<=0): raise ValueError('Degenerate coordinate; apply locked exclusion rule')
    return (h-mu)/sigma


def condition_tensors(z: np.ndarray, labels: np.ndarray, positive_label, negative_label):
    """Return (K_pos,K_neg,M) for provided trial labels, with within-condition centering."""
    z=np.asarray(z,float); labels=np.asarray(labels)
    if z.ndim!=3 or z.shape[1]!=3: raise ValueError('Expected [trial,3,modes]')
    if len(labels)!=len(z): raise ValueError('Trial count mismatch')
    def moment(which):
        a=z[labels==which]
        if len(a)<2: raise ValueError('Too few condition trials')
        a=a-a.mean(axis=0,keepdims=True)
        return np.einsum('ra,rb,rc->abc',a[:,0],a[:,1],a[:,2],optimize=True)/len(a)
    kp=moment(positive_label); kn=moment(negative_label)
    return kp,kn,kp-kn


def symmetry_decomposition(m: np.ndarray):
    """Orthogonal SYM, ALT and MIX projections of cubic tensor."""
    import itertools
    m=np.asarray(m,float)
    if m.ndim!=3 or not (m.shape[0]==m.shape[1]==m.shape[2]):
        raise ValueError('Expected equal mode dimension along three axes')
    sym=np.zeros_like(m); alt=np.zeros_like(m)
    for p in itertools.permutations(range(3)):
        inv=sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))
        v=np.transpose(m,p)
        sym+=v/6; alt+=((-1)**inv)*v/6
    return sym,alt,m-sym-alt


def fingerprint(m: np.ndarray) -> np.ndarray:
    """Strict domain: all three sector energies must be positive (no guessed regularizer)."""
    sym,alt,mix=symmetry_decomposition(m)
    d=m.shape[0]; dims=np.array([d*(d+1)*(d+2)/6,d*(d-1)*(d-2)/6,
                                  d**3-d*(d+1)*(d+2)/6-d*(d-1)*(d-2)/6])
    norms=np.array([np.sum(y*y) for y in (sym,alt,mix)])
    if np.any(norms<=0): raise ValueError('Zero symmetry energy; locked stabilizer needed')
    enrichment=(norms/norms.sum())/(dims/d**3)
    return np.log(enrichment[:2]/enrichment[2])

FROZEN_DIRECTION=np.array([0.9987567550,-0.0498492160])

def psi(m_c: np.ndarray,m_g: np.ndarray,direction=FROZEN_DIRECTION) -> float:
    return float(0.5*(fingerprint(m_c)+fingerprint(m_g))@np.asarray(direction))


def pair_preserving_effect(z_c,labels,positive_label,negative_label,
                           basis_sector='C', b=1024, rng=None, z_g=None):
    """Recompute condition moments, and each of three within-condition pair nulls.
    z_c/z_g are label-blind standardized per-trial Hodge state arrays [trial,3,mode].
    This is the manuscript's two-sector Psi endpoint, not the visual LOSO endpoint.
    """
    if z_g is None: raise ValueError('Both frozen CURL and GRAD states required for Psi')
    rng=np.random.default_rng() if rng is None else rng
    labels=np.asarray(labels)
    observed=psi(condition_tensors(z_c,labels,positive_label,negative_label)[2],
                 condition_tensors(z_g,labels,positive_label,negative_label)[2])
    null=np.zeros((3,b))
    for family,displaced_window in enumerate((2,1,0)):
        for draw in range(b):
            permutation=np.arange(len(labels))
            for lab in (positive_label,negative_label):
                ids=np.flatnonzero(labels==lab)
                permutation[ids]=rng.permutation(ids)
            cc=np.array(z_c,copy=True); gg=np.array(z_g,copy=True)
            cc[:,displaced_window,:]=z_c[permutation,displaced_window,:]
            gg[:,displaced_window,:]=z_g[permutation,displaced_window,:]
            mc=condition_tensors(cc,labels,positive_label,negative_label)[2]
            mg=condition_tensors(gg,labels,positive_label,negative_label)[2]
            null[family,draw]=psi(mc,mg)
    return {'psi_observed':observed,'null_scores':null,
            'delta_pp':float(observed-np.max(np.median(null,axis=1)))}


def group_signflip_p(effects: np.ndarray, draws=99999, seed=42, exact_limit=20):
    """One-sided median sign-flip. The exact enumeration follows the conventional +1 correction."""
    effects=np.asarray(effects,float)
    if effects.ndim!=1 or len(effects)==0 or not np.all(np.isfinite(effects)):
        raise ValueError('Invalid effects')
    obs=np.median(effects); rng=np.random.default_rng(seed)
    if len(effects)<=exact_limit:
        from itertools import product
        values=np.array([np.median(effects*np.array(sign)) for sign in product((-1,1),repeat=len(effects))])
        return float(np.mean(values>=obs-1e-14))
    extreme=0
    for _ in range(draws):
        extreme+=np.median(effects*rng.choice((-1,1),size=len(effects))) >= obs
    return float((extreme+1)/(draws+1))
