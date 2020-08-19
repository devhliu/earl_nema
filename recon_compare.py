from earl_nema import NemaRC
import pydicom
from pydicom.tag import Tag
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class reconComp():

    def __init__(self, nemaAnalyze, algorithms, title):


        ''' Comparison of two different reconstruction types (i.e. OSEM and Q.Clear)

        Parameters:
        nemaAnalyze (list): List containing analyzed NEMA objects from both recon types
        algorithms (list): List containing strngs with the recon types of both reconstructions
        being compared
        '''
        self.nemaAnalyze = nemaAnalyze
        self.algorithms = algorithms
        self.title = title
        sns.set_palette("husl")
    
    # Noise vs Bias plots

    def cov_mcr(self):
        
        sns.set_style("white")
        plt.figure(figsize=(8,7))

        for recon, algo in zip(self.nemaAnalyze,self.algorithms):

            plt.plot(recon.noise(),recon.bias(),label = algo)


        plt.xlabel('Noise (CoV)',fontsize=16)
        plt.ylabel('Bias (SUV mean)',fontsize=16)
        plt.legend(fontsize = 12,loc='upper right')
        plt.title(self.title + ' MCR bias vs COV',fontsize=16)
        plt.show()