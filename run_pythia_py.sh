#!/bin/bash
#
#	run_pythia_py.sh
#
#      script to run run_pythia_py.py and tell it where to store events
#	
#
# 	choose a system
#	0 = pp200GeV
#	1 = pp2760GeV
#	2 = AuAu200GeV
#	3 = PbPb2760GeV
choice=1
#number of events
nEv=100
#number of computer cores to run RunPythia on
nCores=1
#
# initiate some varables that may get reset depending on $choice
#
#center of mass collision energy in [GeV]
sqrts=200
sys_name="pp"$sqrts"GeV"
#sys_name="PbPb"$sqrts"GeV"
#
#source code location
pgm_loc="/path_to_folder/pythia_python/"
src_loc=$pgm_loc"src/"
#
#location to place .root file with pythia events
res_loc=$pgm_loc"out/"
#
#
# colliding system codes
#********************************************************************
# make sure your choice is represented in RunPythia.cxx event loop
#********************************************************************
p=2212
neutron=2112
deuteron=1000010020
He=1000020040
Li=1000030060
C=1000060120
O=1000080160
Cu=1000290630
Kr=1000360840
Xe=1000541290
Au=1000791970
Pb=1000822080
#pass these to the main code, set them first
A=0.0 #projectile
B=0.0 #target
#********************************************************************
#
#kinimatic cut of hard scatterings at generation level in [GeV]
#for min bias use ptHatMin=0, ptHatMax=-1
#for min bias use HardQCD:all=off, nonDiffractive=on, doubleDiffractive=on, centralDiffractive=on
#for ptHatMin>0 use HardQCD:all=on, nonDiffractive=off, doubleDiffractive=off, centralDiffractive=off
ptHatMin=0
ptHatMax=-1
#
# pythia options, HardQCD and nonDiffractive should not be "on" at the same time
# HardQCD=on requires a ptHatMin>1GeV
on="on"
off="off"
mb="SoftQCD:nonDiffractive = "
el="SoftQCD:elastic = "
sd="SoftQCD:singleDiffractive = "
dd="SoftQCD:doubleDiffractive = "
cd="SoftQCD:centralDiffractive = "
hard="HardQCD:all = "
#
####################################################################
# all of the below choices assume minimum bias soft QCD settings
####################################################################
echo "choice $choice selected"
if [ $choice -eq 0 ] # pp 200 GeV
then
	sqrts=200
	sys_name="pp"$sqrts"GeV"
	A=$p
	B=$p
	res_loc=$pgm_loc"out/"
elif [ $choice -eq 1 ] # pp 2760 GeV
then
	sqrts=2760
	sys_name="pp"$sqrts"GeV"
	A=$p
	B=$p
	res_loc=$pgm_loc"out/"
elif [ $choice -eq 2 ] # AuAu 200 GeV
then
	sqrts=200
	sys_name="AuAu"$sqrts"GeV"
	A=$Au
	B=$Au
	res_loc=$pgm_loc"out/"
elif [ $choice -eq 3 ] # PbPb 2760 GeV
then
	sqrts=2760
	sys_name="PbPb"$sqrts"GeV"
	A=$Pb
	B=$Pb
	res_loc=$pgm_loc"out/"
fi
echo "Running PlotAnalysis for "$sys_name
####################################################################
#
#
#
# change directories to the project directory
cd $src_loc
#
# run several instances of RunPythia in parallel and uniquely name the outputs uing the n
for(( n=0; n<nCores; n++)) 
do
	#the name of the .root file that stores final events
	filename=$sys_name"_run"$n
#
	# this is the non-single-diffractive "minimum bias" run that is needed to get the corss section for scaling purposes
	python3 pyPYTHIA.py $nEv $sqrts $A $B $ptHatMin $ptHatMax $res_loc $filename "$mb$on" "$el$off" "$sd$off" "$dd$on" "$cd$on" "$hard$off" > $res_loc$filename'.log' &
	#need time to get a new random seed
	sleep 1

done
#
