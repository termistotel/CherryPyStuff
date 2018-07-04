import numpy as np

def testLinez(a):
    m,n = a.shape

    # Testiraj trivialno
    if m<n:
        return False,a

    for i in range(n):
        if np.all(a[:,i] == 0):
            return False,a

    for i in range(n):
        a[:,i] = a[:,i]/a[i,i]
        for j in range(i+1, n):
            a[:,j] = a[:,j] - a[:,i]*a[i,j]
            print(a)
            if np.all(a[:,j]==0):
                return False,a

    for i in reversed(range(n)):
        for j in reversed(range(i)):
            a[:,j] = a[:,j] - a[:,j]*a[j,i]
            print(a)

    return True,a

def dictToMatrix(dict):
    a = list(dict.items())
    a.sort(key=(lambda x: x[0]))

    try:
        tmp = np.array(list(map(lambda x: list(map(float, x[1])), a)))
    except:
        tmp = "Nije validan unos"

    return tmp

def svdecomposition(mat):
    n,m = mat.shape
    manja = min(n,m)

    # sig1, U = np.linalg.eig(mat.dot(mat.T))
    # sig2, V = np.linalg.eig(mat.T.dot(mat))

    # array1 = np.argsort(sig1)[::-1]
    # array2 = np.argsort(sig2)[::-1]

    # sig1, U = sig1[array1], U[:,array1]
    # sig2, V = sig2[array2], V[:,array2]

    # sigma = np.zeros(shape=mat.shape)
    # sigma[:manja, :manja] = np.sqrt(np.diag(sig1)[:manja, :manja])
    
    # # Fixanje negativnih
    # krive = np.diagonal(mat.dot(V).T.dot(U.dot(sigma))) < 0
    # V[:,krive] *= -1

    U, sigma, V = np.linalg.svd(mat)

    V = V.T

    # print(mat.shape)
    # print(U.shape, sigma.shape, V.shape)
    # print(sigma[:10])

    return U, sigma, V