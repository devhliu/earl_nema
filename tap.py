from earl_nema import NemaRC
import pydicom
from pydicom.tag import Tag
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit
import pandas as pd 



def power_law(x,a,b):
    return a*x**(-b)

def cov_power_fit(time,cov,err):
    '''
    Parameters:
        time: array
            array of scan durations
        cov: array
            array containing COV data
        err: array
            array containing error in COV data
    Returns:
        a,b: floats
            fit parameters for power law fit of COV vs scan duration
    '''

    popt, pcov = curve_fit(power_law, time, cov,p0=[1,0.5],sigma=err)
    a = popt[0]
    b = popt[1]

    # plt.plot(time,power_law(time, *popt),linestyle='--',label='fit')
    # plt.errorbar(time,cov,yerr=err,marker='p',linestyle='',label='data')
    # plt.legend()
    # plt.show()
    # print(popt)

    return a,b

def tap(a,b,cov_max,b_true):
    '''
    Parameters:
    a (float): Power law fit parameter
    b (float): Power law fit exponential parameter
    cov_max (float): threshold for noise
    b_true (float): true background activity concentration in kBq/mL

    Returns:
    activityOpt: dict
        a dictionary with the following keys:
            tap (float): Minimum time activity product (MBq*s/kg)
            tmin (float): Minimum scan duration in seconds
    '''
    activityOpt = {}

    tmin = (a/cov_max)**(1/b)*b_true/2.0 #2.0 is the 'standard' activity concentration for the background in kBq/mL
    tap = tmin*300/75 #minimum scan duration in seconds multiplied by 300 MBq per 75 kg patient

    activityOpt['tmin'] = tmin
    activityOpt['tap'] = tap
    
    return activityOpt


class activityOpt: 

    def __init__(self,recon,filters,sphere_true = 19.69,bkg_true = 1.94):
        '''
        Parameters:
        recon (str): Reconstruction type to analyze
        filters (list of str): filter types to analyze
        sphere_true (float): activity concentration of spheres in kBq/mL
        bkg_true (float): activity concentration of background in kBq/mL
        '''

        self.recon = recon
        self.title = recon.replace('_',' ')
        self.filters = filters
        self.bkg_true = bkg_true
        self.scan_duration = np.array([19,38,75,150,300,450,600])

        recon_dir = '/Users/alexanderhart/DiscoveryMI/'
        time_dirs = ['19s','38s','75s','2p5m','5m','7p5m','10m']
        

        #analyze each of the reconstructions with NemaRC
        recon_analysis = []
        for f in filters:
            filter_analysis = []
            for time in time_dirs:
                if f=='None':
                    a = NemaRC(recon_dir+time+'/'+recon,sphere_true,0)
                    filter_analysis.append(a)
                else:
                    a = NemaRC(recon_dir+time+'/'+recon+'_'+f+'mm_fwhm',sphere_true,0)
                    filter_analysis.append(a)
            recon_analysis.append(filter_analysis)

        #extract the cov data from each of the NemaRC objects
        self.cov = []
        self.cov_err = []
        for f in recon_analysis:
            noise = []
            noise_err = []
            for time in f:
                noise.append(time.COV)
                noise_err.append(time.COV_error)
            self.cov.append(noise)
            self.cov_err.append(noise_err)

    def tap_plot(self):
        plt.figure(figsize=(9,6))
        color_list = sns.husl_palette(len(self.filters))
        
        i = 0
        for cov,cov_err,f in zip(self.cov,self.cov_err,self.filters):
            #calculate the fit of the cov vs scan duration data and the time activity product (tap)
            a,b= cov_power_fit(self.scan_duration,cov,cov_err)
            Opt = tap(a,b,0.15,1.94)
            product = Opt['tap']
            print(f,'Tmin: ',round(Opt['tmin'],2),'s',' TAP: ',round(product,2),'s*MBq/kg')
            clinical_duration = np.array([120,150,180,210,240])
            act_per_weight = product/clinical_duration

            if f =='None':
                plt.plot(clinical_duration/60,act_per_weight,linestyle='--',color=color_list[i], marker='p',label='No Filter')
            else:
                plt.plot(clinical_duration/60,act_per_weight,linestyle='--',color=color_list[i], marker='p',label=f+'mm')
            i+=1
            

        plt.ylabel('Injected Activity/Weight (MBq/kg)',fontsize=16)
        plt.xlabel('Time per bed position (min)',fontsize=16)
        plt.legend(fontsize = 12)
        plt.title(self.title,fontsize=16)
        plt.show()


    def COV_plot(self):

        sns.set_style("white")
        #sns.set_palette("husl")
        color_list = sns.husl_palette(len(self.filters))
        plt.figure(figsize=(8,7))

        scan_duration = [19,38,75,150,300,450,600]

        i=0
        for cov,cov_err,f in zip(self.cov,self.cov_err,self.filters):
            a,b= cov_power_fit(scan_duration,cov,cov_err)
            plt.plot(scan_duration,power_law(scan_duration,a,b),linestyle='--',color=color_list[i])
            if f =='None':
                plt.errorbar(scan_duration,cov,yerr=cov_err,color=color_list[i], marker='p',linestyle='',label='No Filter')
            else:
                plt.errorbar(scan_duration,cov,yerr=cov_err,color=color_list[i], marker='p',linestyle='',label=f+'mm')
            i+=1
            
        threshold = []
        for t in scan_duration:
            threshold.append(0.15)
        plt.plot(scan_duration,threshold,linestyle = 'dashed',color='gray',label='threshold')
        plt.ylabel('COV',fontsize=16)
        plt.xlabel('scan duration (s)',fontsize=16)
        plt.legend(fontsize = 12)
        plt.title(self.title,fontsize=16)
        plt.show()






