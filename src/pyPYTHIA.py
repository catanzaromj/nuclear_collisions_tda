# George's trial code for generating pythia events

# To set the path to the Pythia 8 Python interface do either
# (in a shell prompt):
#      export PYTHONPATH=$(PREFIX_LIB):$PYTHONPATH
# or the following which sets the path from within Python.
import time
start_time = time.time()
import math
import sys
lib = "/media/moschelli/scratch1/pythia_python/env/lib"
sys.path.insert(0, lib)
# Import the Pythia module.
import pythia8
import GParticle as GP
import GEvent as GE
import pickle

# take parameters from configuration file (bash shell script)
nEvent = int(sys.argv[1]) # set the number of events to generate
sqrts = float(sys.argv[2]) # [GeV] per nucleon center of mass energy

# set  Beams:idA and Beams:idB
idA = int(sys.argv[3])
idB = int(sys.argv[4])

# kinimatic cut of hard scatterings at generation level [GeV]
ptHatMin = float(sys.argv[5])
ptHatMax = float(sys.argv[6])

out_path = sys.argv[7] #location to place file with pythia events
filename = sys.argv[8] # the name of the file that stores final events

# initialize a pythia8 object
pythia = pythia8.Pythia()

# settings for collision types
pythia.readString(sys.argv[9]) #readString("SoftQCD:nonDiffractive = on");//used to be called minBias// default = off
pythia.readString(sys.argv[10]) #readString("SoftQCD:elastic = off");// elastic collisions //default = off
pythia.readString(sys.argv[11]) #readString("SoftQCD:singleDiffractive = off");//default = off
pythia.readString(sys.argv[12]) #readString("SoftQCD:doubleDiffractive = on");//default = off
pythia.readString(sys.argv[13]) #readString("SoftQCD:centralDiffractive = on");//default = off// this may have double pomeron exchange in it


# switch on all QCD jet + jet processes
# message from pytia online http://home.thep.lu.se/~torbjorn/pythia81html/QCDProcesses.html
# This group contains the processes for QCD jet production above some minimum pT threshold.
# The pT_min cut cannot be put too low, or else unreasonably large jet cross sections will be obtained.
# This is because the divergent perturbative QCD cross section is used in this process group, without any regularization modifications.
# An eikonalized description, intended to be valid at all pT, is instead included as part of the multiparton-interactions framework,
# specifically in SoftQCD:nonDiffractive above.
# Warning 1: you must remember to set the PhaseSpace:pTHatMin value if you use any of these processes;
# there is no sensible default.
# Warning 2: you must not mix processes from the SoftQCD and HardQCD process groups, since this is likely to lead to double-counting.
pythia.readString(sys.argv[14]); #readString("HardQCD:all = off");//default = off

#set ptHat
pythia.readString("PhaseSpace:pTHatMin = " + str(ptHatMin))
pythia.readString("PhaseSpace:pTHatMax = " + str(ptHatMax))

# No event record printout.
pythia.readString("Next:numberShowInfo = 0")
pythia.readString("Next:numberShowProcess = 0")
pythia.readString("Next:numberShowEvent = 0")

# for pPb
#pythia.readString("Tune:pp = 8")
#pythia.readString("SigmaProcess:Kfactor = 0.7") # not sure what this does

# random seed
# A negative value gives the default seed,
# a value 0 gives a random seed based on the time
# a value between 1 and 900,000,000 a unique different random number sequence
pythia.readString("Random:setSeed = on")
pythia.readString("Random:seed = 0")

# beam initialization.
#pythia.readString("Beams:idA = 2212") # proton = 2212
#pythia.readString("Beams:idB = 2212") # proton = 2212
pythia.readString("Beams:idA = " + str(idA))
pythia.readString("Beams:idB = " + str(idB))
pythia.readString("Beams:eCM = " + str(sqrts))

# initialize pythia
pythia.init()
#help(pythia)
#help(pythia.infoPython())
#help(pythia.heavyIonsPtr)
#help(pythia.heavyIonsPtr.hiInfo())

# kinematic cuts
ptmin = 0.15 # [GeV] minimum transverse momentum
ptmax = 2.0 # [GeV] maximum transverse momentum
ymin = -1.0 # rapidity min
ymax = 1.0 # rapidity max
etamin = -1.0 #pseudorapidit min
etamax = 1.0 #pseudorapidity max

c = 1 #pythia uses natural units #c=299792458. # [m/s] speed of light in vacuum

neve = 0 # counter for number of accepted events
mult = 0 # total multiplicity of all accepted events
pt_tot = 0.0 #total transverse momentum for all accepted events


#ffile=open(out_path+"fuckoff.txt", 'w+') #open file

evtList = ([]) # will store a list of GEvent objects
###########################################################################
#   EVENT LOOP
###########################################################################
for iEvent in range(0, nEvent):
    if not pythia.next(): continue # skip unsuccessfull events

    event = GE.GEvent() # initialie a GEvent event
    event.EventNum = iEvent
    event.ptHatMin = ptHatMin
    #
    # event information
    #
    event.sqrts = pythia.infoPython().eCM() # [GeV] center of mass collision energy
    event.weight = pythia.infoPython().weight()# event weight needed to scale event averages for pythia settings that overproduce rare processes
    event.sigmaGen = pythia.infoPython().sigmaGen() #cross section adjustment related to event weighting
    #
    # the following might not be relevant for softQCD
    # see "Soft Diffraction" in https://pythia.org/latest-manual/EventInformation.html
    event.ptHat = pythia.infoPython().pTHat() #transverse momentum in the rest frame of a 2->2 processes (for the initial hard scattering?)
    event.thetaHat = pythia.infoPython().thetaHat() #polar scattering angle in the rest frame of a 2->2 processes (for the initial hard scattering?)
    event.phiHat = pythia.infoPython().phiHat() #azimuthal scattering angle in the rest frame of a 2->2 processes (for the initial hard scattering?)


    #set atomic numbers
    #
    # protons
    if idA == 2212: event.NA = 1
    if idB == 2212: event.NB = 1
    # neutrons
    if idA == 2112: event.NA = 1
    if idB == 2112: event.NB = 1
    # deuterons
    if idA == 1000010020: event.NA = 2
    if idB == 1000010020: event.NB = 2
    # helium
    if idA == 1000020040: event.NA = 4
    if idB == 1000020040: event.NB = 4
    # lithium
    if idA == 1000030060: event.NA = 6
    if idB == 1000030060: event.NB = 6
    # carbon
    if idA == 1000060120: event.NA = 12
    if idB == 1000060120: event.NB = 12
    # oxygen
    if idA == 1000080160: event.NA = 16
    if idB == 1000080160: event.NB = 16
    # copper
    if idA == 1000290630: event.NA = 63
    if idB == 1000290630: event.NB = 63
    # krypton
    if idA == 1000360840: event.NA = 84
    if idB == 1000360840: event.NB = 84
    # xenon
    if idA == 1000541290: event.NA = 129
    if idB == 1000541290: event.NB = 129
    # gold
    if idA == 1000791970: event.NA = 197
    if idB == 1000791970: event.NB = 197
    #
    if idA == 1000822080: event.NA = 208
    if idB == 1000822080: event.NB = 208


    #
    #   if heavy ion collision or pA collision
    #   HeavyIons member functions found at
    #   https://pythia.org/latest-manual/HeavyIons.html
    #
    #   for python pythia.info was replaced by pythia.infoPythia()
    #   I don't think this was miplimented for hiInfo
    #   there is no replacement for pythia.info.hiinfo
    #
    #   the best I could find is pythia.heavyIonsPtr.hiInfo()
    #   this throws the error:
    #   TypeError: Unable to convert function return value to a Python type!
    #
#    if idA > 9999 or idB > 9999:

        ##event.b = pythia.info.hiinfo.b() #C++ way doesn't work
        ##event.b = pythia.infoPython().hiinfo.b() #also doesn't work

        #found the below method of heavyIonsPtr.hiInfo() by using the help() command
        #but get the error that
#        event.b = pythia.heavyIonsPtr.hiInfo().b() #the impact parameter in femtometers.
#        event.psiRP = pythia.heavyIonsPtr.hiInfo().phi() # the impact parameter angle.
#        event.sigmaTot = pythia.heavyIonsPtr.hiInfo().sigmaTot() # the total cross section from the Glauber calculation in millibarns.

#        event.Ncoll = pythia.heavyIonsPtr.hiInfo().nCollTot() #the number of separate sub-collisions in the current event.

#        event.Npart = pythia.heavyIonsPtr.hiInfo().nPartProj() + pythia.heavyIonsPtr.hiInfo().nPartTarg() #number of participating nuleons

    #
    # end heavy ion condition


    n_ch_ev = 0 #counts number of charged particles for this event
    pt_tot_ev = 0.0 #sums the total transverse momentum for this event

    #----------------------------------------------------------------------
    #   PARTICLE LOOP
    #----------------------------------------------------------------------
    for prt in pythia.event:

        particle = GP.GParticle() # initialize a GParticle object to add to GEvent event object

        # particle information, look here: https://pythia.org/latest-manual/ParticleProperties.html
        particle.pid_PDG = prt.id() #id number following Particle Data Group codes
        particle.status = prt.status() # status codes listed here: https://pythia.org/latest-manual/ParticleProperties.html
        particle.px = prt.px() #[GeV/c] x-momentum
        particle.py = prt.py() #[GeV/c] y-momentum
        particle.pz = prt.pz() #[GeV/c] z-momentum = mt*c^2*sinh(y)
        particle.pt = prt.pT() #[GeV/c] transverse momentum = sqrt(px*px+py*py)
        particle.p = math.sqrt(prt.px()*prt.px() + prt.py()*prt.py() + prt.pz()*prt.pz()) #[GeV/c] momentum magnitude
        particle.E = prt.e() #[GeV] energy = sqrt((mass*c^2)^2 + (p*c)^2) = mt*c^2*cosh(y)
        particle.y = prt.y() #rapidity = 0.5*ln((E+pz*c)/(E-pz*c))
        particle.eta = prt.eta() #pseduorapidity = 0.5*ln((p+pz)/(p-pz))
        particle.phi = prt.phi() #azimuthal angle (angle of pt with x-axis)
        particle.mass = prt.m()  #[GeV/c^2] mass probably in GeV/c^2
        particle.mT = prt.mT() # transverse mass = sqrt((pt/c)*(pt/c) + mass*mass)
        particle.ET = prt.eT() # transverse energy = sqrt((mass*c^2)^2 + (pt*c)^2)
        particle.charge = prt.charge() #electrical charge probably in fractions of e
        #particle.I3 = prt.I3() #2*I3: isospin z-projection (doubled)
        particle.theta = prt.theta() # polar angle, not sure if it's spatial angle or momentum angle

        # angle in the (p_x, p_z) plane, between -pi and +pi, with 0 along the +z axis
        # this should be related to pseudorapidity, need to check
        particle.thetaXZ = prt.thetaXZ()

        #polarization/spin/helicity = cos of angel between spin and 3-momentum vector
        #check info at https://pythia.org/latest-manual/ParticleProperties.html
        particle.pol = prt.pol()

        #production vertex coordinates in [mm]
        particle.xProd = prt.xProd()
        particle.yProd = prt.yProd()
        particle.zProd = prt.zProd()
        particle.tProd = prt.tProd() #time [mm/c]

        particle.tau = prt.tau() # [mm/c] proper lifetime

        # add final particles to saved event
        if prt.isFinal(): event.AddParticle(particle)

        #
        #   ACCEPTANCE CONDITIONS
        #
        if prt.isFinal() \
            and prt.isCharged() \
            and prt.pT() > ptmin and prt.pT() <= ptmax \
            and prt.y() >= ymin and prt.y() <= ymax \
            and prt.eta() >= etamin and prt.eta() <= etamax:

            #ffile.write(str(prt.status())+"\t"+str(prt.id())+"\t"+str(prt.charge())+"\t"+str(prt.pT())+ "\t"+str(prt.y())+"\t"+str(prt.eta())+"\n")

            n_ch_ev += 1
            pt_tot_ev += prt.pT()

        #
        #   END ACCEPTANCE CONDITIONS
        #
    #----------------------------------------------------------------------
    #   END PARTICLE LOOP
    #----------------------------------------------------------------------

    evtList.append(event) # add event to list


    #
    #if particles are accepted then count this event
    #
    if n_ch_ev > 0:

        #ffile.write("Event\t"+str(iEvent)+ "\t"+str(n_ch_ev)+ "\n")

        neve += 1
        mult += n_ch_ev
        pt_tot += pt_tot_ev

###########################################################################
#   END EVENT LOOP
###########################################################################
#ffile.close()

#
#   calculate some stuff
#   normally I don't calculate things in the event generator code
#
avg_N = mult/neve
avg_pt_tot = pt_tot/neve
avg_pt = avg_pt_tot/avg_N

print('\n\n')
print(sqrts, "\t [GeV] center of mass collision energy")
print(idA, "\t projectile ID number")
print(idB, "\t target ID number")
print(ptmin, "\t [GeV] pt min")
print(ptmax, "\t [GeV] pt max")
print(ymin, "\t rapidity min")
print(ymax, "\t rapidity max")
print(etamin, "\t pseudorapidity min")
print(etamax, "\t pseudorapidity max")
print(nEvent, "\t events generated")
print(neve, "\t events accepted")
print(avg_N, "\t average multiplicity per event")
print(avg_pt_tot, "\t [GeV] average total transverse moemtum per event")
print(avg_pt, "\t [GeV] average transverse momentum per particle")

#write events to pickle file
file=open(out_path+filename+".pickle", 'wb') #open file
pickle.dump(evtList, file)
file.close() # close file

print("\n\nRun time: %s seconds" % (time.time()-start_time))
