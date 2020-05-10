# -*- coding: utf-8 -*-
import Bio
from Bio.PDB import PDBList

'''Selecting structures from PDB'''
pdbl = PDBList()
PDBtestlist=['4B97','4IPH','4HNO','4HG7','4IRG','4G4W','4JKW','4IPC','2YPM','4KEI']
PDBlist2_ncov19=['6LU7', '6VSB', '6LXT', '6LVN', '6VW1', '6VWW', '6Y2E', '6Y2F', '6Y2G']

for i in PDBlist2_ncov19:
    pdbl.retrieve_pdb_file(i,pdir='PDB')
