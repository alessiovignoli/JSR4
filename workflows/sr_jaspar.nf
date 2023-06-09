#!/usr/bin/env nextflow


// Modules dependencie section

include { sr_prediction } from "../modules/sr_jasper_pred"
include { sprql_querier } from "../subworkflows/uniprot_sparql" addParams(column_UN: 9)
include { table_matcher_handler } from "../subworkflows/tabular_match_handler" addParams(pos1_TAB: 8)


workflow  sr_input_handler {

	take:
	fasta_file
	outname_path
		

	main:

	// error section of missing or wrong inputs
	
	if (fasta_file == null) {
		log.info '--query_sr   flag has not been given, it is mandatory to have a valid path'
		log.info 'for more details type --help or take a look at conf/sr_jaspar.config'
		exit 1
	} else if(outname_path == null) {
		log.info '--out_name_sr    flag  has not been given, it is mandatory to have a valid string <file_name>'
		log.info 'for more details type --help or take a look at conf/sr_jaspar.config'
		exit 1
	} 
	

	infa = Channel.fromPath(fasta_file)
	sr_prediction(infa)
	sprql_querier(sr_prediction.out.sr_jaspar_out)
	

	// Reconcile the two information in the files above in one through the uniprot ID
	// first related files from the two above process are put in a tuple as pairs

	sr_prediction.out.sr_jaspar_out.map{ it -> ["${it.name}".split(".out")[0], it] }.set{ mapped_sr_results }
	sprql_querier.out.found_pdb.map{ it -> ["${it.name}".split("_pdb.ids")[0], it] }.set{ mapped_sprql_results }
	mapped_sr_results.combine( mapped_sprql_results, by: 0 ).map{ it -> [ it[1], it[2] ]  }.set{ paired_tabulars }

	// then on the pairs the matcher is called, asking to have just one unique output for all inputs

	table_matcher_handler(paired_tabulars, outname_path)
	table_matcher_handler.out.output_table.collectFile(storeDir: params.OUTPUT_DIR).set{ final_out }

	emit:
	final_out 
	stdout = table_matcher_handler.out.stdout
}


