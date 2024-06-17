import numpy as np

import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'

from matplotlib import pyplot as plt

#for saving the results
import pickle




            
            
          
# for plotting figure D3
def plot_infids(samples,n,noise_position,strength_a,noise_a,layers_max_a,ds_a,d_b,layers_max_b,noise_type_b,strengths_b):
    
    #creating a big figure that allows 2 subplots
    fig, axs = plt.subplots(1,2, figsize=(15,6))
    
    #for increasing the vertical space between the subplots
    fig.subplots_adjust(wspace=0.3)
    
    # adding titles to the subplots
    axs[0].set_title("(a)",fontsize=28, pad=20)
    axs[1].set_title("(b)",fontsize=28, pad=20)
    
    #plotting Fig D2a
    
    # we need this for reading out the data
    if noise_a is not None:

        #noise_type tells us which noise we have
        noise_type_a = list(noise_a.keys())[0]
        
        #reading out the noise strength
        strength_a=noise_a[noise_type_a]
        
    # generating a list of layers
    layers_a=np.linspace(1,layers_max_a,layers_max_a)

    # data for different graphs are plotted with different symbols and colors
    symbols_a=["+","x","v","."]
    colors_a=["r", "b","m", "y" ]

    # going over the different graphs and plotting the corresponding infidelities
    for i in range (0,len(ds_a)):
      
        # the degree of the considered graph
        d_a=ds_a[i]

        # choose symbol and color for the considered graph
        symbol_chosen_a=symbols_a[i]
        color_chosen_a=colors_a[i]

        #reading out the average infidelities
        infids_avg_a=pickle.load(  open(  "Data/avg_infidelity_"+ str(n)+ "_qubits_under_"+ str(noise_type_a) + "_of_strength_" +str(strength_a) + "_noise_position_" + str(noise_position) + "_with_" + str(layers_max_a) +"_layers_and_"  +str(samples) + "_samples_degree_" +str(d_a) +".p", "rb" ) )  
    
        axs[0].plot(layers_a, infids_avg_a , symbol_chosen_a + color_chosen_a,markevery=5 ,label = str(d_a) + " - regular" )

    axs[0].set_ylabel("$1-F \ (\\rho_{\mathcal{A}}, \\rho_{\mathcal{A}_{\mathrm{Haar}}  }) $",fontsize=20)
    axs[0].set_xlabel("layer $\ell$",fontsize=20)
    axs[0].tick_params(axis='both', labelsize=15)
    axs[0].legend(fontsize=15)
    
    #plotting Fig D2b
     
    # generating a list of layers
    layers_b=np.linspace(1,layers_max_b,layers_max_b)
    
    # data for different noise strengths are plotted with different symbols and colors
    symbols_b=["+",".","x"]  
    colors_b= ["m"  ,"r","b"]
    
    #going over the different noise strengths
    for i in range (0,len(strengths_b)):
        
        # the noise strength of the considered graph
        strength_b=strengths_b[i]
        
        # choose symbol and color for the considered noise strength
        color_chosen_b=colors_b[i]
        symbol_b=symbols_b[i]

        #reading out the average infidelities
        infids_avg_b=pickle.load(  open(  "Data/avg_infidelity_"+ str(n)+ "_qubits_under_"+ str(noise_type_b) + "_of_strength_" +str(strength_b) + "_noise_position_" + str(noise_position) + "_with_" + str(layers_max_b) +"_layers_and_"  +str(samples) + "_samples_degree_" +str(d_b) +".p", "rb" ) )

        plt.plot(layers_b, infids_avg_b  ,symbol_b + color_chosen_b, markevery=5   ,label =  " $\gamma_{\downarrow}$ =  " + str(strength_b)  )

    axs[1].set_ylabel("$1-F \ (\\rho_{\mathcal{A}}, \\rho_{\mathcal{A}_{\mathrm{Haar}}  }) $",fontsize=20)
    axs[1].set_xlabel("layer $\ell$",fontsize=20)
    axs[1].tick_params(axis='both', labelsize=15)
    axs[1].legend(fontsize=15)
    




            
            
            
