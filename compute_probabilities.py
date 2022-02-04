
from rpy2.robjects.packages import importr
from rpy2 import robjects as ro
import numpy as np
from scipy.stats import multivariate_normal as norm
from math import sqrt, log
import time

def pmvnorm(z, mean, cov):
    mvtnorm = importr('mvtnorm', lib_loc = "/home/andmur09/R/x86_64-pc-linux-gnu-library/4.1")
    upper = ro.FloatVector(z)
    mean = ro.FloatVector(mean)
    cov = ro.r.matrix(ro.FloatVector(cov.flatten('f')), nrow=np.shape(cov)[0])
    result = mvtnorm.pmvnorm(upper=upper, mean=mean, sigma=cov)
    return np.asarray(result)[0]


def grad(z, cb, mean, cov):
    #print("\nCalculating Gradient...")
    n = int(np.shape(mean)[0])
    dz = []
    #print("Mean = ", mean)
    #print("Cov = ", cov)
    for i in range(n):
        if cb[i] != -1:
            dz.append(0)
        else:
            bar_mean = np.delete(mean, i)
            bar_cov = np.delete(np.delete(cov, i, 0), i, 1)
            bar_z= np.delete(z, i)
            #print("index = ", i)
            #print("bar mean = ", bar_mean)
            #print("bar cov = ", bar_cov)
            #print("bar z = ", bar_z)
            bar_F = pmvnorm(bar_z, bar_mean, bar_cov)
            f = norm(mean[i], sqrt(cov[i, i])).pdf(z[i])
            dz.append(f * bar_F)
    #print("Finished...\n")
    return np.c_[np.array(dz)]

#print("x")
#print(np.array(2, 3))

mean =  np.array([0, 0, 0, 0, 0, 0])
cov =  np.array([[1, -1,  0,  0,  0,  0], [-1,  1,  0,  0,  0,  0], [ 0,  0,  1, -1,  -1,  1], [0, 0, -1,  1,  1, -1], [ 0,  0, -1,  1,  1, -1], [ 0,  0,  1, -1, -1,  1]])

z1 = np.array([3, 1.30773624, 3, 3, 3, 2.70407431])
#2 = np.array([3, 1.42703084, 3, 3, 3, 2.94081486])



#print(-norm(mean, cov, allow_singular=True).logcdf(z1))
#print(-norm(mean, cov, allow_singular=True).logcdf(z2))
#F1 = pmvnorm(z1, mean, cov)
#F2 = pmvnorm(z2, mean, cov)
#print(-log(F1))
#print(-log(F2))
start = time.time()
print(pmvnorm(z1, mean, cov))
end = time.time()
print(end - start)
#print(F2)
start = time.time()
print(norm(mean, cov, allow_singular=True).cdf(z1))
end = time.time()
print(end - start)
#print(norm(mean, cov, allow_singular=True).cdf(z2))