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
            for rdf_line in all_info:
                if 'isoforms' in rdf_line and 'PDB' in rdf_line and ';' not in rdf_line:
                    pdbID = rdf_line.split('#PDB_')[1].split('_')[0]
                    chain = rdf_line.split('"')[1].split('=')[0]
                    extremities = rdf_line.split('=')[1].split('"')[0]
                    to_be_written += (uniprotID + '\t' + pdbID + '\t' + chain + '\t' + extremities + '\n')

    # Write to file if the option has been given
    if out_file:
        with open(out_file, 'w') as outfile:
            outfile.write(to_be_written)
    else:
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
