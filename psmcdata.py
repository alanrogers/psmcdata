#!/usr/bin/env python3

"""
psmcdata: parse psmc output and write data in two columns: (1) time
before present, and (2) estimated population size.

usage: python3 psmcdata [-u <mutrate> -g <gentime>] <inputfile.psmc>

where "mutrate" is the mutation rate per base pair per generation, and
"gentime" is the generation time in years. By default, mutrate=1 and
gentime=1.
"""

import sys

mutrate = 1.0 # mutation rate
gentime = 1.0 # generation time
fname = None

def usage():
    print("Usage: psmcdata [-u <mutrate> -g <gentime>] <inputfile>",
          file=sys.stderr)
    print("Defaults: mutrate=%f gentime=%d" % (mutrate, gentime),
          file=sys.stderr)
    exit(1)

i = 1
while i < len(sys.argv):
    if sys.argv[i] == "-u":
        i += 1
        if i == len(sys.argv):
            usage()
        mutrate = float(sys.argv[i])
    elif sys.argv[i] == "-g":
        i += 1
        if i == len(sys.argv):
            usage()
        gentime = float(sys.argv[i])
    else:
        if fname != None:
            usage()
        fname = sys.argv[i]
    i += 1

if fname == None:
    usage()

try:    
    ifile = open(fname, "r")
except FileNotFoundError:
    print("Can't read file %s" % fname, file=sys.stderr)
    exit(1)

print("# mutrate = %e gentime=%f inputfile=%s" % (mutrate, gentime, fname))

# Find position of last set of output within ifile by searching for
# the last line that begins with "RD". There is one set of output for
# each of several sets of iterations, and each of these sets prints a
# single RD line.
position = -1
while True:
    line = ifile.readline()
    if line == "":
        break

    if len(line) >= 2 and line[0:2] == "RD":
        position = ifile.tell()

if position == -1:
    print("Can't find data within .psmc file", file=sys.stderr)
    exit(1)

# Return to start of last section of output
ifile.seek(position)

# read theta0
theta0 = None
while True:
    line = ifile.readline()
    if line == "":
        break
    line = line.strip()
    line = line.split("\t")

    # The TR line prints both theta0 and rho0. Documentation doesn't
    # say which value is which, but the code seems to indicate that
    # theta0 is first.
    if line[0] == "TR":
        theta0 = float(line[1])
        break

if theta0 == None:
    print("Can't find TR line, which specifies theta0", file=sys.stderr)
    exit()

# Ordinarily, theta = 4Nu. But for psmc this is multiplied by 100, the
# number of nucleotide sites lumped into each bin when generating
# the .psmcfa file used as input by psmc. This rescaling is explained
# in the psmc README file.
N0 = theta0/(4*mutrate*100)

print("# theta0=%f N0=%f" % (theta0, N0))

print("%s\t%s" % ("t", "Ne"))

# read data, rescale, and print
while True:
    line = ifile.readline()
    if line == "":
        break
    line = line.strip()
    line = line.split("\t")

    # Data are in the lines that begin with "RS"
    if line[0] != "RS":
        continue

    # Next bit is based on the "rescaling" section of the psmc README
    # file. The documentation doesn't say what values are in the
    # various fields of each "RS" line. The code in file aux.c
    # indicates that t[k] is in field 2 and lambda[k] (=N[k]/N0) is in
    # field 3, where the first field (containing "RS") is field 0.
    t = float(line[2]) * 2 * N0 * gentime
    Nt = float(line[3]) * N0
    
    print("%f\t%f" % (t, Nt))
