#!/usr/bin/env python3

from file_existance import FileExists
from tabular import ExtractField
from count_lines import LineCounter



class TableParser():

    """
    Very general and broad class for parsing a tabular format file. This time the input is the whole file in itself. (as string).
    Evrey line should have one or more fields, all separated by an unique separator, 
    files that abide to this concepts are tsv and csv for example.
    It is not thought to write the input file just to read and do stuff based on reading.
    The values intialized are the opened file object, theeparator aka delimiter,
    total number of lines in file and the header presence flag + the nuber of header lines.
    """

    def __init__(self, infile, delimiter='\t', header=True, header_lines=1) -> None:
        self.infile = infile
        self.delimiter = delimiter
        
        # Set header related variables  
        self.header = header
        if header:
            self.header_lines = header_lines
        else:
            self.header_lines = 0
        
        # Check if file exists before doing anything
        exists = FileExists(infile)
        exists.Check()

    
    def TotalLines(self):

        """
        simple function for counting total number of lines in file
        """

        with open(self.infile, 'r') as intab:
            line_counter = LineCounter(intab)
            total_count = line_counter.Count_lines()
        return total_count




class PercentageIDs(TableParser):

    """
    This class has function related to a single field, all info that can be computed extracting just one column.
    """

    """
    This class is thought to contain all the functiones that have to scroll throught the file and count how many
    of a given field IDs have a certain property. 
    For example The id bubba is found on one or many lines (ex. field one), field one has also many others IDs (unique or not),
    this class will answer questions like: how many IDs in field one have given value in field 3? ecc..
    """

    def __init__(self, infile, id_pos, delimiter='\t', header=True, header_lines=1) -> None:
        super().__init__(infile, delimiter, header, header_lines)
        self.id_pos = id_pos


    def CountUniqueIDs(self):
        
        """
        this function computes how many values of given field/column are unique, aka not identical, using exact string matching
        """

        seen_ids = []
        with open(self.infile, 'r') as in_file:
            for line in in_file:
                extract_obj = ExtractField(line, self.id_pos, self.delimiter)
                id_value = extract_obj.Get_Field()
                #print(id_value)
                seen_ids.append(id_value)
        return seen_ids

