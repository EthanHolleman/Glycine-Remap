import os
import itertools
from operator import or_
from functools import reduce


from Transposer.search import sort_elements

# move this to the run object class since each sam is saved in the jobs attribute

def sort_sams(search_list):
    '''
    Takes in run object and returns sorted list of the solo and intact element
    for that object. Sort by chromosomes and sort by position in the
    chromosomes.
    Each sam can sort itself but want to make sure you do all processing first
    before anyting else happens
    This would be called in the run and given a list of all the search jobs after
    they have been run. Then this function can remove duplicates in each sam
    and the duplicates between sams the sort and return a sorted list of
    elements which then can be written to a fasta file.
    '''
    els_list = [s.element_set for s in search_list]
    # get all element sets from search objects
    all_els = list(itertools.chain.from_iterable(els_list))
    # chain all lists together
    sort_els = sort_elements(all_els)
    # sort the elements as if one large list

    return sort_els


def write_fasta(sorted_elements, output, name):
    # sorted elements are coming in list format
    # need to write in way that works with the information in each element
    # need to figure out what name maybe just use the run name for that
    # and add to the element
    # labels elements by their position on the chromosome format is
    # name chr-position
    fasta_name = os.path.join(output, '{}_remap.fa'.format(str(name)))

    try:
        with open(fasta_name, 'w') as output:
            i = 1
            cur_chr = None
            for el in sorted_elements:
                if cur_chr != el.chr:
                    cur_chr = el.chr
                    i = 1
                header = '>{} {}-{}, {}, {}'.format(el.name, cur_chr, str(i),
                                                   el.startLocation, el.length)
                seq = el.seq
                output.write(header + '\n' + seq[:-1] + '\n')
                i += 1
        print('written to', fasta_name)
    except FileNotFoundError as e:
        return e
