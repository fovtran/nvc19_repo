from Bio.PDB import PDBParser, Selection
from Bio.PDB.PDBIO import PDBIO
import nglview as nv

parser = PDBParser()
structure = parser.get_structure("6LU7", "PDB/m_protein.pdb")

print(structure)
view = nv.show_biopython(structure)
view

for atom in structure.get_atoms():
    print ( atom )

for model in structure:
    for chain in model:
        for residue in chain:
            for atom in residue:
                print ( atom )

res_list = Selection.unfold_entities(structure, 'R')
# Get all atoms from a chain
atom_list = Selection.unfold_entities(chain, 'A')
print(res_list)
print(atom_list)
io=PDBIO()
io.set_structure(structure)
io.save("bio-pdb-pdbio-out.pdb")
import os
os.remove("bio-pdb-pdbio-out.pdb")  # tidy up
