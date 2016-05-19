A = np.array([[2,0,-1],[-1,3,2],[0,1,3]])
b = np.array([3,3,-1])

x, x_approx = jacobi_method(A,b)

x_approx = np.array(x_approx)
dom = np.arange(x_approx.shape[0])
norms = []
for i in xrange(x_approx.shape[0]):
    norms.append(la.norm(A.dot(x_approx[i]) - b))

plt.semilogy(dom, norms)
plt.ylabel("Absolute Error of Approximation")
plt.xlabel("Iteration #")
plt.title("Convergence of Jacobi Method")
plt.savefig("jacobi_convergence.pdf")
