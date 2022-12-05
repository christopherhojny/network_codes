#!/usr/bin/python3

import graph as graph
import networkcode as nwc
import instances as inst
import sys

# check input
if len(sys.argv) < 3:
    print("ERROR: received too few arguments")
    print("usage: ./test.py <alphabet> <codesize> <optional parameters>")
    print("call script with optional parameter -h for more information")
    sys.exit()

optional = sys.argv[3:]
if "-h" in optional:
    print("optional parameters:")
    print("\t-h: show help")
    print("\t-v: visualize network?")
    print("\t-i<name>: instance name")
    print("\t-s<0/1>: (don't) use symmetry handling")
    print("\t-p<0/1>: (don't) apply presolving")
    print("\t-c<0/1>: (don't) add cutting planes")
    print("\texamplary call: ./test.py 4 2 -ibutterfly -s1 -c0")
    sys.exit()

size_alpha = int(sys.argv[1])
size_code = int(sys.argv[2])

# parse optional parameters
default_ins = "butterfly"
default_sym = True
default_pre = True
default_cut = True
default_vis = False
for arg in optional:
    if arg.startswith("-i"):
        default_ins = arg[2:]
    elif arg.startswith("-s"):
        default_sym = bool(int(arg[2:]))
    elif arg.startswith("-p"):
        default_pre = bool(int(arg[2:]))
    elif arg.startswith("-c"):
        default_cut = bool(int(arg[2:]))
    elif arg.startswith("-v"):
        default_vis = True

G = inst.get_instance(default_ins)
if default_vis:
    G.visualize()

nwc.find_unambiguous_code2(G, size_alpha, size_code,
                           handle_symmetries=default_sym, add_cuts=default_cut,
                           apply_preprocessing=default_pre)
