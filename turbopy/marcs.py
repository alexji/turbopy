from __future__ import absolute_import, division, print_function

import os
import numpy as np
## from Ivanna Escala
from .interp_marcs import interp_marcs, construct_model_filename

# This probably doesn't work if you install the package
data_path = os.path.join(__file__, 'data')

# Have to have the full MARCS grid somewhere
marcs_model_directory = "/project2/alexji/MARCS"

def load_atmosphere(Teff, logg, MH, vt,
                    aFe=None, CFe=None, NFe=None,
                    rFe=None, sFe=None):
    """
    Directly loads a MARCS model within the grid with no interpolation
    """
    raise NotImplementedError

def interp_atmosphere(Teff, logg, MH, vt, aFe,
                      output_directory,
                      input_directory=marcs_model_directory,
                      **kwargs):
    """
    Uses the Masseron interpolator to get a new MARCS model
    Give it Teff, logg, MH, vt, aFe and it creates a new file in output_directory then returns the filename
    Note that vt is not actually interpolated, just used for the filename and keeping it in here just in case
    """
    if vt != 2.0: print("vt is not being interpolated in the model atmosphere, defaulting to 2")
    outfname = interp_marcs(Teff, logg, MH, aFe,
                            micro_turb_vel=2,
                            output_model_path=output_directory,
                            input_model_path=input_directory,
                            extrapol=True,
                            **kwargs
    )
    return outfname

class MARCSModel(object):
    def __init__(self, fname=None):
        super(MARCSModel, self).__init__()
        assert fname is None or os.path.exists(fname)
        self.fname = fname
        spherical, Teff, logg, mass, vt, descr, MH, aFe, CFe, NFe, OFe, rFe, sFe = self.get_stellar_params_from_filename(fname)
        self.spherical = spherical
        self.Teff = Teff
        self.logg = logg
        self.mass = mass
        self.vt = vt
        self.descr = descr
        self.MH = MH
        self.aFe = aFe
        self.CFe = CFe
        self.NFe = NFe
        self.OFe = OFe
        self.rFe = rFe
        self.sFe = sFe

    @staticmethod
    def load(fname, validate=False):
        assert os.path.exists(fname), fname
        atmo = MARCSModel(fname)
        if validate: raise NotImplementedError
        return atmo
    
    @staticmethod
    def get_stellar_params_from_filename(fname):
        assert os.path.exists(fname), fname
        bname = os.path.basename(fname)
        s = bname.split("_")
        
        assert s[0][0] in ["s","p"], s[0][0]
        spherical = s[0][0]=="s"
        Teff = float(s[0][1:])
        
        assert s[1][0] == "g"
        logg = float(s[1][1:])
        
        assert s[2][0] == "m" # pretty much always 1.0
        mass = float(s[2][1:])
        
        assert s[3][0] == "t" # should be t0, t02, t05
        vt = float(s[3][1:])

        descr = s[4]
        
        assert s[5][0]=="z"
        MH = float(s[5][1:])
        
        assert s[6][0]=="a"
        aFe = float(s[6][1:])
        
        assert s[7][0]=="c"
        CFe = float(s[7][1:])
        
        assert s[8][0]=="n"
        NFe = float(s[8][1:])

        assert s[9][0]=="o"
        OFe = float(s[9][1:])

        assert s[10][0]=="r"
        rFe = float(s[10][1:])
        
        assert s[11][0]=="s"
        ss = s[11].split(".") # e.g. s+0.00.mod
        sFe = float(ss[0][1:])

        return spherical, Teff, logg, mass, vt, descr, MH, aFe, CFe, NFe, OFe, rFe, sFe
    
    def get_fname(self):
        return self.fname
    
    @property
    def Teff(self):
        return self._Teff
    @Teff.setter
    def Teff(self, x):
        self._Teff = x
    
    @property
    def logg(self):
        return self._logg
    @logg.setter
    def logg(self, x):
        self._logg = x
    
    @property
    def MH(self):
        return self._MH
    @MH.setter
    def MH(self, x):
        self._MH = x
    
    @property
    def aFe(self):
        return self._AM
    @aFe.setter
    def aFe(self, x):
        self._AM = x    
    @property
    def AM(self):
        return self._AM
    @AM.setter
    def AM(self, x):
        self._AM = x
    
    @property
    def spherical(self):
        return self._spherical
    @spherical.setter
    def spherical(self, x):
        assert isinstance(x, bool)
        self._spherical = x
