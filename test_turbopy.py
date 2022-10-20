import turbopy
import sys, os
import numpy as np


os.environ['TURBODATA']='/home/pthibodeaux/stellar_spectra/Turbospectrum_NLTE/DATA'

sys.path.append('/home/pthibodeaux/stellar_spectra/Turbospectrum_NLTE/exec/')

wmin, wmax, dwl = 6700, 6720, 0.1
ll=turbopy.TSLineList('/home/pthibodeaux/stellar_spectra/turbopy/turbospec.20180901t20.linedata')
atmo=turbopy.MARCSModel.load('/home/pthibodeaux/stellar_spectra/Turbospectrum_NLTE/COM/s5000_g+2.0_m1.0_t02_ae_z-1.50_a+0.66_c+0.00_n+0.00_o+0.66_r+0.00_s+0.00.mod')

wave,norm,flux = turbopy.run_synth(wmin,wmax,dwl,[12.0,0.4],[6.0,0.5],[8.0,0.5],atmosphere=atmo,vt=1.0,linelist=ll,outfname="sun-6700-6720.tar.gz",Hlinelist="/home/pthibodeaux/stellar_spectra/turbopy/turbospec.20180901t20.Hlinedata",marcsfile=False)
