


import numpy as np

import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'

from matplotlib import pyplot as plt
#for reading out the data
import pickle


# plotting fig 5
# ds gives the degrees of the graphs
def plot_der(layers_max,samples,noise,noise_position,n,ds):

    # we only design this function for 2 graphs, so we should get a warnig if ds does not exactly contain 2 elements
    if len(ds)==2:
        pass
    else:
        raise ValueError("The plot is designed for exactly 2 graphs. So d should be of length 2.")
    
    #creating a big figure that allows 2x2 plots
    fig, axs = plt.subplots(2, 2, figsize=(15,12))
    
    #for increasing the horizontal space between the subplots
    fig.subplots_adjust(hspace=0.6)

    #creating a list with the layer numbers
    layers=np.linspace(1,layers_max,layers_max)
    
    # adding titles to the subplots
    axs[0, 0].set_title("(a)",fontsize=28, pad=20)
    axs[0, 1].set_title("(b)",fontsize=28, pad=20)
    axs[1,0].set_title("(c)",fontsize=28, pad=20)
    axs[1,1].set_title("(d)",fontsize=28, pad=20)
    
    # we need this for reading out the data
    if noise is not None:
                
        #noise_type tells us which noise we have
        noise_type = list(noise.keys())[0]
        
        #reading out the noise strength 
        strength=noise[noise_type]
            
    # going over the different graphs
    for i in range (0,len(ds)):
        
        d=ds[i]

        #reading out the average of the absolute value of the derivatives of gamma and the corresponding variance 
        avg_g=  pickle.load( open( "Data/gammas/abs_avg_derivatives_gamma_" + str(n) + "_qubits_under_"+ str(noise_type) + "_of_strength_" + str(strength) + "_with_"+str(layers_max) + "_layers_and_"+str(samples)  + "_samples_noise_pos_" + str(noise_position) + "_degree_"  + str(d) + ".p", "rb" ) ) 
        vars_g=  pickle.load( open( "Data/gammas/abs_var_derivatives_gamma_" + str(n) + "_qubits_under_"+ str(noise_type) + "_of_strength_" + str(strength) + "_with_"+str(layers_max) + "_layers_and_"+str(samples)  + "_samples_noise_pos_" + str(noise_position) + "_degree_"  + str(d) + ".p", "rb" ) ) 
        
        #reading out the average of the absolute value of the derivatives of alpha and the corresponding variance 
        avg_a=  pickle.load( open( "Data/alphas/abs_avg_derivatives_alpha_" + str(n) + "_qubits_under_"+ str(noise_type) + "_of_strength_" + str(strength) + "_with_"+str(layers_max) + "_layers_and_"+str(samples)  + "_samples_noise_pos_" + str(noise_position) + "_degree_"  + str(d) + ".p", "rb" ) ) 
        vars_a=  pickle.load( open( "Data/alphas/abs_var_derivatives_alpha_" + str(n) + "_qubits_under_"+ str(noise_type) + "_of_strength_" + str(strength) + "_with_"+str(layers_max) + "_layers_and_"+str(samples)  + "_samples_noise_pos_" + str(noise_position) + "_degree_"  + str(d) + ".p", "rb" ) ) 
        
        # using i such that the first graph goes to the first column and the second graph goes to the second column
        # plotting the average in the first row
        axs[0,i ].plot(layers, avg_g , "> k",markevery=5 ,label="$ \langle |\partial_{\gamma_{0}} C |  \\rangle   $")
        axs[0, i].plot(layers, avg_a , "< r",markevery=5 ,label="$ \langle |\partial_{\\alpha_{L}} C |  \\rangle  $")

    
        axs[0,i ].set_yscale("log")   
        axs[0,i ].set_xlabel("layer $\ell$", fontsize=28)
        axs[0,i ].tick_params(axis='both', labelsize=28)
        axs[0,i ].legend(fontsize=28)
        axs[0,i ].set_xticks( [0,20,40,60,80],["0","20","40","60","80"] ,  fontsize=28)
        
        # setting the y-label ticks for the 3-regular graph:
        if d==3:
            axs[0,i ].set_yticks( [1,2,3,4,6],["1","2","3","4","6"] ,  fontsize=28)
            
        # setting the y-label ticks for the 5-regular graph:
        elif d==5:
            axs[0,i ].set_yticks( [2,3,4,6,9,15],["2","3","4","6","9","15"] ,  fontsize=28)
       
        else: 
            pass
        
        # Plottting the variance in the second row
        axs[1,i ].plot(layers, vars_g , "> k",markevery=5 ,label="$  \mathrm{Var} (   |\partial_{\gamma_{0}} C |  )  $")
        axs[1,i ].plot(layers, vars_a , "< r",markevery=5 ,label="$\mathrm{Var} (   |\partial_{\\alpha_{L}} C |  ) $")
        

        axs[1,i ].set_yscale("log")
        axs[1,i ].set_xlabel("layer $\ell$", fontsize=28)
        axs[1,i ].tick_params(axis='both', labelsize=28)
        axs[1,i ].legend(fontsize=28)
        axs[1,i ].set_xticks( [0,20,40,60,80],["0","20","40","60","80"] ,  fontsize=28)
        
        # plot range for the 3-regular graph
        if d==3:
            axs[1,i ].set_ylim([0.3,25])
        # plot range for the 5-regular graph
        elif d==5:
            axs[1,i ].set_ylim([3,150])
    
        else: 
            pass
            
            