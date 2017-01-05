# testDriver.py
from scipy import linalg as la
import numpy as np
from matplotlib import pyplot as plt

# Problem 1
def truncated_svd(A,r=None,tol=10**-6):
    """Computes the truncated SVD of A. If r is None or equals the number
        of nonzero singular values, it is the compact SVD.
    Parameters:
        A: the matrix
        r: the number of singular values to use
        tol: the tolerance for zero
    Returns:
        U - the matrix U in the SVD
        s - the diagonals of Sigma in the SVD
        Vh - the matrix V^H in the SVD
    """
    m,n = A.shape
    eigs,evecs = la.eig(A.conj().T.dot(A))

    s = np.sqrt(eigs)
    sort_indices = np.argsort(s)[::-1]
    s = s[sort_indices]
    evecs = evecs[:,sort_indices]
    if r is not None:
        if r > len(s):
            raise ValueError("r is too big")
        else:
            s = s[:r]

    V = np.empty((n,len(s)))
    for i in xrange(V.shape[1]):
        V[:,i] = evecs[:,i]

    U = np.empty((m,len(s)))
    for i in xrange(len(s)):
        U[:,i] = (1./s[i])*A.dot(V[:,i])

    return U, s, V.conj().T

# Problem 2
def visualize_svd(A):
    """Plot each transformation associated with the SVD of A."""
    S = np.load("circle.npz")["circle"]
    vec = np.load("circle.npz")["unit_vectors"]

    U,s,Vh = la.svd(A)

    VhS = Vh.dot(S)
    SigVhS = np.diag(s).dot(VhS)
    USigVhS = U.dot(SigVhS)

    Vhvec = Vh.dot(vec)
    SigVhvec = np.diag(s).dot(Vhvec)
    USigVhvec = U.dot(SigVhvec)

    border1 = [-1.1, 1.1, -1.1, 1.1]
    border2 = [-4.5, 4.5, -4.5, 4.5]
    plt.subplot(2,2,1)
    plt.plot(S[0],S[1],vec[0],vec[1])
    plt.axis(border1)
    plt.axis("equal")
    plt.subplot(2,2,2)
    plt.plot(VhS[0],VhS[1],Vhvec[0],Vhvec[1])
    plt.axis(border1)
    plt.axis("equal")
    plt.subplot(2,2,3)
    plt.plot(SigVhS[0],SigVhS[1],SigVhvec[0],SigVhvec[1])
    plt.axis(border2)
    plt.axis("equal")
    plt.subplot(2,2,4)
    plt.plot(USigVhS[0],USigVhS[1],USigVhvec[0],USigVhvec[1])
    plt.axis(border2)
    plt.axis("equal")
    plt.show()

# Problem 3
def svd_approx(A, k):
    """Returns best rank k approximation to A with respect to the induced 2-norm.

    Inputs:
    A - np.ndarray of size mxn
    k - rank

    Return:
    Ahat - the best rank k approximation
    """
    U,s,Vt = la.svd(A, full_matrices=False)
    S = np.diag(s[:k])
    u1,s1,vt1 = U[:,:k],S[:k,:k],Vt[:k,:]
    diff = (u1.nbytes + np.diag(s1).nbytes + vt1.nbytes) - A.nbytes
    if diff > 0:
        print "WARNING: Given parameters do not result in compressed data."
    Ahat = U[:,:k].dot(S).dot(Vt[:k,:])
    return Ahat

# Problem 4
def lowest_rank_approx(A,e):
    """Returns the lowest rank approximation of A with error less than e
    with respect to the induced 2-norm.

    Inputs:
    A - np.ndarray of size mxn
    e - error

    Return:
    Ahat - the lowest rank approximation of A with error less than e.
    """
    U,s,Vt = la.svd(A, full_matrices=False)

    k = np.where(s<e)[0][0]
    print k

    return svd_approx(A,k)

# Problem 5
def compress_image(filename,k):
    """Plot the original image found at 'filename' and the rank k approximation
    of the image found at 'filename.'

    filename - jpg image file path
    k - rank
    """
    orig_img = plt.imread(filename).astype(float)
    red = orig_img[:,:,0]
    green = orig_img[:,:,1]
    blue = orig_img[:,:,2]

    img = np.zeros(orig_img.shape)
    img[:,:,0] = svd_approx(red,k)
    img[:,:,1] = svd_approx(green,k)
    img[:,:,2] = svd_approx(blue,k)

    img = np.round(img)/255.
    orig_img = np.round(orig_img)/255.
    img[img<0] = 0.
    img[img>1] = 1.

    plt.subplot(2,1,1)
    plt.title("Original Image")
    plt.imshow(orig_img)
    plt.subplot(2,1,2)
    plt.title("Rank " + str(k) + " Approximation")
    plt.imshow(img)
    plt.show()

def grayImage(filename):

    img_color = plt.imread(filename)
    return (img_color[:,:,0]+img_color[:,:,1]+img_color[:,:,2])/3.0


def test(student_module, late=False):

    def grade(p):
        """Manually grade a problem worth 'p' points"""
        part = -1
        while part > p or part < 0:
            part = int(input("\nScore out of " + str(p) + ": "))
        if part == p: return p,""
        else:
            m = "\n" + raw_input("\nEnter extra feedback:")
            return part,m

    def arrayTest(A,B,f):
        if np.allclose(A,B,rtol=.1, atol=.1):
            return 1, ""
        else:
            f = f + "\nCorrect answer:\n" + str(A) + "\nStudent answer:\n" + str(B) + "\n\n"
            return 0, f

    s = student_module

    score = 0
    total = 50
    feedback = ""

    try: #Problem 1: 10 points
        feedback += "\n\nProblem 1 (10 points):"
        points = 0
        errMessage = "\nIncorrect SVD for A = \n"
        m = 4
        n = 3
        A = np.array([1, 0, 3, 1, 2, 0, 5, 0, -1, 0, 3, 5]).reshape((m,n))
        r = 2
        U, S, Vh = truncated_svd(A,r)

        U2,S2,Vh2 = s.truncated_svd(A,r)

        #Check matrix shapes
        if S2.size != r or U2.shape != (m,r) or Vh2.shape != (r,n):
            print U2.shape, S2.shape, Vh2.shape
            feedback += "\n Wrong matrix shapes for input r = " + str(r) + ", A = \n" + str(A)
            feedback += "\nMatrix shapes should be \nU: (m,r)\nS: (r,) or (r,1)\nVh: (r,n)"
            if U2.shape == (m,r) and Vh2.shape == (r,n) and S2.shape == (r,r):
                feedback += "\nHint: return just the diagonal of S (as specified in the docstring)"
                points += 3

        else:
            S = np.diag(S)
            S2 = np.diag(S2)
            p,f = arrayTest(U.dot(S.dot(Vh)), U2.dot(S2.dot(Vh2)), errMessage+str(A))
            points += p*5
            feedback += f

        m = 10
        n = 5
        A = np.random.randint(0,300,(m,n))
        r = 5
        U, S, Vh = truncated_svd(A,r)

        U2,S2,Vh2 = s.truncated_svd(A,r)

        #Check matrix shapes
        if S2.size != r or U2.shape != (m,r) or Vh2.shape != (r,n):
            print U2.shape, S2.shape, Vh2.shape
            feedback += "\n Wrong matrix shapes for input r = " + str(r) + ", A = \n" + str(A)
            feedback += "\nMatrix shapes should be \nU: (m,r)\nS: (r,) or (r,1)\nVh: (r,n)"
            if U2.shape == (m,r) and Vh2.shape == (r,n) and S2.shape == (r,r):
                feedback += "\nHint: return just the diagonal of S (as specified in the docstring)"
                points += 3
        else:
            S = np.diag(S)
            S2 = np.diag(S2)
            p,f = arrayTest(U.dot(S.dot(Vh)), U2.dot(S2.dot(Vh2)), errMessage+str(A))
            points += p*5
            feedback += f

        score += points
        feedback += "\nScore += " + str(points)

    except Exception as e:
        feedback += "\nError: " + e.message

    try: #Problem 2: 10 points
        feedback += "\n\nProblem 2 (10 points):"
        points = 0
        s.visualize_svd()
        p, f = grade(10)
        points = p
        feedback += f

        score += points
        feedback += "\nScore += " + str(points)

    except Exception as e:
        feedback += "\nError: " + e.message

    try: #Problem 3: 10 points
        feedback += "\n\nProblem 3 (10 points):"
        points = 0
        A = np.random.rand(30,30)
        a = 29
        B = np.random.rand(6,8)
        b = 3
        C = np.random.rand(18,10)
        c = 4

        A1 = svd_approx(A,a)
        A2 = s.svd_approx(A,a)
        if A2 is not None:
            p,f = arrayTest(A1,A2,"\nWrong approximation for k=29, A 30x30")
            points += p*4
            feedback += f

        B1 = svd_approx(B,b)
        B2 = s.svd_approx(B,b)
        if B2 is not None:
            p,f = arrayTest(B1,B2,"\nWrong approximation for k=3, A 6x8")
            points += p*3
            feedback += f

        C1 = svd_approx(C,c)
        C2 = s.svd_approx(C,c)
        if C2 is not None:
            p,f = arrayTest(C1,C2,"\nWrong approximation for k=3, A 6x8")
            points += p*3
            feedback += f

        score += points
        feedback += "\nScore += " + str(points)

    except Exception as e:
        feedback += "\nError: " + e.message

    try: #Problem 4: 10 points
        points = 0
        feedback += "\n\nProblem 4 (10 points):"
        hubble = grayImage("hubble.jpg")
        e1 = 3.5
        H1 = lowest_rank_approx(hubble,e1)
        H2 = s.lowest_rank_approx(hubble,e1)
        if H2 is not None:
            p,f = arrayTest(H1,H2,"\nWrong approximation for the Hubble image, e=3.5")
            points += p*5
            feedback += f

        e2 = 10.0
        H1 = lowest_rank_approx(hubble,e2)
        H2 = s.lowest_rank_approx(hubble,e2)
        if H2 is not None:
            p,f = arrayTest(H1,H2,"\nWrong approximation for the Hubble image, e=10.0")
            points += p*5
            feedback += f

        score += points
        feedback += "\nScore += " + str(points)

    except Exception as e:
        feedback += "\nError: " + e.message

    try: #Problem 5: 10 points
        '''
        Spots on image = -2
        '''
        feedback += "\n\nProblem 5 (10 points):"
        points = 0
        s.compress_image("portland.jpg",7)
        p,f = grade(5)
        points += p
        feedback += f

        s.compress_image("portland.jpg",40)
        p,f = grade(5)
        points += p
        feedback += f

        score += points
        feedback += "\nScore += " + str(points)

    except Exception as e:
        feedback += "\nError: " + e.message


    if late:    # Late submission penalty
        feedback += "\n\nHalf credit for late submission."
        feedback += "\nRaw score: " + str(score) + "/" + str(total)
        score *= .5

    # Report final score.
    feedback += "\n\nTotal score: " + str(score) + "/" + str(total)
    percentage = (100.0 * score) / total
    feedback += " = " + str(percentage) + "%"
    if   percentage >=  98.0: feedback += "\n\nExcellent!"
    elif percentage >=  90.0: feedback += "\n\nGreat job!"
    return score, feedback








