#!/usr/bin/env python3

from sys import exit

class TypeErrorMessage():
    """
    This is a helper class for error type messages that will be used by other classes for sending error type messages 
    all subclass of this one should be variable type specific and they should be composed instead of inherited
    """

    def Asses_Type(self):
        print('This error type is not yet implemented as a class\nplease do so yourself')
        exit(1)


class StrTypeErr(TypeErrorMessage):

    def __init__(self, variable) -> None:
        self.variable = variable

    def Asses_Type(self):
        if not isinstance(self.variable, str):
            print('not the correct datat type')
            exit(1)
        #return isinstance(self.variable, str)
