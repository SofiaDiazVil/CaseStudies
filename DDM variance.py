# -*- coding: utf-8 -*-
"""
Created on Thu May 11 14:09:15 2023

@author: PERSONAL
"""
# Import the libraries 
from pyddm import Sample, Drift, Overlay, Solution, Model, Fittable
from pyddm.models import DriftConstant, NoiseConstant, BoundConstant, OverlayChain, OverlayPoissonMixture, OverlayNonDecision
from pyddm.plot import model_gui
from pyddm.models.loss import LossRobustLikelihood
import pyddm.plot
from pyddm.functions import fit_adjust_model, display_model
import matplotlib.pyplot as plt
import pandas
import os 
import numpy as np 
import scipy
import copy
from math import ceil, sqrt
from statistics import mean



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
path = "D:/Users/PERSONAL/Documents/psychologie Master 2/Case Studies/test files/"
file_list = os.listdir(path)
 
# prints all files to check if correct 
print(file_list)

#%% 
# Make array to store the parameters of each participant 
Parameters_ALL = np.zeros(shape = (9,len(file_list))) # 9 colums (one per parameter, one for ID and one for Lockdown
                                                      # group), and as many rows as files in the directory

# Loop to go through each file DO AT THE END 
#for i in range (len(file_list)):

# Open file 
#file = file_list[i]
file = file_list[3]

with open(file, "r") as f: # name and mode (r -> read)
    df_ddm = pandas.read_csv(f, sep = ";")
    
df_ddm["RT"] = df_ddm["RT"]/1000 # set the reaction to seconds instead of ms

# Create sample with the file 
ddm_sample = Sample.from_pandas_dataframe(df_ddm, rt_column_name="RT", correct_column_name="Correct")  

# Create new sample for the variance of the drift rate 
    # select the number of bins 
RESOLUTION = ceil(sqrt(len(df_ddm)))
if RESOLUTION % 2 == 0:
    RESOLUTION = RESOLUTION-1

RESOLUTION  #number of bins, should be odd number 
# Function to prepare the sample
def prepare_sample_for_variable_drift(ddm_sample, resolution=RESOLUTION):
    new_ddm_samples = []
    for i in range(0, resolution):
        corr = ddm_sample.corr.copy()
        err = ddm_sample.err.copy()
        undecided = ddm_sample.undecided
        conditions = copy.deepcopy(ddm_sample.conditions)
        conditions['driftnum'] = (np.asarray([i]*len(corr)),
                                  np.asarray([i]*len(err)),
                                  np.asarray([i]*undecided))
        new_ddm_samples.append(Sample(corr, err, undecided, **conditions))
    new_ddm_sample = new_ddm_samples.pop()
    for s in new_ddm_samples:
        new_ddm_sample += s
    return new_ddm_sample 

# ACtually create the new sample 
new_ddm_sample = prepare_sample_for_variable_drift(ddm_sample, resolution=RESOLUTION)

# Drift rate and Variance of the drift rate 
class DriftUniform(Drift):
    name = "Uniformly-distributed drift"
    resolution = RESOLUTION # Number of bins. We are using 9
    required_parameters = ['drift', 'width'] # Mean drift and the width of the uniform distribution
    required_conditions = ['driftnum']
    def get_drift(self, conditions, **kwargs):
        stepsize = self.width/(self.resolution-1)
        mindrift = self.drift - self.width/2
        return mindrift + stepsize*conditions['driftnum']

# variance of the non-decision time 
class OverlayNonDecisionGaussian(Overlay):
    name = "Add a Gaussian-distributed non-decision time"
    required_parameters = ["nondectime", "ndsigma"]
    def apply(self, solution):
        # Make sure params are within range
        assert self.ndsigma > 0 # "Invalid st parameter" # CHECK THAT NDSIGMA IS NOT UNDER 0
        # Extract components of the solution object for convenience
        corr = solution.corr
        err = solution.err
        dt = solution.model.dt
        # Create the weights for different timepoints
        times = np.asarray(list(range(-len(corr), len(corr))))*dt
        weights = scipy.stats.norm(scale=self.ndsigma, loc=self.nondectime).pdf(times)
        if np.sum(weights) > 0:
            weights /= np.sum(weights) # Ensure it integrates to 1
        newcorr = np.convolve(weights, corr, mode="full")[len(corr):(2*len(corr))]
        newerr = np.convolve(weights, err, mode="full")[len(corr):(2*len(corr))]
        return Solution(newcorr, newerr, solution.model, solution.conditions, solution.undec)
    
#%%
    
# Build model 
model_ddm = Model(drift = DriftUniform(drift=Fittable(minval=-5, maxval=5),
                                       width=Fittable(minval= 0.0001, maxval=2)),
                  noise=NoiseConstant(noise=Fittable(minval=.5, maxval=5)),
                  bound=BoundConstant(B = Fittable(minval = 0.5, maxval = 2)),
                  overlay = OverlayChain(overlays=[OverlayPoissonMixture(pmixturecoef = .02, rate = 1),
                                                   OverlayNonDecisionGaussian(nondectime = Fittable(minval = 0.1, maxval = 0.5),
                                                                              ndsigma = Fittable(minval = 0.0001, maxval = 0.8))]),
                  dx=.001, dt=.01, T_dur=2)

# Plot model to check the effect of the parameters 
#model_gui(model_ddm, conditions={"driftnum": list(range(0, 11))})

# Fit the model 
fit_model = fit_adjust_model(sample = new_ddm_sample, model = model_ddm, verbose = True, fitting_method="differential_evolution", lossfunction=LossRobustLikelihood) 
display_model(fit_model)
 

#%%
# Draw a plot to observe the actual fit of the model
pyddm.plot.plot_fit_diagnostics(model=fit_model, sample= new_ddm_sample, conditions= {"driftnum": list(range(0, 11))})
#plt.savefig("simple-fit.png")
plt.show()


# Test if they always come in the same order, if so just save them in an array as rows. column names are Name_Parameters
Name_Parameters = Model.get_model_parameter_names(fit_model) #get the name of the fitted parameters
Value_Parameters = Model.get_model_parameters(fit_model) #get the value of the fitted parameters, same order as name function

# # Save data into the array, both parameters and participant information
# Parameters_ALL[i,2:9] = Value_Parameters
# Parameters_ALL[i,0]   = df_ddm["Country"][0]
# Parameters_ALL[i,1]  = df_ddm["ID"][0]


# #%% Save array to CSV 
# Names = " ".join(str(x) for x in Name_Parameters) # set column names as strings 

# np.savetxt("Parameters_lockdown.csv", Parameters_ALL, header = Names)
