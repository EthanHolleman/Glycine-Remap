#!/usr/bin/env python3
import os
import time

from args import set_args
from args import check_depends
from run import Run
from Transposer.process_sams import sort_elements
from Transposer.process_sams import sort_sams
from Transposer.process_sams import rename_elements
from Transposer.process_sams import pruner
from Transposer.process_sams import write_results
from backmap.backmap import *
from backmap.backmap_write import *

# TODO: Move print statements
def main():
    args = set_args()  # read args and assign to args
    intact_old = args.I
    solo_old = args.S
    BDB_old = args.P
    BDB_cur = args.C
    output = args.O
    BTI = args.B
    acc_old = args.acc_o
    acc_cur = args.acc_c
    run_name = args.name
    backmap = args.M
    min = args.E
    # assign passed arguements not really needed but done
    # to add some clarity later on
    # create the run object
    new_run = Run(cur_BDB=BDB_cur, old_BDB=BDB_old, BTI=BTI,
                  cur_acc=acc_cur, old_acc=acc_old, run_name=run_name,
                  output=output, cie=intact_old, csi=solo_old, min_els=min)
    # do everything up to including bowtieing all the consensus sequences
    new_run.select_clusters()
    new_run.make_clstr_fastas()  # convert clstr files to full fasta files
    #new_run.make_consensensi()  # make cluster consensus sequences
    new_run.make_consensensi_teo()
    #new_run.prune_clstr_cons()
    new_run.make_jobs_two()
    #new_run.make_jobs()  # make bowtie jobs
    new_run.run_jobs()  # run bowtie jobs add threads arguement
    sels = rename_elements(pruner(sort_sams(new_run.jobs), f=100))
    out_base = os.path.join(new_run.write_dirs[2], run_name)
    sels = list(sels)
    write_results(sels, out_base)

    # backmap elements
    if backmap is not False:
        old_els = make_soy_elements(backmap, acc_old)
        old_els = add_flanks(old_els, BDB_old)
        matches, unmatches, flank_dict = test_exact(make_flank_dict(old_els), sels)
        chr_index = chr_indexer(flank_dict)
        matches, unmatches, chr_index = rum_ham(chr_index, unmatches, matches)
        print(len(matches), 'len matchs')
        print(len(unmatches), 'len unmatch')
        # matches are appended and returned
        match_path = os.path.join(new_run.write_dirs[2], run_name + '_matches.csv')
        unmatch_path = os.path.join(new_run.write_dirs[2], run_name + '_unmatched.csv')
        match_writer(match_formater(matches), match_path)
        nomatch_writer(unmatches, unmatch_path)

if __name__ == '__main__':
    main()
