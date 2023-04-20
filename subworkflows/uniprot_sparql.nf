#!/usr/bin/env nextflow



// Modules dependencie section

include { uniprot_to_pdb } from "../modules/from_uniprot_to_pdb"


workflow sprql_querier {

	take:
	pattern_to_idfile

	main:
	py_script_from = Channel.fromPath("${launchDir}/bin/from_uniprot_to_pdb.py")
	uniprot_to_pdb(pattern_to_idfile, py_script_from.collect())
	
	emit:
	found_pdb = uniprot_to_pdb.out.retrieved_pdb
	stout = uniprot_to_pdb.out.standardout		// for debug
}
