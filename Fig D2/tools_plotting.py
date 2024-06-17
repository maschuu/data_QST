


import numpy as np

import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'

from matplotlib import pyplot as plt

#for saving the results
import pickle


# Plotting Figure D2

# Comparing a system of n qubits with a system of m qubits. For a given AD strength gammam in the m qubit system we compute the amplitude damping strength gamman in the n qubit system
# We do this such that both systems feature the same global depolarizing strength peff
# We need this function because the universal circuit has a different number of qubits than the qaoa circuits for d-regular graphs, which we consider
def get_gamman(n,m,gammam):
     
     gamman=1- (  np.power( ( 2**(2*n) -1  ) * (  ( (1 + np.sqrt(1-gammam )  )**(2*m) -1)  /(2**(2*m)-1  )    ) +1    , (1/(2*n))  )  -1      )**2

     return gamman
 

# ds contains the degrees of the graphs
def plot_fidelities_qaoa(n,ds,noise,samples,layers_max):
    
    # creating a list of the number of layers
    layers=np.linspace(1,layers_max,layers_max)

    # we need this to read out the data
    if noise is not None:   
        
        #noise_type tells us which noise we have
        noise_type = list(noise.keys())[0]
        
        #reading out the noise strength  
        strength=noise[noise_type]
           
    #each graph gets a different symbol and color
    symbols=["+","x","D","."]
    colors=["r", "b","m", "y" ]
    
    for i in range (0,len(ds)):
            
            # this is the symbol and the color we choose for the current graph
            d=ds[i]
            symbol=symbols[i]
            color=colors[i]

            #reading out the fidelities       
            fids=pickle.load( open("Data/fidelities_"+ str(n)+ "_qubits_under_"+ str(noise_type) + "_of_strength_" +str(strength) + "_with_" + str(layers_max) +"_layers_and_"  +str(samples) + "_samples_degree_" +str(d) +".p", "rb" ) )      

            if noise_type=="dephasing" or noise_type=="depolarizing" or noise_type=="amp_damping":

                plt.plot(layers,fids, symbol + color,markevery=1,label= str(d)+ "-regular")

            else:              
                #warns us if we have asked for another noise model  
                raise ValueError("Noise type error: unknown noise")
                       
            #plotting a horizontal line at fidelity=1 to see better when we reach the fidelity 1
            plt.axhline(1, 0, layers_max,color = 'k',linestyle="dashed")

            plt.xlabel("layer $\ell$", fontsize=18)
            plt.ylabel("$ \\tilde{F}  $", fontsize=18)
        
    # plotting the universal qaoa circuit
    # we chose the convention that the universal circuit has degree 0
    d=0
    
    # the circuit is only universal if it has an odd number of qubits, we choose n=5 and save the number of qubits in the original circuit in m
    m=n
    n=5
    
    # we now translate the strength of AD noise from a system with m qubits to a system with n=5 qubits, such that both systems get the same peff
    if noise_type=="amp_damping":

        gamman=get_gamman(m=m,n=n,gammam=strength)

    else: 
        #warns us if we have asked for another noise model
        raise ValueError("We only designed the function to compute the noise strength in the universal circuit for AD")
                 
    #reading out the fidelities for the universal circuit
    fids=pickle.load( open("Data/fidelities_"+ str(n)+ "_qubits_under_"+ str(noise_type) + "_of_strength_" +str(gamman) + "_with_" + str(layers_max) +"_layers_and_"  +str(samples) + "_samples_degree_" +str(d) +".p", "rb" ) ) 

    plt.plot(layers,fids, "s c",markevery=1,label="universal")
    plt.xticks(np.arange(0, layers_max, step=5),fontsize=15)
    plt.yticks(fontsize=15)
    plt.ylim([0.945,1.005])
    plt.legend(ncol=2,fontsize=15)  
    
