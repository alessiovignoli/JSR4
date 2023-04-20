#!/usr/bin/env nextflow



process uniprot_to_pdb {
	tag { "${ID_file}" }
	label 'sparql_query'	

	input:
	path ID_file
	path py_script

	output:
	path outname, emit: retrieved_pdb
	stdout emit: standardout		//for debug

	script:
	outname = ID_file.getBaseName() + '_pdb.ids'
	"""
	python3 ${py_script} -i ${ID_file} -o ${outname} --col ${params.column_UN} --spatiator ${params.separator_col_UN} --skip_line ${params.skip_1row_UN}
	"""
}


