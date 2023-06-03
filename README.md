# CaseStudies
In this repository you can find the code and data used for our Case Studies project. Using the elements available in this repository you can replicate our results.

Here below you can find a description of what each script is 
- DDM Basic.py : simplest version of the DDM model. It only calculates the drift rate, noise, boundary and non-decision time. This is the code used for the results in the paper. 
- DDM congruency.py : DDM model that calculates the same as the Basic version, but additionally it als estimates a different drift rate and non decision time for the congruent and incongruent trials. This code was never run, it was rather made as an exercice. 
- DDM Variance.py : DDM model that calculates the same as the Basic version, but additionally it also estimates the variance of the drift rate and non-decision time. This code wasn't used since  it takes a longer time to run and the variance was not necessary for our hypotheses. 

Here below you can find the information regarding the data 
- folder Raw Data Files : in this folder you can find one excel (CVS) file per participant. An explanation regarding how this data needs to be used can be found in the README file in this folder. 
- Parameters_lockdown_finaldataset.csv : excel file (CVS) produced after running the "DDM Basic.py". With participants that have a parameter estimation that has less than 6 decimals the values in the excel file were not automatically saved correctly (extra letters not corresponding to the parameter estimate were also saved) and thus this was corrected manually (keep only the estimates). The corrected version is the one uploaded here. 
- 'CODE PARAMETERTESTING-1.r': the code used for the MANOVA analyses. It calculates the means and standard deviations of each parameters, as well as test our models using MANOVA. It also contains our script for making the figures and plots.


