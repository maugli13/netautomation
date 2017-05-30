#!/usr/bin/python
import argparse
import base64

parser = argparse.ArgumentParser(description='Sonicwall exp file converter')
parser.add_argument('-i','--input',help='Input .exp file name',required=True)
parser.add_argument('-o','--output',help='Output file name', required=True)
args = parser.parse_args()
 
## show values ##
#print ("Input file: %s" % args.input )
#print ("Output file: %s" % args.output )
with open(args.input, 'r') as inputfile:
	contents = inputfile.read()
	outputfile = open(args.output, 'w')
	outputfile.write(str((base64.b64decode(contents, altchars=None))).replace('&', '\n'))
