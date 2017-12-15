pymorton
========
### v0.1

A simple cli interface for encoding/decoding 2d and 3d unsigned integer coordinates to/from  
Morton codes via the shell.  In all cases Morton Codes are generated as 64bit unsigned integers.  
Coordinate tuples consist of 32bit precision unsigned integers in the case of 2d, and 21bit  
precision unsigned integers in the 3d case. This is prototype-grade code written in python 3,  
compatible with *nix-like operating systems, and distributed under the MIT License.

## Installation

1) Clone with git or untar the package to a local folder of your choosing.  
2) Create a symlink from the package's pymorton to ~/.local/bin  
   or a different folder that exists in your path.

## Usage: 
  pymorton --encode  
  pymorton --decode=2d  
  pymorton --encode < test.xy > test.morton2d  
  pymorton --decode=3d < test.morton3d > test.xyz  
   
## Options:
####  -d, --decode
    Decode stdin morton codes to coordinates on stdout.
####  -e, --encode
    Encode stdin coordinates to morton codes on stdout.
####  -i, --interactive
    Perform conversions interactively.
####  -t, --test
    Test encoding/decoding routines.  
####  -N, --number
    Set the number of samples to use for tests.
####  -h, --help
    Show help screen.
####  -V, --version
    Show version info.

## Notes:
1) The input of coordinate tuples must be separated by a newline character.  
2) Tuple components (x,y,z) must be tab or space delimited.  
3) Input and output files can be used via shell pipes.  
4) Decoding requires one to specify 2d or 3d conversion.  
5) Encoding will detect 2d or 3d conversion based on the number of components of the first coordinate entry.  

## To do:
1) Buffer input and output streams so that numpy genfromtxt commands can be leveraged for higher performance.  
2) Build an actual python wrapper to Jeroen Baert's c++ LibMorton for higher performance.  
3) Rewrite pymorton in c++ to serve as a cli interface to LibMorton.  
