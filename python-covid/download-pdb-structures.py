# -*- coding: utf-8 -*-
import Bio
from Bio.PDB import PDBList

'''Selecting structures from PDB'''
pdbl = PDBList()
PDBlist2=['4B97','4IPH','4HNO','4HG7','4IRG','4G4W','4JKW','4IPC','2YPM','4KEI']
for i in PDBlist2:
    pdbl.retrieve_pdb_file(i,pdir='PDB')
