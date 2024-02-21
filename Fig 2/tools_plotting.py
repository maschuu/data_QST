


import numpy as np

import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'

from matplotlib import pyplot as plt

#for reading out the data
import pickle



# n : number of qubits
# pmax: maximal probability that the single instance purity lies outside the plotted bounds
def plot_purity_toy_model(n,noise,layers_max,pmax):
    
    # getting the noise type and strength
    if noise is not None:
        
            #noise_type tells us which noise we have
            noise_type = list(noise.keys())[0]
            
            #reading out the noise strength  
            strength=noise[noise_type]
             
    #reading out the exact average purity
    exact_avg_pur=  pickle.load( open( "Data/exact_avg_pur_"+ str(n) + "_qubits_under_" + str(noise_type) + "_of_strength_" +str(strength) + "_with_" +str(layers_max) + "_layers_" + ".p", "rb" ) ) 
    
    #reading out the approximate average purity
    approx_avg_pur=  pickle.load( open( "Data/approx_avg_pur_"+ str(n) + "_qubits_under_" + str(noise_type) + "_of_strength_" +str(strength) + "_with_" +str(layers_max) + "_layers_" + ".p", "rb" ) ) 
    
    #reading out the upper purity bound
    upper_pur=  pickle.load( open( "Data/upper_pur_"+ str(n) + "_qubits_under_" + str(noise_type) + "_of_strength_" +str(strength) + "_with_" +str(layers_max) + "_layers_" + "_and_pmax_" + str(pmax) +  ".p", "rb" ) ) 
    
    #reading out the lower purity bound
    lower_pur=  pickle.load( open( "Data/lower_pur_"+ str(n) + "_qubits_under_" + str(noise_type) + "_of_strength_" +str(strength) + "_with_" +str(layers_max) + "_layers_" + "_and_pmax_" + str(pmax) +  ".p", "rb" ) ) 
    
    # substracting 1/dimension from all purities for the plot
    dimension=2**n
    exact_avg_pur = exact_avg_pur- (1/dimension)
    approx_avg_pur = approx_avg_pur- (1/dimension)
    upper_pur = upper_pur- (1/dimension)
    lower_pur = lower_pur- (1/dimension)
    
    #creating a list of layers
    layers=np.linspace(0,layers_max,layers_max+1)

    #plotting the exact avg puritiy as solid line
    plt.plot(layers,exact_avg_pur,color="blue",  label="Exact avg. purity")

    #plotting the aprroximate avg puritiy as dashed line
    plt.plot(layers,approx_avg_pur, color="blue", linestyle='dashed' ,label="Approx. avg. purity")

    # shading the region between the upper and the lower purity bound
    plt.fill_between(layers, lower_pur , upper_pur, alpha=0.2)
    
    plt.ylim(0.01,1)
    plt.xlim(0,layers_max)
    plt.xlabel("layer $\ell$", fontsize=20)
    plt.ylabel("$\langle \mathrm{Tr}[\\rho_{\ell}^2] \\rangle - \\frac{1}{2^n} $", fontsize=20)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.legend(fontsize=15,loc='upper right')
    plt.yscale('log')


