#!/usr/bin/env nextflow

process table_matcher {
	label 'tabular'
	tag { "${outname}" } 

	input:
	tuple path(infile1), path(infile2), val(outname)

	output:
        path outname, emit: matched_table
        stdout emit: standardout                //for debug

	script:
	"""
	match_table_louncher.py -f1 ${infile1} -f2 ${infile2} -o ${outname} -p1 ${params.pos1_TAB} -p2 ${params.pos2_TAB} -d1 ${params.del1_TAB} -d2 ${params.del2_TAB} --check_types ${params.check_TAB}
	"""
}
