from earl_nema import NemaRC
import pydicom
from pydicom.tag import Tag
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class reconComp():

    def __init__(self, nemaAnalyze):


        ''' Comparison of two different reconstruction types (i.e. OSEM and Q.Clear)

        Parameters:
        nemaAnalyze (list): List containing analyzed NEMA objects from both recon types
        algorithms (list): List containing strngs with the recon types of both reconstructions
        being compared
        '''
        self.nemaAnalyze = nemaAnalyze
        #self.algorithms = algorithms
        self.algorithms  = []
        for nema in nemaAnalyze:
            self.algorithms.append(nema.title)
        sns.set_palette("husl")
    
    # Noise vs Bias plots

    def cov_mcr(self):
        
        sns.set_style("white")
        plt.figure(figsize=(8,7))

        for recon, algo in zip(self.nemaAnalyze,self.algorithms):

            plt.plot(recon.noise(),recon.bias(),marker=None,label = algo)
            #plt.gray()
            plt.scatter(recon.noise(),recon.bias(),c=recon.noise(),s=50,marker='o',cmap='Greys',edgecolors='black')
            for txt, noise, bias in zip(recon.recons,recon.noise(),recon.bias()):
                plt.annotate(txt,(noise,bias))


        plt.xlabel(r'Noise ($\%$ CoV)',fontsize=16)
        plt.ylabel(r'Bias (mean $\%$ recovery)',fontsize=16)
        plt.legend(fontsize = 12,loc='lower right')
        plt.title('MCR Mean Bias vs COV',fontsize=16)
        plt.show()

    def cov_mcr_max(self):
        
        sns.set_style("white")
        plt.figure(figsize=(8,7))

        for recon, algo in zip(self.nemaAnalyze,self.algorithms):

            plt.plot(recon.noise(),recon.max_bias(),marker='o',label = algo)


        plt.xlabel(r'Noise ($\%$ CoV)',fontsize=16)
        plt.ylabel(r'Bias (Max $\%$ recovery)',fontsize=16)
        plt.legend(fontsize = 12,loc='lower right')
        plt.title('MCR Max Bias vs COV',fontsize=16)
        plt.show()

    def rmse_mean(self):
        ''' Mean Squared Error of RC mean: MSE = RCmean Bias^2 + CoV^2
        '''
        sns.set_style("white")
        plt.figure(figsize=(9,16))

        for recon, algo in zip(self.nemaAnalyze,self.algorithms):
            noise = np.array(recon.noise())/100
            bias = np.array(recon.bias())/100
            rmse = np.sqrt((noise**2+bias**2))*100
            xaxis = [algo]*len(rmse)
            plt.plot(xaxis,rmse,marker='p',linestyle='')
            for err,txt in zip(rmse,recon.recons):
                plt.annotate(txt,(algo,err))

        plt.xlabel(r'Reconstruction Type',fontsize=16)
        plt.ylabel(r'RMSE - $\sqrt{Mean Bias^2+COV^2}$',fontsize=16)
        #plt.legend(fontsize = 12,loc='lower right')
        #plt.title('RMSE of RC Mean Bias and COV',fontsize=16)
        plt.show()

    def rmse_max(self):
        ''' Mean Squared Error of RC mean: MSE = RCmean Bias^2 + CoV^2
        '''
        sns.set_style("white")
        plt.figure(figsize=(9,16))

        for recon, algo in zip(self.nemaAnalyze,self.algorithms):
            noise = np.array(recon.noise())/100
            max_bias = np.array(recon.max_bias())/100
            rmse = np.sqrt((noise**2+max_bias**2))*100
            xaxis = [algo]*len(rmse)
            plt.plot(xaxis,rmse,marker='p',linestyle='')
            for err,txt in zip(rmse,recon.recons):
                plt.annotate(txt,(algo,err))

        plt.xlabel(r'Reconstruction Type',fontsize=16)
        plt.ylabel(r'RMSE - $\sqrt{Max Bias^2+COV^2}$',fontsize=16)
        #plt.legend(fontsize = 12,loc='lower right')
        #plt.title('RMSE of RC Mean Bias and COV',fontsize=16)
        plt.show()

    #def cov_time(self):



    