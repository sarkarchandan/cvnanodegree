from __future__ import annotations
from multiprocessing.sharedctypes import Value
import matplotlib.pyplot as plt
'''
The color class creates a color from 3 values, r, g, and b (red, green, and blue).

attributes:
    r - a value between 0-255 for red
    g - a value between 0-255 for green
    b - a value between 0-255 for blue
'''
    
class Color(object):

    r: int
    g: int
    b: int
    
    # __init__ is called when a color is constructed using color.Color(_, _, _)
    def __init__(self, r: int, g: int, b: int) -> None:
        # Setting the r value
        self.r = r
        self.g = g
        self.b = b
        

    # __repr__ is called when a color is printed using print(some_color)
    # It must return a string
    def __repr__(self) -> str:
        '''Display a color swatch and then return a text description of r,g,b values.'''
        plt.imshow([[(self.r/255, self.g/255, self.b/255)]])
        ## TODO: Write a string representation for the color
        ## ex. "rgb = [self.r, self.g, self.b]"
        ## Right now this returns an empty string
        string = f'Color(r={self.r}, g={self.g}, b={self.b})'
        return string

    # Overload __add__ method
    def __add__(self, rhs: Color) -> Color:
        if isinstance(rhs, Color):
            return Color(r=self.r + rhs.r, g=self.g+rhs.g, b=self.b+rhs.b)
        else:
            raise ValueError('Invalid operand, expected Color, got: {type(rhs)}')
    
    