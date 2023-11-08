#############################################
#
#   Store pythia events
#
#############################################
import math
import numpy as np
import GParticle as GP

class GEvent:
    def __init__(self):
        self.EventNum = -1     #Event Number
        self.NA = 0.0          #Atomic Number of Nucleus A
        self.NB = 0.0          #Atomic Number of Nucleus B
        self.sqrts = 0.0       #[GeV]center of mass collision energy

        self.weight = 0.0      #total PYTHIA weight calculated for this event
        self.sigmaGen = 0.0    #PYTHIA-computed cross-section for this event
        self.ptHatMin = 0.0    #minimum ptHat for this event (will vary)
        self.ptHat = 0.0       #transverse momentum in the rest frame of a 2->2 processes (for the initial hard scattering?)
        self.thetaHat = 0.0    #polar scattering angle in the rest frame of a 2->2 processes (for the initial hard scattering?)
        self.phiHat = 0.0      #azimuthal scattering angle in the rest frame of a 2->2 processes (for the initial hard scattering?)

        self.psiRP = 0.0       # the impact parameter angle. (reaction plane?)
        self.sigmaTot = 0.0    # the total cross section from the Glauber calculation in millibarns.

        self.nJets = 0         #number of jets found by some jet finder

        self.b = 0.0       #[fm] impact parameter
        self.Ncoll = 0.0   #number of binary nucleon collisoins
        self.Npart = 0.0   #number of participating nuclleons

        self.Particles = ([])#array of GParticles

    # create a function that appends the array of particles
    # and makes sure they are all of type GParticle
    def AddParticle(self, prt:GP):
        #if not isinstance(prt, GP):
            #raise TypeError
        self.Particles.append(prt)


