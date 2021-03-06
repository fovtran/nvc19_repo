from __future__ import print_function
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqIO.FastaIO import SimpleFastaParser
from Bio.SeqIO.QualityIO import FastqGeneralIterator
from Bio.SeqUtils.ProtParam import ProteinAnalysis

records = SeqIO.parse('structures_4_3_2020/coronavirus.fasta','fasta')
for req in records:
	print(req.id, len(req))
	pass

Region = "ADA"
records = SeqIO.parse('structures_4_3_2020/coronavirus.fasta','fasta')
for record in records:
	if str(record.seq).find(Region) >= 0:
		print (str(record.id))

record_dict = SeqIO.index('structures_4_3_2020/coronavirus.fasta','fasta')
for req in record_dict:
		print(record_dict.get_raw(req).decode())
		#pass
record_dict.close()

analysed_seq = ProteinAnalysis(Region)
print( "Molecular weight: ", analysed_seq.molecular_weight() )
print( "Gravy: ", analysed_seq.gravy())
print( "Aminoacids: ", analysed_seq.count_amino_acids())
print(analysed_seq.count_amino_acids()['A'])
print(analysed_seq.count_amino_acids()['E'])
print(analysed_seq.count_amino_acids()['D'])

my_seq = Seq(Region)
print(my_seq)
print (my_seq.alphabet)
print(my_seq.complement())
print(my_seq.reverse_complement())


from Bio.SeqUtils import ProtParamData  # Local
from Bio.SeqUtils import IsoelectricPoint  # Local
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
from Bio.Data import IUPACData
from Bio.SeqUtils import molecular_weight

from biopandas.pdb import PandasPdb
ppdb = PandasPdb().fetch_pdb(d[0])
sequence = ppdb.amino3to1()
print( sequence.tail() )
for chain_id in sequence['chain_id'].unique():
    print('\nChain ID: %s' % chain_id)
    print(''.join(sequence.loc[sequence['chain_id'] == chain_id, 'residue_name']))

ppdb.df['ATOM'] = ppdb.df['ATOM'][ppdb.df['ATOM']['element_symbol'] != 'H']
print(ppdb.df)
