#!/usr/bin/env python
import sys
from gemmi import cif,read_structure

greeted = set()
for path in sys.argv[1:]:
    try:
        st = read_structure(path)  # copy all the data from mmCIF file
        block = st.make_mmcif_headers()
        st.setup_entities()
        print ( block.get_mmcif_category_names() )
        for key, value in st.info.items(): print(key, value)
        for a in st:
            print( a )
        for e in st.entities:
            print( e )
            print( e.name )
            print( e.subchains )
            print( e.entity_type )
            print( e.polymer_type )
            print( e.full_sequence )

        st.make_mmcif_document().write_file('PDB/new.cif')
    except Exception as e:
        print("Oops. %s" % e)
        sys.exit(1)
