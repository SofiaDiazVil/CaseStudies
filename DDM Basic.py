# -*- coding: utf-8 -*-
"""
Created on Thu May 11 14:09:15 2023

@author: PERSONAL
"""
# Import the libraries 
from pyddm import Sample, Drift, Overlay, Solution, Model, Fittable
from pyddm.models import DriftConstant, NoiseConstant, BoundConstant, OverlayChain, OverlayPoissonMixture, OverlayNonDecision
from pyddm.models.loss import LossRobustLikelihood
from pyddm.plot import model_gui
import pyddm.plot
from pyddm.functions import fit_adjust_model, display_model
import matplotlib.pyplot as plt
import pandas
import os 
import numpy as np 
import scipy
import copy



#%%
# # Variable names --> check if they match the file 
# ID # participant ID
# Country # lockdown group, japan or scotland 
#     japan or scotland 
# RT # reaction time 
# Correct # accuracy 
#   0 or 1 

#%%
# Create list of file names for the DDM 
    # Get the list of all files and directories
path = "D:/Users/PERSONAL/Documents/psychologie Master 2/Case Studies/test files/" #set here the path to the folder where the raw data files are
file_list = os.listdir(path)
 
# prints all files to check if correct 
print(file_list)

#%% 
# Make array to store the parameters of each participant 
Parameters_ALL = np.zeros(shape = (len(file_list),6)).astype(object) # 6 colums (one per parameter, one for ID and one for Lockdown
                                                                     # group), and as many rows as files in the directory

# Loop to go through each file DO AT THE END 
for i in range (len(file_list)):

    # Open file 
    file = file_list[i]
    #file = file_list[2]
    
    with open(file, "r") as f: # name and mode (r -> read)
        df_ddm = pandas.read_csv(f, sep = ",") # the files are separated by ";" not ","
        
    df_ddm["RT"] = df_ddm["RT"]/1000 # set the reaction to seconds instead of ms
    
    # Create sample with the file 
    ddm_sample = Sample.from_pandas_dataframe(df_ddm, rt_column_name="RT", correct_column_name="Correct")  
    
    
    # Build model, identify which parameters have to be fitted or estimated 
    model_ddm = Model(drift = DriftConstant(drift=Fittable(minval=-5, maxval=5)),
                      noise=NoiseConstant(noise=Fittable(minval=.5, maxval=5)),
                      bound=BoundConstant(B = Fittable(minval = 0.5, maxval = 2)),
                      overlay = OverlayNonDecision(nondectime=Fittable(minval=0.1, maxval=0.5)),
                      dx=.01, dt=.01, T_dur=3)
    
    # Plot model to check the effect of the parameters 
    #model_gui(model_ddm, conditions={"driftnum": list(range(0, 11))})

    # Fit the model using differential evolution and robst loss likelihood 
    fit_model = fit_adjust_model(sample = ddm_sample, model = model_ddm, 
                                 fitting_method="differential_evolution", 
                                 lossfunction=LossRobustLikelihood, verbose = True) 
    #display_model(fit_model) #display the parameters if needed 
 
    ## Draw a plot to observe the actual fit of the model
    #pyddm.plot.plot_fit_diagnostics(model=fit_model, sample= ddm_sample)
    #plt.savefig("simple-fit.png") #save the figure if needed 
    #plt.show()


    # Save the Name of the parameters and the value
    Name_Parameters = Model.get_model_parameter_names(fit_model) #get the name of the fitted parameters
    Value_Parameters = Model.get_model_parameters(fit_model) #get the value of the fitted parameters, same order as name function

    # Save data into the array, both parameters and participant information
    # drift
    drift = Value_Parameters[0] #select the parameter
    drift = str(drift) #turn fitted object into a string
    drift = drift[7:15] #select the value, skip the "Fitted(" and select the valu decimals 
    # noise 
    noise = Value_Parameters[1]
    noise = str(noise)
    noise = noise[7:15]
    # boundary 
    B = Value_Parameters[2]
    B = str(B)
    B = B[7:15]
    # non-decision time 
    NDT = Value_Parameters[3]
    NDT = str(NDT)
    NDT = NDT[7:15]

    # Save the value of the parameters into the array as well participant info
    Parameters_ALL[i,0] = df_ddm["Country"][0]
    Parameters_ALL[i,1] = df_ddm["ID"][0]
    Parameters_ALL[i,2] = drift
    Parameters_ALL[i,3] = noise
    Parameters_ALL[i,4] = B
    Parameters_ALL[i,5] = NDT


#% Save array to CSV 
Names = " ".join(str(x) for x in Name_Parameters) # set column names as strings 
np.savetxt("Parameters_lockdown.csv", Parameters_ALL, header = Names, fmt='%s', delimiter=',')

#%% 
# Test the parameter retrieval 
    # This code needs to be run for each file separately. The first part is very similar to the first section 
    # of the code (a model is fitted with the original data). 
    
# 
# Open file 
file = file_list[4]

with open(file, "r") as f: # name and mode (r -> read)
    df_ddm = pandas.read_csv(f, sep = ",") # the files are separated by ";" not ","

    
df_ddm["RT"] = df_ddm["RT"]/1000 # set the reaction to seconds instead of ms

# Create sample with the file 
ddm_sample = Sample.from_pandas_dataframe(df_ddm, rt_column_name="RT", correct_column_name="Correct")  

# Build model, identify which parameters have to be fitted or estimated 
model_ddm = Model(drift = DriftConstant(drift=Fittable(minval=-5, maxval=5)),
                  noise=NoiseConstant(noise=Fittable(minval=.5, maxval=5)),
                  bound=BoundConstant(B = Fittable(minval = 0.5, maxval = 2)),
                  overlay = OverlayNonDecision(nondectime=Fittable(minval=0.1, maxval=0.5)),
                  dx=.01, dt=.01, T_dur=3)
# Fit the model using differential evolution and robst loss likelihood 
fit_model = fit_adjust_model(sample = ddm_sample, model = model_ddm, 
                             fitting_method="differential_evolution", 
                             lossfunction=LossRobustLikelihood, verbose = True)

# Save the original parameters 
Name_Parameters = Model.get_model_parameter_names(fit_model)
Original_Parameters = Model.get_model_parameters(fit_model)

# Create a series that you can resample, for this we need to fit the model
sol = model_ddm.solve()

# Create a new sample or data based on the previous model/series 
samp = sol.resample(200) #different number of trials can be tested. We did 60, 70, 80 and 200

# Define the model 
model_retrieval = Model(drift = DriftConstant(drift=Fittable(minval=-5, maxval=5)),
                  noise=NoiseConstant(noise=Fittable(minval=.5, maxval=5)),
                  bound=BoundConstant(B = Fittable(minval = 0.5, maxval = 2)),
                  overlay = OverlayNonDecision(nondectime=Fittable(minval=0.1, maxval=0.5)),
                  dx=.01, dt=.01, T_dur=2)

# Fit the model to the new data 
fit_retrieval = fit_adjust_model(samp, model_retrieval,
                                 fitting_method = "differential_evolution",
                                 lossfunction = LossRobustLikelihood, verbose=True)

# Save the parameters for this new data 
Retrieved_Parameter = Model.get_model_parameters(fit_retrieval) 

# Compare the retrieved parameters with the original ones 
print(Name_Parameters)
print(Original_Parameters)
print(Retrieved_Parameter)

print("# trials:", len(df_ddm))

# The comparison was done manually based on the output of the previous lines.
# For 60 trial   
    # file 0 --> ~ 0.15 diffence across parameters.
    # file 1 --> ~ 0.15 diffence across parameters.  
    # file 2 --> ~ 0.5 diffence across parameters. 
    # file 3 --> ~ 0.05 difference across parameters. 
    # file 4 --> ~ 0.05 difference across parameters 
# For 70 trial   
    # file 0 -->  ~ 0.2 diffence across parameters.
    # file 1 -->  ~ 0.5 diffence across parameters.  
    # file 2 -->  ~ 0.05 diffence across parameters. 
    # file 3 -->  ~ 0.1 difference across parameters. 
    # file 4 -->  ~ 0.05 difference across parameters
# For 80 trial   
    # file 0 -->  ~ 0.05 diffence across parameters.
    # file 1 -->  ~ 0.15 diffence across parameters.  
    # file 2 -->  ~ 0.2 diffence across parameters. 
    # file 3 -->  ~ 0.1 difference across parameters. 
    # file 4 -->  ~ 0.05 difference across parameters
# For 200 trial   
    # file 0 -->  ~ 0.1 diffence across parameters.
    # file 1 -->  ~ 0.2 diffence across parameters.  
    # file 2 -->  ~ 0.1 diffence across parameters. 
    # file 3 -->  ~ 0.1 difference across parameters. 
    # file 4 -->  ~ 0.1 difference across parameters



