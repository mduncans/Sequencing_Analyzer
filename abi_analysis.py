from Bio.Seq import translate as t
from Bio.Seq import Seq
from tqdm import tqdm
from Bio import SeqIO
import pandas as pd
import glob
import os
import re


def get_seq_files(directory, key = None):
    if not directory.endswith('/'):
        directory += '/'

    if key is None:
        return glob.glob(f"{directory}*.ab1")
    else:
        return glob.glob(f'{directory}*{key}_*.ab1')


def create_dna_seqs_dict(files, reverse = True):
    '''
    generates dictionary of dna sequences from abi files input to function
    '''
    seqs = {}
    print('Reading ab1 files\n')
    for f in tqdm(files):
        s = SeqIO.read(f, 'abi')
        if reverse:
            seqs[s.name] = str(s.seq.reverse_complement())
        else:
            seqs[s.name] = str(s.seq)
    return seqs

def trim_dna_seqs(seqs, starting_seq = 'GGGCAGCCCCGAGAA', length = 321):
    '''
    Finds a matching starting_seq in the sequence and trims everything to 
    give a sequence from the starting_seq to input length
    '''
    trimmed_dna_seqs = {}
    print('Trimming DNA Sequences\n')
    for name, dna_seq in tqdm(seqs.items()):
        if len(re.findall(starting_seq, dna_seq)) == 1:
            index = dna_seq.index(starting_seq)
            try:
                trimmed_dna_seqs[name] = dna_seq[index:index + length]
            except:
                pass
    return trimmed_dna_seqs

def create_protein_seqs(trimmed_seqs):
    '''
    translates dna seqs to protein seqs and returns pandas dataframe
    '''
    print('Translating DNA Sequences\n')
    pro_seqs = {name: {i: aa for i, aa in enumerate(t(seq))} for name, seq in tqdm(trimmed_seqs.items())}
    return pd.DataFrame.from_dict(pro_seqs, orient = 'index')

if __name__ == '__main__':
    files = get_seq_files('220126_Fc1_SequencingResults/')
    ds = create_dna_seqs_dict(files,)
    tds = trim_dna_seqs(ds)
    ps = create_protein_seqs(tds)
    
    ps.to_excel('20220126 Fc1 Sequencing Results.xlsx')

else:
    doc_string = '\
    abi_analysis is used to create alignments from several .ab1 files. \n\
    The general work flow is:\n\
    \n\
    list_of_abi_files = get_seq_files(directory, key = None)\n\
    seqs_dict = create_dna_seqs_dict(list_of_abi_files, reverse = True)\n\
    trimmed_dna_seqs = trim_dna_seqs(seqs_dict, starting_seq = string_of_dna, length = int_length)\n\
    pro_seqs_df = create_protein_seqs(trimmed_dna_seqs)'
    print(doc_string)