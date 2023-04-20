#!/usr/bin/env nextflow


process sr_prediction {
	label 'sr_jaspar'
	tag { "${inname}" }

	input:
	path inname

	output:
	path output_name, emit: sr_jaspar_out
	stdout emit: standardout 	// for debug

	script:
	output_name = "${inname.baseName}" + "_sr.out"
	"""
	infer_profile.py --latest  ${inname} --output-file ${output_name} 
	"""

}

