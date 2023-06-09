#!/usr/bin/env nextflow


//
// A worflow file that calls this subworkflow can be written starting from the  config    tabular_match_handler.config   
// it should take care of providing the correct tuple of file pairs as input
//


// Modules dependencie section

include { table_matcher } from "../modules/tabular_matcher"


workflow table_matcher_handler {

	take:
	in_pair
	outname

	main:

	// handling the possibility to have as many outputs as pairs with dynamic nanming
	// as a trick the process will always run in suffix mode just to be renamed after in case
	
	in_pair.map{ it -> [ it[0], it[1], "${it[0].baseName}-${it[1].baseName}.${params.suffix_TAB}" ]}.set{ corrected_pair }
	table_matcher(corrected_pair)
	stdout = table_matcher.out.standardout


	// only real difference is in how the output is handeled

	output_table = null
	if (outname) {
		output_table = table_matcher.out.matched_table.collectFile( name: outname )
	} else {
                output_table = table_matcher.out.matched_table
	}


	emit:
	stdout
	output_table
}
