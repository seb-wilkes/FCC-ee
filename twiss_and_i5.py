#%%
import os
import numpy as np
# Require an efficient way to move through an iterable list
import itertools  
#%%
class twiss_functions():
    """
    This class calculates the twiss parameters as required. It also includes a function to calculate the 
    5th Synchrotron Integral by extracting the relevant bending Radii.
    Lastly, included is a function to calculate BMag.
    """
    def __init__(self, location=''):
        self.root = '/home/sebw/madx/cern/fcc_ee_stuff/' + location
        os.chdir(self.root) # can comment out if preferred
        self.data = {}
        self.check_flag = False
    
    def file_search_boundaries(self, reference_flag=True):
        ''' 
        Edit values as appropriate
        reference_flag refers to if checking the reference file, or a standard output file 
        (which have different lengths)
        '''
        if reference_flag:
            line_start = 1
            line_end = 569
        else:
            line_start = 1
            line_end = 3097
        return line_start,line_end
        
    def get_bending_names(self, directory, reference_flag=True):
        ''' It searches within: cwd + directory + "/full_sequence.seq"'''
        
        line_start, line_end = self.file_search_boundaries(reference_flag)
        with open(directory + '/full_sequence.seq') as f:
            iterable = itertools.islice(f, line_start, line_end)
            for line in iterable:
                # process lines                
                if line[1]=='b':
                    # Extract name and dipole magnet length
                    line_split = line.split()
                    bend_name = line_split[0][1:]
                    self.data[bend_name] = {"l":0.0,"a":0.0, "R":0.0}
                    self.data[bend_name]["l"] = float(line_split[2][:-1])
                    # Now extract bending angle
                    line = next(iterable)
                    self.data[bend_name]["a"] = float(line_split[2][:-1])
                    # Calculate radius from component values; using absolute to ignore direction
                    self.data[bend_name]["R"] = np.abs(\
                        self.data[bend_name]["l"]/(2*np.sin(0.5*self.data[bend_name]["a"])))
        self.check_flag = True

    def update_radii(self, directory, dipoles, bending_radii, force = False):
        ''' Tool used to generate radii array '''
        if force or not self.check_flag:
            self.get_bending_names(directory)
        for i in range(0, len(dipoles)):
            bending_radii[i] = self.data[dipoles.index[i].split(sep='.')[0].lower()]["R"]
    
    def gamma_twiss(self, alfa, beta):
        return (1+alfa**2)/beta

    def curly_H(self, alpha, beta, disp_x, disp_px):
        gamma_H = self.gamma_twiss(alpha, beta)
        dpx = (disp_px - alpha*disp_x)/beta #transforming MADX units
        H = gamma_H*disp_x**2+2*alpha*disp_x*dpx+beta*dpx**2
        return H

    def compute_I5(self, alpha, beta, disp_x, disp_px, radii, s):
        delta_s = np.roll(s,-1) - s
        delta_s[-1] += 9.51459240451159e+04 #This is the circumference of the FCC
        return np.sum(1.0/(radii**3)* \
            self.curly_H(alpha, beta, disp_x, disp_px)*delta_s)

    def b_mag(self, a_o, b_o, a_m, b_m):
        '''
        _o suffix is the original (reference) lattice
        _m is the machine to be tested
        '''
        # First noramlise the coordianate
        beta_norm = b_m/b_o
        alpha_norm = beta_norm*a_o + a_m
        gamma_norm = self.gamma_twiss(alpha_norm,beta_norm)
        #Now calculate BMag 
        # (or M, according to Matthew Sands:
        # https://lib-extopc.kek.jp/preprints/PDF/1991/9105/9105527.pdf )
        M = 0.5*(beta_norm + gamma_norm + np.sqrt(((beta_norm+gamma_norm)**2)-4))
        return M
