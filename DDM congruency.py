# -*- coding: utf-8 -*-
"""
Created on Thu May 11 14:09:15 2023

@author: PERSONAL
"""
# Import the libraries 
from pyddm import Sample, Drift, Overlay, Solution, Model, Fittable
from pyddm.models import NoiseConstant, BoundConstant, OverlayChain, OverlayNonDecision, OverlayPoissonMixture
from pyddm.plot import model_gui
from pyddm.functions import fit_adjust_model, display_model
import pandas
import os 
import numpy as np 
import scipy



#%%
# # Variable names --> check if they match the file 
# ID # participant ID
# lockdown # lockdown group, japan or scotland 
#     japan or scotland 
# cond_trial # congruent or incongruent trial 
#     congruent or incongruent
# rt # reaction time 
# acc # accuracy 
#   0 or 1 

#%%
# Create list of file names for the DDM 
    # Get the list of all files and directories
path = ""
file_list = os.listdir(path)
 
# prints all files to check if correct 
print(file_list)

#%% 
# Make array to store the parameters of each participant 
Parameters_ALL = np.zeros(shape = (11,len(file_list))) # 11 colums (one per parameter, one for ID and one for Lockdown
                                                      # group), and as many rows as files in the directory

# Loop to go through each file DO AT THE END 
#for i in range (len(file_list)):

# Open file 
#file = file_list[i]
file = file_list[1]

with open(file, "r") as f: # name and mode (r -> read)
    df_ddm = pandas.read_csv(f)
    
ddm_sample = Sample.from_pandas_dataframe(df_ddm, rt_column_name="rt", correct_column_name="acc")  

# non decision time 
class OverlayNonDecisionTrial(OverlayNonDecision):
    name = "Non-decision time for congruent and incongruent trials, and its variability"
    required_parameters = ["nondectime_cong", "nondectime_incong"]
    required_conditions = ["cond_trial"]
    def get_nondecision_time(self, conditions):
        assert conditions['side'] in ["congruent", "incongruent"], "Invalid trial condition" #if congruency doesn't match the expected categories 
        return self.nondectimecong if conditions['cond_trial'] == "congruent" else self.nondectime_incong
    
        
# Drift Rate 
    # Drift rate variability has not been included, pyddm is not efficient for this (SOLVE LATER)
class DriftTrial(Drift):
    name = "Drift for congruent and incongruent trials, and its variability"
    required_parameters = ["drift_cong", "drift_incong"] 
    required_conditions = ["cond_trial"] 
    def get_drift(self, conditions, **kwargs):
        assert conditions['side'] in ["congruent", "incongruent"], "Invalid trial condition" #if congruency doesn't match the expected categories 
        return self.drift_cong if conditions['cond_trial'] == "congruent" else self.drift_incong

# Build model 
model_ddm = Model(overlay=OverlayChain(overlays=[OverlayNonDecisionTrial(nondectime_cong = Fittable(minval = 0, maxval = 1),
                                                                         nondectime_incong = Fittable(minval = 0, maxval = 1)),
                                                 OverlayPoissonMixture(pmixturecoef = .02, rate = 1)]),                                            
                  noise=NoiseConstant(noise = Fittable(minval = 0, maxval = 5)),
                  bound=BoundConstant(B = Fittable(minval = 0.1, maxval = 1.5)),
                  drift=DriftTrial(drift_cong = Fittable(minval = 0, maxval = 1),
                                   drift_incong = Fittable(minval = 0, maxval = 1)),
                  dx = 0.001, dt = 0.01, T_dur = 2)

# Fit the model 
fit_model = fit_adjust_model(sample = ddm_sample, model = model_ddm, verbose = True)
display_model(fit_model)

# Plot model to check the effect of the parameters 
model_gui(fit_model, conditions={"cond_trial": ["congruent", "incongruent"]})

# Test if they always come in the same order, if so just save them in an array as rows. column names are Name_Parameters
Name_Parameters = Model.get_model_parameter_names(fit_model) #get the name of the fitted parameters
Value_Parameters = Model.get_model_parameters(fit_model) #get the value of the fitted parameters, same order as name function

# # Save data into the array, both parameters and participant information
# Parameters_ALL[i,1:9] = Value_Parameters
# Parameters_ALL[i,10]   = df_ddm["lockdown"][0]
# Parameters_ALL[i,0]  = df_ddm["ID"][0]


# #%% Save array to CSV 
# Names = " ".join(str(x) for x in Name_Parameters) # set column names as strings 

# np.savetxt("Parameters_lockdown.csv", Parameters_ALL, header = Names)
