import pypdb

Region = "ADA"
chem_desc = pypdb.describe_chemical(Region)
print(chem_desc)

q = pypdb.make_query(Region)
d = pypdb.do_search(q)
for a in d:
	print(a)

print( pypdb.describe_pdb(d[0]) )
blast_results = pypdb.get_blast(d[0])
gene_info = pypdb.get_gene_onto(d[0])
ligands_dict = pypdb.get_ligands(d[0])
print(blast_results)
print(gene_info)
pdb_file = pypdb.get_pdb_file(d[0], filetype='pdb', compression=True)
f = open(d[0]+".pdb", 'wb')
f.write(pdb_file)
f.close()
