# This script is for:
# Starting with an annotated .gb file containing multiple entries
# For each entry, pull out all PCGs, concatenate, and align (amino acids)

# Next steps:
# AA to DNA, align both, Bowker's test

# Note:
# SeqIO.parse()  is an iterator, for single records use Bio.SeqIO.read()
# Play around in shell REPL with entry = next(SeqIO.parse('PlayData.gb', "genbank"))

################################# 
####### Manipulating GB files ###
#################################

from Bio import SeqIO
from Bio import Seq

def fetch_transcripts(entry):
    """
fetch_transcripts takes in a singular gb entry and builds a dict of all transcripts:
'NADH Dehydrogenase subunit 2' : ['MLKFY ...']
'cytochrome c oxidase subunit I' : ['MLPHA ...']
    """
    transcripts = {}
    for feature in entry.features: # entry.features returns a list of all 51 feature
        if feature.type == 'CDS':
            transcripts[feature.qualifiers["product"][0]] = [feature.qualifiers["translation"][0]]
    return transcripts

taxid_jointtranscipt = {}
# This empty dict will be built upon by
# Extracting taxid from all entries as KEY
# running fetch_transcripts for each entry, contatenate all AAs as value, ie:
# 'taxon:1270212' : ['MLKFY ...']
# 'taxon:1270125' : ['MLPHA ...']

for entry in SeqIO.parse('PlayData.gb', "genbank"):
    # first we extract taxid as key
    # entry.features[0] is (usually) the source sequence. Assert check though.
    assert entry.features[0].type == 'source'
    taxid = entry.features[0].qualifiers['db_xref'] # would give taxid ['taxon:1270216']

    # then we concatenate all transcipts as key
    transcripts_dict = fetch_transcripts(entry)
    jointtranscipt = ""
    for transcript in transcripts_dict:
        jointtranscipt = jointtranscipt + str(transcripts_dict[transcript])
    taxid_jointtranscipt[str(taxid)] = jointtranscipt
    
