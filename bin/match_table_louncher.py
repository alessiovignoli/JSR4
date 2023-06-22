#!/usr/bin/env python3

import argparse
from python_codebase.tabular_matcher import MatchByKeyPos

def get_args():

    "get the arguments when using from the commandline"

    parser = argparse.ArgumentParser(description='this simple script takes as input two table files, with each line divided by a uniq separator like csv or tsv files. It will write an output file the union of thistwo files using a matching key. Basically every line in file1.csv will be matched to one or more line in file2.tsv based on a commonn field that function as a key. \nFor example\n\tline 1 in file1 is ->  a,b,c,d\n\tline2 in file2 is ->  e f b g h\n if the field containing b in both file is provided the script will write in the output file :\na,b,c,d,e,f,g,h\n\nNote that if the two files are from different formats the output will be in the formast of the first file given.\nWarning if line1 in file1 does not match any line in file2 that line will not be written in the output file, same goes for line2 in file2.', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-f1", "--input1", type=str, required=True, metavar="FILE", help='first input file, the file has to have a unique spatiator/delimiter never found in the field separated by it, all line in this file must abide to this rule. At least the column of the key used for matching should always have the same position in every line.')
    parser.add_argument("-f2", "--input2", type=str, required=True, metavar="FILE", help='the above rules have to apply to this file as well')
    parser.add_argument("-o", "--output", type=str, required=True, metavar="FILE", help='the outputfilename or path')
    parser.add_argument("-p1", "--pos1", type=int, required=False,  nargs='?', default=0, metavar="field/column position/index", help='default 0, integer pointing to the column/field to be used as a key in file1, WARNING the notation must be python based, meaning first field = 0')
    parser.add_argument("-p2", "--pos2", type=int, required=False,  nargs='?', default=0, metavar="field/column position/index", help='same rule as above but this applies to file2 instead.')
    parser.add_argument("-d1", "--delimiter1", type=str, required=False,  nargs='?', const='\t', default='\t', metavar="delimiter/spatiator", help='default <tab>, with this flag the spatiator/delimiter of the file can be specified, it can be whatever string, for special charachters use either \' or \" to encapsulate them, they have to be pythonic simbols.')
    parser.add_argument("-d2", "--delimiter2", type=str, required=False,  nargs='?', const='\t', default='\t', metavar="delimiter/spatiator", help='all rules as above apply, it can be different from the value given to the above flag, in that case the output file will be delimited using the above flag value.')
    parser.add_argument("--check_types", required=False, nargs='?', default=False, metavar="debug", help='default False, no type of the variables will be checked at line level inside the script, this flag is usefull for debugging.')

    args = parser.parse_args()
    return args


def main(file_1, file_2, output, pos1=0, pos2=0, del1='\t', del2='\t', check=False):

    # Open the files and read them line by line
    with open(file_1, "r") as file1, open(output, 'w') as out:
        for line1 in file1:
            with open(file_2, "r") as file2:
                for line2 in file2:
                    matched_lines = MatchByKeyPos(line1, line2, pos1, pos2, del1, del2, check)
                    matched_line = matched_lines.Match()
                    if matched_line:
                        out.write(matched_line)



if __name__ == "__main__":
    args = get_args()

    # To handle complications from command line string arguments
    if args.check_types == 'false' or args.check_types == 'False':
        args.check_types = False

    main(args.input1, args.input2, args.output, args.pos1, args.pos2, args.delimiter1, args.delimiter2, args.check_types)
