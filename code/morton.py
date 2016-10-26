########################################################################
#morton.py
#v0.1
#A lightweight version of Jeroen Baert's LibMorton rewritten in python,
#with added Morton encoding/decoding routines for 2D keys, and
#bug fixes for errors in 3D key encoding/decoding.

#Distributed under the MIT License.

#Copyright (c) 2016 Jeroen Baert
#Copyright (c) 2016 Jacob Pelletier 

#Permission is hereby granted, free of charge, to any person obtaining a
#copy of this software and associated documentation files (the "Software"), 
#to deal in the Software without restriction, including without limitation 
#the rights to use, copy, modify, merge, publish, distribute, sublicense, 
#and/or sell copies of the Software, and to permit persons to whom the 
#Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included 
#in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
#OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
#THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR 
#OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
#ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR 
#OTHER DEALINGS  IN THE SOFTWARE.


########################################################################

#-----------------------------------------------------------------------
#Imports
import numpy

#-----------------------------------------------------------------------
#2D Encoding

def split_by_2(a):
    x = numpy.uint64(a) & numpy.uint64(0xffffffff)
    x = (x | x << numpy.uint64(16)) & numpy.uint64(0x0000ffff0000ffff)
    x = (x | x << numpy.uint64(8)) & numpy.uint64(0x00ff00ff00ff00ff)
    x = (x | x << numpy.uint64(4)) & numpy.uint64(0x0f0f0f0f0f0f0f0f)
    x = (x | x << numpy.uint64(2)) & numpy.uint64(0x3333333333333333)
    x = (x | x << numpy.uint64(1)) & numpy.uint64(0x5555555555555555)
    return x
    
def encode_magicbits_2D(x, y):
    return ((split_by_2(numpy.uint64(y)) << numpy.uint64(1)) | split_by_2(numpy.uint64(x)))


#-----------------------------------------------------------------------
#2D Decoding

def get_second_bits(x):
    x = numpy.uint64(x) & numpy.uint64(0x5555555555555555)
    x = (x | (x >> numpy.uint64(1)))  & numpy.uint64(0x3333333333333333)
    x = (x | (x >> numpy.uint64(2)))  & numpy.uint64(0x0f0f0f0f0f0f0f0f)
    x = (x | (x >> numpy.uint64(4)))  & numpy.uint64(0x00ff00ff00ff00ff)
    x = (x | (x >> numpy.uint64(8))) & numpy.uint64(0x0000ffff0000ffff)
    x = (x | (x >> numpy.uint64(16))) & numpy.uint64(0x00000000ffffffff)
    
    #This takes 5 shifts, 5 Ors, and 6 Ands.
    return x

def decode_magicbits_2D(morton):
    y = get_second_bits(numpy.uint64(morton) >> numpy.uint64(1))
    x = get_second_bits(morton)
    return (numpy.uint32(x),numpy.uint32(y))

  
#-----------------------------------------------------------------------
#3D Encoding

def split_by_3(a):
    x = numpy.uint64(a) & numpy.uint64(0x1fffff)
    x = (x | x << numpy.uint64(32)) & numpy.uint64(0x1f00000000ffff)
    x = (x | x << numpy.uint64(16)) & numpy.uint64(0x1f0000ff0000ff)
    x = (x | x << numpy.uint64(8)) & numpy.uint64(0x100f00f00f00f00f)
    x = (x | x << numpy.uint64(4)) & numpy.uint64(0x10c30c30c30c30c3)
    x = (x | x << numpy.uint64(2)) & numpy.uint64(0x1249249249249249)
    
    #This takes 5 shifts, 5 Ors, and 6 Ands.
    return x
    
def encode_magicbits_3D(x, y, z):
    return ((split_by_3(z) << numpy.uint64(2))| (split_by_3(y) << numpy.uint64(1)) | split_by_3(x))

#Note that only 21bits of each x,y,z coordinate is available for converting to
#a 63bit Morton key.

#-----------------------------------------------------------------------
#3D Decoding

def get_third_bits(x):
    #Original function was flawed. Corrections were made by trial and 
    #error and tested to be correct. A published reference to the correct 
    #implementation was also found in the discussion posted on stack overflow  
    #and linked below. There are other good suggestions in this post which
    #need further investigation for performance improvements in the c++ version.
    #Reference: http://stackoverflow.com/questions/4909263/how-to-efficiently-de-interleave-bits-inverse-morton/28358035#28358035
    x = x & numpy.uint64(0x9249249249249249)
    x = (x | (x >> numpy.uint64(2)))  & numpy.uint64(0x30c30c30c30c30c3)
    x = (x | (x >> numpy.uint64(4)))  & numpy.uint64(0xf00f00f00f00f00f)
    x = (x | (x >> numpy.uint64(8)))  & numpy.uint64(0x00ff0000ff0000ff)
    x = (x | (x >> numpy.uint64(16))) & numpy.uint64(0xffff00000000ffff)
    x = (x | (x >> numpy.uint64(32))) & numpy.uint64(0x00000000ffffffff)
    
    #//This takes 5 shifts, 5 Ors, and 6 Ands.
    return x

def decode_magicbits_3D(morton):
    z = get_third_bits(morton>>numpy.uint64(2))
    y = get_third_bits(morton>>numpy.uint64(1))
    x = get_third_bits(morton)
    return (numpy.uint32(x), numpy.uint32(y), numpy.uint32(z))
   
#-----------------------------------------------------------------------
#That's all folks!
