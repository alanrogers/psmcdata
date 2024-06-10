# psmcdata
Read PSMC output and write a text file with 2 columns: time and
estimated effective population size.

    usage: python3 psmcdata.py [-u <mutrate> -g <gentime>] <inputfile.psmc>

where "mutrate" is the mutation rate per base pair per generation, and
"gentime" is the generation time in years. By default, mutrate=1 and
gentime=1.

To install programs as an executable file, "psmcdata", in directory
$HOME/bin, type

    make install



