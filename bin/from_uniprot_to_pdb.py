#!/usr/bin/env python3

# add yourself if you modify this and the date pls
# 14/02/2023 Alessio Vignoli        --start--

import argparse
from rdflib import Graph

def pdb_SPARQL_query(in_file, out_file, column_num, col_spatiator, skip_1line):

    # Optional flag handling and setting default values
    if not column_num:
        column_num = 0                                          # default first column
    else:
        column_num = int(column_num) -1                         # putting value in python notation starting from zero
    if not col_spatiator or str(col_spatiator)=='false':
        col_spatiator = "\t"                                    # setting field/column delimiter to a tab
    if not skip_1line or str(skip_1line)=='true' or str(skip_1line)=='True':
        skip_1line = True
    else:
        skip_1line = False

    
    # Actual functional section
    # list for already seen uniprot IDs
    seen_uniprotIDs = []
    # infromation to be written at the end
    to_be_written = ''
    with open(in_file, 'r') as infile:
        if skip_1line:
            infile.readline()                                   # skipping first line
        for line in infile:                                     # obtaining the IDs
            uniprotID = line.rstrip().split(col_spatiator)[column_num] 
            #print(uniprotID)
            if uniprotID in seen_uniprotIDs:                    # skipping already queried IDs
                continue
            else:
                seen_uniprotIDs.append(uniprotID)               # appending previously unseen IDs

            # Actual SPARQL query (can be gratly improved if the right query schema is built)
            g = Graph()
            url = "https://www.uniprot.org/uniprot/" + uniprotID + ".rdf"

            # get all protein info of the uniprot ID in graph format
            g.parse(url)
            all_info = g.serialize(format="turtle").split('\n')

            # Scan all the fields retrieved for the one of interest(no need for this step if the query was precise)
            # Series of checks on different lines because the pattern to identify the information is quite complicated
            # it is also complicated by the need to filter out non x-ray structures
            isoforms_check = False
            tmp_dict = {}
            buffer_line = ''
            for rdf_line in all_info:

                # first retrieving all structure informations associated to such uniprot entry
                if 'isoforms' in rdf_line and 'PDB' in rdf_line and ';' not in rdf_line and ' :chain ' in rdf_line:
                    pdbID =  rdf_line.split('#PDB_')[1].split('_')[0]
                    chain = rdf_line.split('"')[1].split('=')[0]
                    extremities = rdf_line.split('=')[1].split('"')[0]
                    tmp_dict[pdbID] = (chain, extremities)

                # The following block access the pdb information about type of structure like NMR or x-ray ecc.
                # if the strucure is x-ray then it is selected and outputted
                # since the information is on more then one line first the pdb ID has to retrieved once more to make a connection with the dictionary above
                # then x-ray is checked and the pdb id selected in case and then the flags resetted in order to check a new pdb block in the rdf 
                if rdf_line ==  '\n':
                    isoforms_check = False
                elif 'isoforms' in rdf_line:
                    isoforms_check = True
                    buffer_line = rdf_line
                elif 'X-Ray' in rdf_line and isoforms_check:
                    x_ray_pdbID = buffer_line.split('#PDB_')[1].split('_')[0]
                    
                    # filtering out short structures, like protein complexes where the interested protein is just a fragment of few aa
                    if (int((tmp_dict[x_ray_pdbID][1]).split('-')[1]) - int((tmp_dict[x_ray_pdbID][1]).split('-')[0])) > 15:
                        to_be_written += (uniprotID + '\t' + x_ray_pdbID + '\t' + tmp_dict[x_ray_pdbID][0] + '\t' + tmp_dict[x_ray_pdbID][1] + '\n')


    # Write to file if the option has been given
    if out_file:
        with open(out_file, 'w') as outfile:
            outfile.write('ref UniprotID\tpdbID\tchain\tStructure Start-End\n')
            outfile.write(to_be_written)
    else:
        print('ref UniprotID\tpdbID\tchain\tStructure Start-End\n')
        print(to_be_written)
                    

def main(args):
    
    pdb_SPARQL_query(args.infile, args.out, args.col, args.spatiator, args.skip_line)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="given a file containing uniprot ID on each row separated as you want, it queries Uniprot through the SPARQL rest API to retrieve associated pdb IDs - chain IDs - start - end information. If a given uniprtoID is encountered multiple times it would be searched only once. Is up to the user to make sure the uniprot IDs are correct.")
    parser.add_argument('-i', '--infile',  type=str, required=True, metavar="FILE", help='path to the input uniprot ID file')
    parser.add_argument('-o', '--out', type=str, required=False, metavar="FILE", help='output filename or path, if given output will be written to this location')
    parser.add_argument('--col', type=int, required=False, metavar="INT",  help='optional flag, the column where the ID is, default 1 first column')
    parser.add_argument('--spatiator', type=str, required=False, metavar="STR",  help='optional flag the digit/digits to use as spaciator, default "\\t" <tab>  for complex separator like < | > do this --spatiator " | "')
    parser.add_argument('--skip_line', type=str, required=False, metavar="BOOL",  help='optional flag, default true, meaning skip the first line in the ID file (column description), every other value given will prompt the script not to skip the first line')
    args = parser.parse_args()

    main(args)
