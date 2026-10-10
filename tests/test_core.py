import numpy as np
from sgit import incidence, oriented_relation, symmetry_decomposition, fingerprint, FROZEN_DIRECTION

def test_boundary_squared_zero():
    b1,b2=incidence(3,np.array([[0,1],[0,2],[1,2]]),np.array([[0,1,2]]))
    assert np.allclose(b1@b2,0)
    assert b2[:,0].tolist()==[1,-1,1]

def test_antisy():
    x=np.array([[[1.,2.],[3.,5.],[2.,6.]]])
    a=oriented_relation(x,np.array([[0,1]]))
    b=oriented_relation(x,np.array([[1,0]]))
    assert np.allclose(a,-b)

def test_symmetry_orthogonality():
    m=np.arange(64,dtype=float).reshape(4,4,4)**1.3
    a,b,c=symmetry_decomposition(m)
    assert np.allclose(a+b+c,m)
    assert abs(np.sum(a*b))<1e-8
    assert abs(np.sum(a*c))<1e-8
    assert abs(np.sum(b*c))<1e-8

def test_fingerprint_permutation_and_sign():
    rng=np.random.default_rng(123)
    m=rng.normal(size=(12,12,12))
    assert np.allclose(fingerprint(m),fingerprint(m.transpose(2,0,1)))
    assert np.allclose(fingerprint(m),fingerprint(-m))

def test_direction():
    assert abs(np.linalg.norm(FROZEN_DIRECTION)-1)<1e-7
