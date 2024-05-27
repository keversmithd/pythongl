import numpy as np



def f(x):
    return x[0]+x[1]+x[2]

def probability_measure(x):
    mean = 0.5
    std_dev = 1
    return np.exp(-1/2*((x[0]-mean)/std_dev)**2)*np.exp(-1/2*((x[1]-mean)/std_dev)**2)*np.exp(-1/2*((x[2]-mean)/std_dev)**2)

def trap_quad():

    #dimension
    dimension = 3
    
    # covariance
    covariance = [[1.2312,0,0],[0,2.31231,0],[0,0,2.31231]]

    # step space intervals

    sum_left = 0
    sum_right = 0
    sum_mid = 0

    previous_mu_left = 0
    previous_mu_right = 0
    previous_mu_mid = 0

    previous_measure = 0
    for i in range(0,200):



        x_left = np.random.multivariate_normal([i,i,i], covariance).T
        x_right = np.random.multivariate_normal([i+1,i+1,i+1], covariance).T
        x_mid = np.random.multivariate_normal([i+(1/2),i+(1/2),i+(1/2)], covariance).T
        
        dmu_left = probability_measure(x_left) - previous_mu_left
        dmu_right = probability_measure(x_right) - previous_mu_right
        dmu_mid = probability_measure(x_mid) - previous_mu_mid

        sum_left += f(x_left)*dmu_left
        sum_right += f(x_right)*dmu_right
        sum_mid += f(x_mid)*dmu_mid

        #dmu and so forth and so on

    return ( sum_left + 2*sum_mid + sum_right)/3

def guass_quadrature():
    n = 32

    sample_points = [np.random.rand(3) for _ in range(0,n)]
    weights = [1/n for _ in range(0,n)]
    result = 0
    previous_measure = 0
    for i in range(0,n):
        dmu = probability_measure(sample_points[i]) - previous_measure
        result += (f(sample_points[i])*weights[i])*dmu
        previous_measure = probability_measure(sample_points[i])
    
    print(result/(n-0)) # / (b-a)



print(guass_quadrature())