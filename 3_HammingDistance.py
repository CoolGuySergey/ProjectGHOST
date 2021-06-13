# WORK IN PROGRESS
# Calculate hamming distance using SubsMat module

from Bio import AlignIO
from Bio import Alphabet
from Bio.Alphabet import IUPAC
from Bio.Align import AlignInfo
from Bio import SubsMat

alpha = Alphabet.Gapped(IUPAC.protein)

filename = "seq_file2.aln"
c_align = AlignIO.read(filename, "clustal", alphabet=alpha)
summary_align = AlignInfo.SummaryInfo(c_align)
replace_info = summary_align.replacement_dictionary(["A", "V", "L",
                                                     "F", "S", "Q"])

my_arm = SubsMat.SeqMat(replace_info)
my_lom = SubsMat.make_log_odds_matrix(my_arm)
my_lom.print_mat()


# Calculate hamming distance

def hamming_distance(s1, s2):
    distance = 0
for i in range(len(s1)):
if s1[i]!=s2[i]: #compare i-th letter of s1 and s2
distance += 1
return distance


d = hamming_distance("agtctgtca", "gatctctgc")
print d
print hamming_distance("attgctg", "atgcctg")
