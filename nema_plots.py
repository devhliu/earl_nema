from earl_nema import NemaRC
import pydicom
from pydicom.tag import Tag
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class NemaPlots():

    def __init__(self, RCs, recons, title):

        ''' Recovery coefficient plots including EARL guidelines
            using RCs generated from NemaRC class

        Parameters:
        RCs (list): List containing NemaRC objects from each recon
        recons (list): List containing strngs with the recon parameters of each element in RCs
        title (str): Title of plot (recon parameters to be compared)
        '''
        self.RCs = RCs
        self.recons = recons
        self.title = title

        # EARL ranges

        #EARL 1
        self.RC_max_1 = np.array([[0.95,1.16],[0.91,1.13],[0.83,1.09],
                                        [0.73,1.01],[0.59,0.85],[0.31,0.49]])
        self.RC_mean_1 = np.array([[0.76,0.89],[0.72,0.85],[0.63,0.78],
                                        [0.57,0.73],[0.44,0.60],[0.27,0.38]])

        #EARL 2
        self.RC_max_2 = np.array([[1.05,1.29],[1.01,1.26],[1.01,1.32],
                                        [1.00,1.38],[0.85,1.22],[0.52,0.88]])
        self.RC_mean_2 = np.array([[0.85,1.0],[0.82,0.97],[0.8,0.99],
                                        [0.76,0.97],[0.63,0.86],[0.39,0.61]])
        self.SUV_peak_2 = np.array([[0.99,1.07],[0.95,1.07],[0.9,1.09],[0.75,0.99],[0.45,0.69],[0.27,0.41]])

        self.spheres = np.array([37, 28, 22, 17, 13, 10])

        

    def RCmean(self):
        
        x = [10,37]
        y = [1,1]
        
        sns.set_style("white")
        #sns.set_palette("husl")
        plt.figure(figsize=(8,7))
        for RC,recon in zip(self.RCs,self.recons):
            plt.plot(self.spheres,RC.spheres['RC_mean'],marker='o', linestyle = '--',label=recon)

        plt.fill_between(self.spheres, self.RC_mean_1[:,0], self.RC_mean_1[:,1],
                                color='lightblue', alpha=0.2, label='EARL 1')
        plt.fill_between(self.spheres, self.RC_mean_2[:,0], self.RC_mean_2[:,1],
                                color='C4', alpha=0.2, label='EARL 2')
        plt.xlabel('Sphere Diameter (mm)',fontsize = 16)
        plt.plot(x,y,linestyle='--',color='gray')
        plt.ylabel('RC Mean', fontsize = 16)
        plt.ylim(0.4,1.2)
        plt.legend(fontsize = 12,loc='lower right')
        plt.title(self.title + ' RC Mean',fontsize=16)
        plt.show()

    def RCmax(self):

        x = [10,37]
        y = [1,1]
        
        sns.set_style("white")
        #sns.set_palette("husl")
        plt.figure(figsize=(8,7))
        for RC,recon in zip(self.RCs,self.recons):
            plt.plot(self.spheres,RC.spheres['RC_max'],marker='o', linestyle = '--',label=recon)

        plt.fill_between(self.spheres, self.RC_max_1[:,0], self.RC_max_1[:,1],
                                color='lightblue', alpha=0.2, label='EARL 1')
        plt.fill_between(self.spheres, self.RC_max_2[:,0], self.RC_max_2[:,1],
                                color='C4', alpha=0.2, label='EARL 2')
        plt.xlabel('Sphere Diameter (mm)',fontsize = 16)
        plt.plot(x,y,linestyle='--',color='gray')
        plt.ylabel('RC Max', fontsize = 16)
        plt.ylim(0.4,1.6)
        plt.legend(fontsize = 12,loc='lower right')
        plt.title(self.title + ' RC Max',fontsize=16)
        plt.show()

    
    def COV(self,xaxis,axis_title):

        sns.set_style("white")
        #sns.set_palette("husl")
        plt.figure(figsize=(8,7))

        for RC,recon,x in zip(self.RCs,self.recons,xaxis):
            plt.errorbar(x,RC.COV,yerr=RC.COV_error, marker='o',label=recon)

        plt.ylabel('COV',fontsize=16)
        plt.xlabel(axis_title,fontsize=16)
        plt.legend(fontsize = 12)
        plt.title(self.title + ' Background COV',fontsize=16)
        plt.show()
    
    def noise(self):
        cov = []
        for RC in self.RCs:
            cov.append(RC.COV)

        return cov
    
    def bias(self): #1 - SUV mean Mean contrast recovery 
        mcr_bias = []
        for RC in self.RCs:
            mcr_bias.append(1-RC.MCR_mean)

        return mcr_bias

    # Noise vs Bias plots

    def cov_v_mcr(self): #nvb = CoV (noise) vs MCR (average SUV mean bias of all 6 spheres)

        cov = []
        mcr_bias = []
        for RC in self.RCs:
            cov.append(RC.COV)
            mcr_bias.append(1-RC.MCR_mean)

        sns.set_style("white")
        plt.figure(figsize=(8,7))

        plt.plot(cov,mcr_bias)

        plt.xlabel('Noise (COV)',fontsize=16)
        plt.ylabel('Bias (SUV mean)',fontsize=16)
        plt.title(self.title + ' MCR bias vs COV',fontsize=16)
        plt.show()

    def cov_v_max_mcr(self):

        cov = []
        mcr_bias = []
        for RC in self.RCs:
            cov.append(RC.COV)
            mcr_bias.append(1-RC.MCR_max)

        sns.set_style("white")
        plt.figure(figsize=(8,7))

        plt.plot(cov,mcr_bias)

        plt.xlabel('Noise (COV)',fontsize=16)
        plt.ylabel('Bias (SUV max)',fontsize=16)
        plt.title(self.title + ' MCR max bias vs COV',fontsize=16)
        plt.show()