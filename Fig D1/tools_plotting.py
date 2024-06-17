
import numpy as np

from matplotlib import pyplot as plt

# for saving results
import pickle

import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'cm'

# Comparing a system of n qubits with a system of m qubits. For a given amplitude damping strength gammam in the m qubit system we compute the amplitude damping strength gamman in the n qubit system
# we do this such that both systems feature the same global depolarizing strength peff
def get_gamman(n,m,gammam):
     
     gamman=1- (  np.power( ( 2**(2*n) -1  ) * (  ( (1 + np.sqrt(1-gammam )  )**(2*m) -1)  /(2**(2*m)-1  )    ) +1    , (1/(2*n))  )  -1      )**2

     return gamman


# Plotting Figure D1
# for making a joint plot of the purities corresponding to the 3-regular graph and the purities corresponding to the Erdos-Renyi graph
def plot_pur_3reg_renyi(layers_max,ns,d,p_edge,noise_type,strength_6qubit,noise_position,samples):
    
    # creating a big figure to plot 2 subfigures in 1 row
    fig, axs = plt.subplots(1,2, figsize=(18,6))
    # for increasing the space between the subplots
    fig.subplots_adjust(wspace=0.4)
   
    # adding titles to the subplots
    axs[0].set_title("(a)",fontsize=28,pad=20)
    axs[1].set_title("(b)",fontsize=28,pad=20)
    
    # PLOTTING THE PURITIES FOR THE 3-REG GRAPH
    # we start at layer zero, as we also plot the initial purity
    layers_list=np.linspace(0,layers_max,layers_max+1)

    # each graph gets a different symbol and color
    symbols=["x",".","v","+"]
    colors=[ "r","m", "g","c" ]
    
    # warning if we use more than 4 graph sizes
    if len(ns)>4:
            raise ValueError("We only specified 4 symbols for different graphs in the code. If you want to plot more than 4 graphs go to the code and add symbols")

    # Plotting the average purity decay in QAOA
    # this for loop runs over the different graphs
    for i in range(0,len(ns)):
        
        n=ns[i]
        
        # in case we do not have 6 qubits we need to compute a new amplitude damping noise strength to keep peff constant
        if n==6: 
            gamman=strength_6qubit
        else:
            # we scale down the local amplitude damping noise strengths starting from a 6-qubit system
            gammam=strength_6qubit
            m=6
            gamman=np.round(get_gamman(m=m,n=n,gammam=gammam),4)
       
        # choose a color and a symbol for the considered graph
        color_chosen=colors[i]
        symbol_chosen = symbols[i]
  
        # loading the data, note: this gives the purities from layer=1 up to layer=layers_max, but not for the initial state. This purity we add by hand in the next step
        purs= pickle.load(  open(   "Data/qaoa_avg_pur_"+ str(  n) + "_qubits_under_"+ str(noise_type) + "_of_strength_" +str(gamman) +"_with_"+ str(layers_max) +"_layers_and_"+str(samples) + "_samples_noise_position_" + str(noise_position) + "_degree_" +str(d) + ".p", "rb" ) )  
        purs=np.append(1,purs)
        
        # plotting the purity decay for the considered graph
        if noise_type=="dephasing": 
                axs[0].plot(layers_list,purs,symbol_chosen + color_chosen,markevery=5, markersize=10,label="n = " + str(n)) 
  
        elif noise_type=="depolarizing": 
                axs[0].plot(layers_list,purs, symbol_chosen + color_chosen,markevery=5, markersize=10,label="n = " + str(n) )    

        elif noise_type=="amp_damping":
                axs[0].plot(layers_list,purs,symbol_chosen + color_chosen,markevery=5, markersize=10,label="n = " + str(n))  

        else:   # warns us if we have asked for another noise model                  
                raise ValueError("Noise type error: unknown noise")
                            
        # reading out the exact average purity
        exact_avg_pur=  pickle.load( open( "Data/exact_avg_pur_"+ str(n) + "_qubits_under_" + str(noise_type) + "_of_strength_" +str(gamman) + "_with_" +str(layers_max) + "_layers_" + ".p", "rb" ) ) 

        # plotting the exact average purity
        axs[0].plot(layers_list,exact_avg_pur,color=color_chosen)          

    # reading out the approximate average purity 
    # we computed the approximate average purity with the 6-qubit graph originally, therefore this graph appears here in the readout of the average purities
    # note that the approximate average purities are all the same for the different graphs as they all feature the same peff
    approx_avg_pur=  pickle.load( open( "Data/approx_avg_pur_"+ str(6) + "_qubits_under_" + str(noise_type) + "_of_strength_" +str(strength_6qubit) + "_with_" +str(layers_max) + "_layers_" + ".p", "rb" ) ) 

    # plotting the approximate average purity    
    axs[0].plot(layers_list,approx_avg_pur,color="black",linestyle="dashed")   

    # xlabel
    axs[0].set_xlabel("layer $\ell$", fontsize=32)
    # ylabel
    axs[0].set_ylabel(" $ \langle \mathrm{Tr}  [ \\rho_{\ell}^2 ] \\rangle $", fontsize=32)

    # choosing the size of the x-ticks and y-ticks
    axs[0].tick_params(axis='both', which='major', labelsize=24)
    axs[0].tick_params(axis='both', which='minor', labelsize=18)
   
    # making the y scale logarithmic
    axs[0].set_yscale("log")

    # Adding a legend
    axs[0].legend(fontsize=28)
    
    # PLOTTING THE PURITIES FOR THE ERDOS-RENYI GRAPH 

    # Plotting the average purity decay in QAOA
    # this for loop runs over the different Erdos-Renyi graphs
    for i in range(0,len(ns)):
        
        n=ns[i]
        
        # in case we do not have 6 qubits we need to compute a new amplitude damping noise strength to keep peff constant
        if n==6: 
            gamman=strength_6qubit
        else:
            # we scale down the local amplitude damping noise strengths starting from a 6-qubit system
            gammam=strength_6qubit
            m=6
            gamman=np.round(get_gamman(m=m,n=n,gammam=gammam),4)
           
        # choose a color and a symbol for the considered graph
        color_chosen=colors[i]
        symbol_chosen = symbols[i]
  
        # loading the data, note: this gives the purities from layer=1 up to layer=layers_max, but not for the initial state. This purity we add by hand in the next step
        purs= pickle.load(  open(   "Data/qaoa_avg_pur_renyi_p_edge_" + str(p_edge)  +"_with_" + str(  n) + "_qubits_under_"+ str(noise_type) + "_of_strength_" +str(gamman) +"_with_"+ str(layers_max) +"_layers_and_"+str(samples) + "_samples_noise_position_" + str(noise_position) +  ".p", "rb" ) )  
        purs=np.append(1,purs)
        
        # plotting the purity decay for the considered graph
        if noise_type=="dephasing": 
                axs[1].plot(layers_list,purs,symbol_chosen + color_chosen,markevery=5, markersize=10,label="n = " + str(n)) 

        elif noise_type=="depolarizing": 
                axs[1].plot(layers_list,purs, symbol_chosen + color_chosen,markevery=5, markersize=10,label="n = " + str(n) )    

        elif noise_type=="amp_damping":
                axs[1].plot(layers_list,purs,symbol_chosen + color_chosen,markevery=5, markersize=10,label="n = " + str(n))  

        else:   # warns us if we have asked for another noise model               
                raise ValueError("Noise type error: unknown noise")
                        
        # reading out the exact average purity
        exact_avg_pur=  pickle.load( open( "Data/exact_avg_pur_"+ str(n) + "_qubits_under_" + str(noise_type) + "_of_strength_" +str(gamman) + "_with_" +str(layers_max) + "_layers_" + ".p", "rb" ) ) 

        # plotting the exact average purity
        axs[1].plot(layers_list,exact_avg_pur,color=color_chosen)          

    # plotting the approximate average purity    
    # we can just use the aproximate average purity that we read out for the 3-reg graph, as it is equivalent to the one for the Renyi graph, as the approximate average purity just depends on the number of qubits    
    axs[1].plot(layers_list,approx_avg_pur,color="black",linestyle="dashed")   

    # xlabel
    axs[1].set_xlabel("layer $\ell$",fontsize=32)
    # ylabel
    axs[1].set_ylabel(" $ \langle \mathrm{Tr}  [ \\rho_{\ell}^2 ] \\rangle $",fontsize=32)

    # choosing the size of the x-ticks and y-ticks
    axs[1].tick_params(axis='both', which='major', labelsize=24)
    axs[1].tick_params(axis='both', which='minor', labelsize=18)
   
    #making the y scale logarithmic
    axs[1].set_yscale("log")

    # Adding a legend
    axs[1].legend(fontsize=28)

