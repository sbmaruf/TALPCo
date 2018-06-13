import os
import numpy as np
import argparse
import shutil

parser = argparse.ArgumentParser(description='Ted parallel data extraction.')
# for each address please add a trailing `/`
parser.add_argument("--debug",          type=int, default=1,
                    help="Additional print operation for debug.")
parser.add_argument("--lang1",          type=str, default="data_eng.txt",
                    help="Each of the srt file's name starts with this Language name.")
parser.add_argument("--lang2",          type=str, default="data_zsm.txt",
                    help="Each of the srt file's name starts with this Language name.")
parser.add_argument("--dir",            type=str, default="./data/",
                    help="Directory of the dataset")
parser.add_argument("--out_dir",        type=str, default="./nmt_io/",
                    help="NMT parallel sentences files")
parser.add_argument("--out_file",       type=str, default="alt.en-ms.",
                    help="Name of the output file")
parser.add_argument("--parallel_file",  type=int, default=1,
                    help="if the parallel lines will be saved in same file or not")
params = parser.parse_args()


def list2sent(lst):
    f = 0
    s = ''
    for i in lst:
        s += (' ' if f != 0 else '') + i
        f = 1
    return s


###############################
# Entry point of the script
###############################
file1_address = params.dir + params.lang1
file2_address = params.dir + params.lang2

assert os.path.exists(file1_address)
assert os.path.exists(file2_address)

os.makedirs(params.out_dir, exist_ok=True)

with open(file1_address) as file_ptr1:
    lang1_dict = {}
    lang2_dict = {}
    for line in file_ptr1:
        words = line.split()
        sent = list2sent(words[1:])
        lang1_dict[words[0]] = sent

with open(file2_address) as file_ptr2:
    for line in file_ptr2:
        words = line.split()
        sent = list2sent(words[1:])
        lang2_dict[words[0]] = sent

assert len(lang1_dict) == len(lang2_dict)

if not params.parallel_file:
    out_address = params.out_dir + params.out_file + 'joint'
    with open(out_address, "w") as file_ptr:
        for k, v in lang1_dict.items():
            file_ptr.write("#-----<s>-----#\n")
            file_ptr.write(v+"\n")
            file_ptr.write("#-----<s>-----#\n")
            file_ptr.write(lang2_dict[k]+"\n")
else:
    out_address1 = params.out_dir + params.out_file + 'en'
    out_address2 = params.out_dir + params.out_file + 'ms'
    with open(out_address1, "w") as file_ptr1,\
            open(out_address2, "w") as file_ptr2:
        for k, v in lang1_dict.items():
            file_ptr1.write(v+"\n")
            file_ptr2.write(lang2_dict[k]+"\n")
