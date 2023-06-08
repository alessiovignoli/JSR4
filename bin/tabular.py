#!/usr/bin/env python3

from type_error_messages import StrTypeErr
from type_error_messages import IntTypeErr



class TabularLine():
    """
    tabular specific helper functions are stored in this class, it is meant to work on strings instead of files.
    The idea behind is to work on files line by line to decreas memory usage.
    It by default checks if the two input are of the correct type -> both string type
    """

    def __init__(self, string, delimiter='\t') -> None:
        self.string = string
        self.delimiter = delimiter
        err_message1 = StrTypeErr(self.string, 'TabularLine.string')
        err_message1.Asses_Type()
        err_message2 = StrTypeErr(self.delimiter, 'TabularLine.delimiter')
        err_message2.Asses_Type()


  
class ExtractField(TabularLine):
    """
    extracts and returns the requested field from the line
    """

    def __init__(self, string, position, delimiter='\t') -> None:
        super().__init__(string, delimiter)
        self.position = position
        err_mssg_pos = IntTypeErr(self.position, 'ExtractField.position')
        err_mssg_pos.Asses_Type()
    
    def Get_Field(self):
        return (self.string.split(self.delimiter)[self.position])
   
