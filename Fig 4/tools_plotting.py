


import numpy as np

import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'

from matplotlib import pyplot as plt

#for reading out the data
import pickle




# plotting figure 4
def plot_purs_std(noise_type,strengths,noise_position,samples,n,layers_max_a,ds_a,layers_max_b,d_b):
    
    #creating a big figure that allows 2 subplots
    fig, axs = plt.subplots(1,2, figsize=(15,6))
    
    #for increasing the space between the subplots
    fig.subplots_adjust(wspace=0.3)
    
    # adding titles to the subplots
    axs[0].set_title("(a)",fontsize=28, pad=20)
    axs[1].set_title("(b)",fontsize=28, pad=20)
    
    #plotting Fig 4a
    #we start at zero, as we also plot the initial purity
    layers_list_a=np.linspace(0,layers_max_a,layers_max_a+1)
    
    #each graph gets a different symbol
    symbols_a=["x",".","v","+"]

    #each noise strength gets a different color
    colors_a=["r", "b","m", "y" ]
    
    #warning if we use more than 4 graphs
    if len(ds_a)>4:
            raise ValueError("We only specified 4 symbols for different graphs in the code.")

    #warning if we use more than 4 noise strengths
    if len(strengths)>4:
            raise ValueError("We only specified 4 colours for plotting different noise strengths.")

    #this for loop runs over the different noise strengths
    for i in range (0,len(strengths)): 
            
            strength_a=strengths[i]
            #choose a color for the considered noise strength
            color_chosen_a=colors_a[i]

            #reading out the approximate average purity
            approx_avg_pur_a=  pickle.load( open( "Data/approx_avg_pur_"+ str(n) + "_qubits_under_" + str(noise_type) + "_of_strength_" +str(strength_a) + "_with_" +str(layers_max_a) + "_layers_" + ".p", "rb" ) ) 
            
            #reading out the exact average purity
            exact_avg_pur_a=  pickle.load( open( "Data/exact_avg_pur_"+ str(n) + "_qubits_under_" + str(noise_type) + "_of_strength_" +str(strength_a) + "_with_" +str(layers_max_a) + "_layers_" + ".p", "rb" ) ) 
            
            # substracting 1/dimension from the purity
            dimension=2**n
            approx_avg_pur_a = approx_avg_pur_a- (1/dimension)
            exact_avg_pur_a = exact_avg_pur_a- (1/dimension)
            
            #plotting the approx avg purity
            axs[0].plot(layers_list_a,approx_avg_pur_a,color=color_chosen_a,linestyle="dashed",)   

            #plotting the exact avg purity
            if noise_type=="dephasing": 
                    axs[0].plot(layers_list_a,exact_avg_pur_a,color=color_chosen_a,label="$p   \\approx $ " + str(np.round(strength_a,3)))  
                
            elif noise_type=="depolarizing": 
                    axs[0].plot(layers_list_a,exact_avg_pur_a,color=color_chosen_a,label="p = " + str(strength_a))    

            elif noise_type=="amp_damping":
                    axs[0].plot(layers_list_a,exact_avg_pur_a,color=color_chosen_a,label="$ \gamma_{\downarrow} = $ " + str(strength_a))    

            else:              
                #warns us if we have asked for another noise model   
                raise ValueError("Noise type error: unknown noise")
                

    # Plotting the avg purity decay in QAOA
    # we have 2 for loops. The outer one runs over the degree of the graph, the inner one runs over the noise strength.
    for j in range(0,len(ds_a)):
        
        # choosing the degree of the considered graph
        d_a=ds_a[j]
        #choosing the symbol for the considered graph
        symbol_a=symbols_a[j]

        for i in range (0,len(strengths)): 

            # choosing a color for the considered noise strength
            strength_a=strengths[i]
            color_chosen_a=colors_a[i]

            #loading the average purity for qaoa. Note: this gives the purities from layer=1 until layer=layer_max, but not for the initial state. This purity we add by hand in the second next step.
            purs_a= pickle.load(  open(   "Data/qaoa_avg_pur_"+ str(  n) + "_qubits_under_"+ str(noise_type) + "_of_strength_" +str(strength_a) +"_with_"+ str(layers_max_a) +"_layers_and_"+str(samples) + "_samples_noise_position_" + str(noise_position) + "_degree_" +str(d_a) + ".p", "rb" ) )  
            #substracting the purity of the completely mixed state
            purs_a=purs_a-(1/dimension)
            #adding the initial purity as the first element
            purs_a=np.append(1-(1/dimension),purs_a)

            #plotting the decay of the average purity in qaoa
            if noise_type=="dephasing": 
                axs[0].plot(layers_list_a,purs_a,symbol_a + color_chosen_a,markevery=5) 

            elif noise_type=="depolarizing": 
                axs[0].plot(layers_list_a,purs_a, symbol_a + color_chosen_a,markevery=5 )    

            elif noise_type=="amp_damping":
                axs[0].plot(layers_list_a,purs_a,symbol_a + color_chosen_a,markevery=5)  

            else:              
                #warns us if we have asked for another noise model 
                raise ValueError("Noise type error: unknown noise")
                  
    axs[0].set_ylabel(" $ \langle \mathrm{Tr}  [ \\rho_{\ell}^2 ] \\rangle -\\frac{1}{2^n} $",fontsize=20)
    axs[0].set_xlabel("layer $\ell$",fontsize=20)
    axs[0].tick_params(axis='both', labelsize=15)
    axs[0].set_yscale("log")
    axs[0].legend(fontsize=15)
    
    #plotting Fig 4b
    
    #plotting from layer=1 to layer=layers_max
    layers_list_b=np.linspace(1,layers_max_b,layers_max_b)

    #symbols and colors for the different noise strengths
    symbols_b=["+","x","v","."]
    colors_b=["r", "b","m", "y" ]

    #going over the different noise strengths
    for i in range (0,len(strengths)): 

        strength_b=strengths[i]
        symbol_b=symbols_b[i]
        
        #choose a color for the current noise strength
        color_chosen_b=colors_b[i]

        # reading out the standard deviations
        stds_b= pickle.load(  open(   "Data/qaoa_std_pur_"+ str(  n) + "_qubits_under_"+ str(noise_type) + "_of_strength_" +str(strength_b) +"_with_"+ str(layers_max_b) +"_layers_and_"+str(samples) + "_samples_noise_position_" + str(noise_position) + "_degree_" +str(d_b) + ".p", "rb" ) )  

        # making the y scale logarithmic
        axs[1].set_yscale("log")

        if noise_type=="dephasing": 
            axs[1].plot(layers_list_b,stds_b, symbol_b+color_chosen_b,markevery=2,label="p $\\approx$ " + str(np.round(strength_b,3)))  

        elif noise_type=="depolarizing": 
            axs[1].plot(layers_list_b,stds_b, symbol_b+color_chosen_b,markevery=2,label=" p = " + str(strength_b))         
          
        elif noise_type=="amp_damping": 
            axs[1].plot(layers_list_b,stds_b, symbol_b+color_chosen_b, markevery=2,label=" $ \gamma_{\downarrow} = $" + str(strength_b) )   

        else:              
            #warns us if we have asked for another noise model   
            raise ValueError("Noise type error: unknown noise")
                
    axs[1].set_ylabel("  $  \sqrt{ \mathrm{Var} (  \mathrm{Tr} [\\rho_{\ell}^2]  )}  $  / $ ( \langle  \mathrm{Tr} [\\rho_{\ell}^2] \\rangle -\\frac{1}{2^n} )  $",fontsize=18)
    axs[1].set_xlabel("layer $\ell$",fontsize=20)
    axs[1].tick_params(axis='both', labelsize=15)
    axs[1].legend(fontsize=15)
    
    
    
    
    
    
    
