#############################################
#
#   Store pythia particle information
#
#############################################
import math
import numpy as np

class GParticle:
    def __init__( self ):
        self.pid_PDG = 0    #particle-ID PDG
        self.status = 0     #status codes listed here: https://pythia.org/latest-manual/ParticleProperties.html
        # pythia uses speed of light c=1 in natural units
        self.px = 0.0       #[GeV/c] x-momentum
        self.py = 0.0       #[GeV/c] y-momentum
        self.pz = 0.0       #[GeV/c] z-momentum
        self.pt = 0.0       #[GeV/c] transverse momentum
        self.p = 0.0        #[GeV/c] momentum magnitude
        self.E = 0.0        #[GeV] energy
        self.y = 0.0        #rapidity
        self.eta = 0.0      #pseduorapidity
        self.phi = 0.0      #azimuthal angle (angle of pt with x-axis?)
        self.mass = 0.0     #[GeV/c^2] mass
        self.mT = 0.0       #transverse mass
        self.ET = 0.0       #transverse energy
        self.charge = 0.0   #electrical charge probably in fractions of e
        self.theta = 0.0    #polar angle, not sure if it's spatial angle or momentum angle
        self.thetaXZ = 0.0
        self.pol = 0.0
        #production vertex coordinates in [mm]
        self.xProd = 0.0
        self.yProd = 0.0
        self.zProd = 0.0
        self.tProd = 0.0    #time [mm/c]
        self.tau = 0.0      #[mm/c] proper lifetime

        self.JetNumber = 0  #index indicating which jet this particle belongs to, if JetNumber == 0 this particle is not in a jet (or has not been assigned yet)
