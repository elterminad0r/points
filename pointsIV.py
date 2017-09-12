#!/usr/bin/env python3

"""
Program to find the lowest-degree polynomial in terms of x that will fit a set
of coordinates. Duplicated coordinates are averaged. Coordinates should be
given as x-y pairs to -c, as space separated x-y pairs in a file or stdin. If
stdin is not a tty, it will automatically be read from. There is also an option
to convert a sequence of numbers (y-values y1-yn for x 1-n) to coordinates.
"""

import argparse
import sys

from functools import partial
from fractions import Fraction
from operator import mul, sub
from pprint import pprint

def print_system(system, verbose, string_method):
    if verbose:
        for lhs, rhs in system:
            print("{} = {}".format(" + ".join(map(string_method, lhs))), rhs)
        print()

def get_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-c", "--coord", nargs=2, action="append", type=Fraction,
                        help="x-y coordinate pair")
    parser.add_argument("-f", "--fractions", action="store_true",
                        help="use the repr of Fraction")
    parser.add_argument("-v", "--verbose", action="store_const", const=repr, default=str,
                        help="verbosely print stages of working")
    parser.add_argument("-z", "--zeroes", action="store_const", const=None, default=lambda: True,
                        help="print terms with 0-valued coefficients")
    parser.add_argument("-i", "--in-file", type=argparse.FileType("r"), action="append",
                        help="supply a file to read more coordinate pairs from (can be used more than once)")
    parser.add_argument("-n", "--nth-term", nargs="+", type=int,
                        help="a sequence of numbers to find the nth term of - shortcut for -c 1 n1 -c 2 n2.. Note that it's always posible to specify a 0-value with -c")
    return parser.parse_args()

def mult_list(l, n):
    return map(functools.partial(mul, n), l)

def sub_list(la, lb):
    return map(sub, la, lb)

def reduce_eq(system):
    ((l_elim, *l_target), r_target), *system = system

    for (elim_var, *eq), rhs in system:
        y_lhs = sub_list(mult_list(eq, l_elim), l_target)
        y_rhs = rhs * l_elim
        yield y_lhs, y_rhs

def solve(coords):
    pass

def read_coords(coords, stdin, opt_files, nth_term):
    out = []
    out.extend(map(tuple, coords))

    if not stdin.isatty():
        opt_files.append(stdin)

    for f in opt_files:
        with f as coord_file:
            for x, y in filter(None, map(str.split, coord_file)):
                out.append(tuple(map(Fraction, (x, y))))

    out.extend(enumerate(nth_term, 1))
    return out

def print_coords(coords):
    for xy in coords:
        print("({}, {})".format(*xy))
    print()

def main():
    args = get_args()
    coords = read_coords(args.coord or [], sys.stdin, args.in_file or [], args.nth_term or [])
    print_coords(coords)

if __name__ == "__main__":
    main()
