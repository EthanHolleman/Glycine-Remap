import argparse
import shutil
import sys
import multiprocessing as mp

DEPENDS = './depends.txt'

def check_depends():
    dps = []
    with open(DEPENDS) as dp:
        dps = dp.readlines()
    for dp in dps:
        if shutil.which(dp) is not None:
            print('Please install {} and rerun TARP'.format(dp))
            sys.exit

    print('All dependency checks passed\n')


def set_args():
    parser = argparse.ArgumentParser(description='Gylcine_Remap Args')

    parser.add_argument('-I', type=str, help='Path to outdated intact type elements')
    parser.add_argument('-S', type=str, help='Path to outdated solo type elements')
    parser.add_argument('-P', type=str, help='Path to BLAST DB created from assembly old elements are mapped to')
    parser.add_argument('-C', type=str, help='Path to BLAST DB created from most recent assembly')
    parser.add_argument('-O', type=str, help='Path where results will be written')
    parser.add_argument('-T', type=int, default=mp.cpu_count(), help='Number of cores to run processes on, default is all')
    parser.add_argument('-B', type=str, help='Bowtie index created from most recent assembly')
    parser.add_argument('-acc_o', type=str, help='Path to accession file for outdated assembly')
    parser.add_argument('-acc_c', type=str, help='Path to accession file for current assembly')
    parser.add_argument('-name', type=str, help='Name of the run, all data will be written in dir under this name')
    parser.add_argument('-M', action='store_true', help='Run backmapping, default = true, set to false to prevent backmapping')
    args = parser.parse_args()
    exit = False
    if not args.I:
        print('Path to intact elements fasta file required (-I)')
        exit = True
    if not args.P or not args.C:
        print('Please supply path to BLAST database for both current and outdated assemblies')
        exit = True
    if not args.O:
        print('Please supply output directory')
        exit = True
    if not args.B:
        print('Please supply bowtie2 index of current assembly')
        exit = True
    if not args.acc_c or not args.acc_c:
        print('''Please provide paths to the acc2chr files for the current and
        outdated assemblies. These can be found in the Genbank FTP folders for
        a given assembly.''')
    if exit:
        print('Goodbye')
        sys.exit()
    else:
        return args


# confiles can be made with one consensus to rule them all from fasta tools
# args that need to add
# run name, potentially need old bowtie index to do the cross validation
# of consensus sequences
# need to fix some of this crazy output from fasta tools
