/* Copyright 2004
   Stanford University

   This file is part of the DSR PDB Library.

   The DSR PDB Library is free software; you can redistribute it and/or modify
   it under the terms of the GNU Lesser General Public License as published by
   the Free Software Foundation; either version 2.1 of the License, or (at your
   option) any later version.

   The DSR PDB Library is distributed in the hope that it will be useful, but
   WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
   or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
   License for more details.

   You should have received a copy of the GNU Lesser General Public License
   along with the DSR PDB Library; see the file COPYING.LIB.  If not, write to
   the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
   MA 02111-1307, USA. */

#include <dsrpdb/PDB.h>

#include <vector>
#include <iterator>
#include <fstream>
#include <dsrpdb/align.h>
#include <dsrpdb/distance.h>


#ifdef PDB_USE_BOOST_PROGRAM_OPTIONS
#include <boost/program_options.hpp>
#endif


int main(int argc, char *argv[]){
  std::string base_file, input_file, output_file;
  bool print_help=false;
  bool crms=false, drms=false;
  int base_model=0;
  bool warn=false;
#ifdef PDB_USE_BOOST_PROGRAM_OPTIONS
  {
    boost::program_options::options_description o("Allowed options"), po, ao;
    o.add_options()
      ("aligned-pdb,a", boost::program_options::value< std::string>(&output_file), "Where to write the result of aligning input-pdb to base-pdb.")
    
      ("crms,c", boost::program_options::bool_switch(&crms), "Output the cRMS between the two pdbs (after alignment).")
      ("drms,d", boost::program_options::bool_switch(&drms), "Output the dRMS between the two pdbs.")     
      ("verbose,v", boost::program_options::bool_switch(&warn), "Warn about errors parsing pdb file.")
      ("help", boost::program_options::bool_switch(&print_help), "Produce help message");
    po.add_options()("base-pdb", boost::program_options::value< std::string>(&base_file), "Base file")
      ("input-pdb", boost::program_options::value< std::string>(&input_file), "input file");
    ao.add(o).add(po);
    
    boost::program_options::positional_options_description p;
    p.add("base-pdb", 1);
    p.add("input-pdb", 1);

    boost::program_options::variables_map vm;
    boost::program_options::store(boost::program_options::command_line_parser(argc, argv).
				  options(ao).positional(p).run(), vm);
    boost::program_options::notify(vm);


    if (base_file.empty() || input_file.empty() || print_help) {
      std::cout << "This program aligns two proteins and can compute distances between them.\n";
      std::cout << "usage: " << argv[0] << " base-pdb input-pdb\n\n";
      std::cout << o << "\n";
      return EXIT_FAILURE;
    }
  }

#else
  if (argc != 3){
    std::cerr << "The program is built without boost/program_options.hpp.\n";
    std::cerr << "useage: " << argv[0] << " file0.pdb file1.pdb" << std::endl;
    return EXIT_FAILURE;
  }
  input_file = argv[1];
  output_file = argv[2];
#endif
  
  std::ifstream in(input_file.c_str());

  if (!in){
    std::cerr<< "Error opening input file: " << input_file << std::endl;
    return EXIT_FAILURE;
  }
  std::ifstream bin(base_file.c_str());

  if (!bin){
    std::cerr<< "Error opening input file: " << base_file << std::endl;
    return EXIT_FAILURE;
  }

  dsrpdb::PDB input(in, warn);
  dsrpdb::PDB base(bin, warn);
  dsrpdb::Protein base_protein;
  for (unsigned int i=0; i< base.number_of_models(); ++i){
    const dsrpdb::Model &m= base.model(i);
    if (base_model ==0 || m.index()==base_model) {
      for (unsigned int j=0; j< m.number_of_chains(); ++j){
	base_protein= m.chain(j);

      }
    }
  }
  
  if ( !output_file.empty() || crms) {
    for (unsigned int i=0; i< input.number_of_models(); ++i){
      dsrpdb::Model &m= input.model(i);
      dsrpdb::Protein &p= m.chain(0);
      dsrpdb::align_second_protein_to_first(base_protein, p);
    }
  }

  if (!output_file.empty()) {
    std::ofstream out(output_file.c_str());
    if (!out){
      std::cerr << "Error opening output file " 
		<< output_file << std::endl;
      return EXIT_FAILURE;
    }
    input.write(out);
  }

  if (crms) {
    std::cout << "cRMS:\n";
    for (unsigned int i=0; i< input.number_of_models(); ++i){
      dsrpdb::Model &m= input.model(i);
      dsrpdb::Protein &p= m.chain(0);
      double d=dsrpdb::no_align_cRMS(base_protein, p);
      if (d < .00001) d=0;
      std::cout << "Model " << i << " is " << d << std::endl;
    }
  }

  if (drms) {
    std::cout << "dRMS:\n";
    for (unsigned int i=0; i< input.number_of_models(); ++i){
      dsrpdb::Model &m= input.model(i);
      dsrpdb::Protein &p= m.chain(0);
      double d=dsrpdb::dRMS(base_protein, p);
      if (d < .00001) d=0;
      std::cout << "Model " << i << " is " << d << std::endl;
    }
  }

  return EXIT_SUCCESS;

}

