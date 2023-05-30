#!/usr/bin/env nextflow


// Modules dependencie section

include { sprql_querier } from "../subworkflows/uniprot_sparql" addParams(column_UN: 9)
include { sr_prediction } from "../modules/sr_jasper_pred"


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
	//out_filename = (("${fasta_file}".split('/')[-1]).split('\\.')[0]).split('\\*')[0]  + '_sr_pdb.txt'
	sr_prediction(infa)
	sprql_querier(sr_prediction.out.sr_jaspar_out)
	

	// Reconcile the two information in the files above in one through the uniprot ID

	sr_prediction.out.sr_jaspar_out.splitText().map{ it -> [(("${it}".trim()).split("\t"))[-1], "${it}".trim()]}.set{ mapped_sr_results }
	sprql_querier.out.found_pdb.splitText().map{ it -> [(("${it}".trim()).split("\t"))[0], ((("${it}".trim()).split("\t"))[1..3]).join("\t") ]}.set{ mapped_pdb_results }
	mapped_sr_results.combine( mapped_pdb_results, by: 0 ).set{ matched_lines }
	
	// let's add the header line

	header = Channel.of("Query\tTF Name\tTF Matrix\tE-value\tQuery Start-End\tTF Start-End\tDBD\t%ID\tJoint-coverage\tref uniprotID\tpdbID\tchain\tStructure Start-End")
	matched_lines.map{ it -> [it[1], it[2]].join("\t") }.set{ tmp }
	header.concat(tmp).collectFile(name: outname_path, storeDir: params.OUTPUT_DIR, newLine: true, sort: false).set{ final_out }
	

	emit:
	final_out = final_out
	stdout = sprql_querier.out.stout
}


