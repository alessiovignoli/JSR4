#!/usr/bin/env nextflow




// this prints the help in case you use --help parameter in the command line and it stops the pipeline
if (params.help) {
    log.info "This simple pipeline launches first a  process consisting of similarity regression (SR) as implemented by jasper"
    log.info "on the basis of the SR paper itself. Github  ->  https://github.com/wassermanlab/JASPAR-inference-tool"
    log.info ""
    log.info "Second from the uniprot ID of the found hits (modified jaspar to outptut that info) it recovers the "
    log.info "pdb IDs chain and start-end info associated to such uniprot ID. Placing all toghether in a tab sepaarted file."
    log.info "\n"
    log.info "Here is the list of flags accepted by the pipeline:\n"
    log.info "--query_sr               input fasta file with one or more sequences in it, SR will be performed on all the input sequences (seq)."
    log.info "                         If more than one input fasta has to be passed to the pipeline, (for embarassing parellization porpuses for ex.)"
    log.info "                         pass the path to a directory like ->     --query_sr test/     (absoluth and relative paths are accepted."
    log.info "                         the relative path refers to the directory from which the command   nextflow run is launched."
    log.info "                         The multiple files can also be passed as glob pattern using the '*' charachter like:"
    log.info '                         nextflow run <this script name>  --query_sr "../test/example*.fasta"        ("" <- they are necessary)'	
    log.info "--out_name_sr            The name of the output file. it will be placed at params.OUTPUT_DIR  path, this flag is present in the nextflow.config "
    log.info "                         default value test/, it can be changed by command line as  --OUTPUT_DIR  your/dir/path/   same concepts of"
    log.info "                         <query_sr> path apply. As for now the output of all input files will be written to one same file, this behaviour  "
    log.info "                         might be changed in future for memory reason."
    log.info "                         Be aware that the policy for the output file is to override. Be carefull."
    log.info ""
    log.info ""
    log.info ""
    log.info "#### WARNING ####"
    log.info " this pipeline goes with the config file   sr_jaspar.config that import and necessitate the   uniprot_sparql_query.config  "
    log.info " config file in the same directory, in the github both file are present under the dir  conf/ "
    exit 1
}


// Modules dependencie section

include { sr_input_handler } from "./workflows/sr_jaspar"




workflow {
    if ( params.GIVEN_JASPAR_PROFILE) {                         // to check if the profile was given

		sr_input_handler(params.query_sr, params.out_name_sr)
		sr_input_handler.out.stdout.view()
		sr_input_handler.out.final_out.view()

    } else {                            // print error message reminder of the profile
        log.info "the     -profile sr_jaspar      flag has not been given in the command line or sr_jaspar was not among the profile specified"
                log.info "the sr_jaspar profile is mandatory as it contains all variable necessary for this script"
                log.info "it can be found at conf/sr_jaspar.config, go read it for more details"
                exit 1
        }

}
