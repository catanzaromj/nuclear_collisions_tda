import time
start_time = time.time()
import math
import GParticle as GP
import GEvent as GE
import pickle

# kinematic cuts
ptmin = 0.15 # [GeV] minimum transverse momentum
ptmax = 2.0 # [GeV] maximum transverse momentum
ymin = -1.0 # rapidity min
ymax = 1.0 # rapidity max
etamin = -1.0 #pseudorapidit min
etamax = 1.0 #pseudorapidity max

sqrts = 0 # [GeV] center of mass collision energy
NA = 0 # atomic number of nucleus A
NB = 0 # atomic number of nucleus B

neve = 0 # counter for number of accepted events
mult = 0 # total multiplicity of all accepted events
pt_tot = 0.0 #total transverse momentum for all accepted events

# open event.pickle file
file = open('/home/moschelli/Dropbox/Research/pythia_python/out/pp2760GeV_run0.pickle', 'rb')
evtList = pickle.load(file)
file.close()


print("\n\nThere are %s events!" % len(evtList))
###########################################################################
#   EVENT LOOP
###########################################################################
for event in evtList:

    n_ch_ev = 0 #counts number of charged particles for this event
    pt_tot_ev = 0.0 #sums the total transverse momentum for this event

    #----------------------------------------------------------------------
    #   PARTICLE LOOP
    #----------------------------------------------------------------------
    for prt in event.Particles:


        #
        #   ACCEPTANCE CONDITIONS
        # prt.pid_pdg > 99 \ removes leptons and gauge bosons (besides photons gauge bosons shouldn't be there anyway because they are not final particles)
        if prt.charge != 0 \
            and prt.pt > ptmin and prt.pt <= ptmax \
            and prt.y >= ymin and prt.y <= ymax \
            and prt.eta >= etamin and prt.eta <= etamax:

            #print(prt.status,"\t",prt.pid_PDG,"\t", prt.charge,"\t", prt.pt,"\t",prt.y,"\t",prt.eta)
            n_ch_ev += 1
            pt_tot_ev += prt.pt

        #
        #   END ACCEPTANCE CONDITIONS
        #

    #----------------------------------------------------------------------
    #   END PARTICLE LOOP
    #----------------------------------------------------------------------


    #
    #if particles are accepted then count this event
    #
    if n_ch_ev > 0:

        if neve == 0:
            sqrts = event.sqrts
            NA = event.NA
            NB = event.NB

        #print("Event\t", event.EventNum, "\t", n_ch_ev, "\n")

        neve += 1
        mult += n_ch_ev
        pt_tot += pt_tot_ev

###########################################################################
#   END EVENT LOOP
###########################################################################

#
#   calculate some stuff
#   normally I don't calculate things in the event generator code
#
avg_N = mult/neve
avg_pt_tot = pt_tot/neve
avg_pt = avg_pt_tot/avg_N

print('\n\n')
print(sqrts, "\t [GeV] center of mass collision energy")
print(NA, "\t projectile atomic number")
print(NB, "\t target atomic number")
print(ptmin, "\t [GeV] pt min")
print(ptmax, "\t [GeV] pt max")
print(ymin, "\t rapidity min")
print(ymax, "\t rapidity max")
print(etamin, "\t pseudorapidity min")
print(etamax, "\t pseudorapidity max")
#print(nEvent, "\t events generated")
print(neve, "\t events accepted")
print(avg_N, "\t average multiplicity per event")
print(avg_pt_tot, "\t [GeV] average total transverse moemtum per event")
print(avg_pt, "\t [GeV] average transverse momentum per particle")

print("\n\nRun time: %s seconds" % (time.time()-start_time))
