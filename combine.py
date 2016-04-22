#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description='Combine two CSV files and display the result to stdout.')
parser.add_argument("-d", "--debug", help="Output debug messages", action="store_true")
parser.add_argument('left_file', help='left CSV filename')
parser.add_argument('right_file', help='right CSV filename')
args = parser.parse_args()

# 1. The <right> file may NOT be a previously combined file.

# 2. The <left> file may be a previously combined file.

# 3. If the module exists in both <left> and <right> files, then the combined record will look like this:
# <module>|l1,l2,l3,l4,l5;r1,r2,r3,r4,r5

# 4. If the module only exists in the <left> file, then the combined record will look like this:
# <module>|l1,l2,l3,l4,l5;,,,,

# 5. If the module only exists in the <right> file, then the combined record will look like this:
# <module>|,,,,;r1,r2,r3,r4,r5

# Dictionary to hold module KEY/VALUE pairs
module_dictionary = {}

# the CSV header row from the left file
left_header_row     = None

#
number_of_left_columns = None
number_of_right_columns = None

empty_module_values = None

def get_padding( header_string ):
    padding_string=""
    for character_value in header_string:
        if (character_value == ",") or (character_value == ";"):
            padding_string += str(character_value)
        else:
            continue
    return padding_string

# Parse the right file first because it is always fixed length
with open( args.left_file, 'r') as file:
  # read each line into a list of lines
  list_of_lines = file.readlines()

  # get the first 'header' line remove newline and divide it into 'columns'
  left_header_row = ( list_of_lines.pop(0).strip() )
  if args.debug: print "Left file header = {}".format( left_header_row )

  # get the number of keys to determine the number of expected tokens per line (plus semi colon)
  number_of_left_columns = len( left_header_row.split(",") ) + 1
  if args.debug: print "Number of columns from left file = {}".format( number_of_left_columns )

  # Add the header
  key_values = ( left_header_row.rstrip('\n') ).split("|")
  module_dictionary[ key_values[0] ] = key_values[1]

  for aline in list_of_lines:
      key_values = ( aline.rstrip('\n') ).split("|")
      if args.debug: print "Key: {} Value: {}".format( key_values[0], key_values[1] )
      module_dictionary[ key_values[0] ] = key_values[1]

# Parse the right file
with open( args.right_file, 'r') as file:

  # read each line into a list of lines
  list_of_lines = file.readlines()

  # get the first 'header' line remove newline and divide it into 'columns'
  right_header_row = ( list_of_lines.pop(0).strip() )
  if args.debug: print "Right file header = {}".format( right_header_row )

  # get the number of keys to determine the number of expected tokens per line
  number_of_right_columns = len( right_header_row.split(",") )
  if args.debug: print "Number of columns from right file = {}".format( number_of_right_columns )

  padding_for_left_file_values = get_padding(right_header_row)
  if args.debug: print "Left value padding = {}".format( padding_for_left_file_values )

  padding_for_right_file_values = get_padding(left_header_row)
  if args.debug: print "Right value padding = {}".format( padding_for_right_file_values )

  key_values = ( right_header_row.rstrip('\n') ).split("|")
  left_value = module_dictionary.get(key_values[0])
  module_dictionary[ key_values[0] ] = left_value+';'+key_values[1]
  if args.debug: print "New header: {}".format( left_value+';'+key_values[1] )

  for aline in list_of_lines:
      key_values = ( aline.rstrip('\n') ).split("|")
      right_module = key_values[0]
      if args.debug: print "Checking Key: {} Value: {}".format( right_module, key_values[1] )
      if module_dictionary.has_key( right_module ):
          if args.debug: print "Module '{}' exists in dictionary - merging".format( right_module )
          left_value = module_dictionary.get( right_module )
          module_dictionary[ right_module ] = left_value+';'+key_values[1]
          if args.debug: print "Merged: {}".format( left_value+';'+key_values[1] )
      else:
          if args.debug: print "Adding new module '{}' to dictionary".format( right_module )
          module_dictionary[ right_module ] = padding_for_right_file_values+';'+key_values[1]
          if args.debug: print "Added: {}".format( padding_for_right_file_values+';'+key_values[1] )

key_values = ( right_header_row.rstrip('\n') ).split("|")
print key_values[0]+'|'+ module_dictionary.get( key_values[0] )
del module_dictionary[key_values[0]]

for keyz,valuez in sorted( module_dictionary.items() ):
    if args.debug: print "value length: {} column length {}".format( len( valuez ), number_of_right_columns+number_of_left_columns )
    if args.debug: print "length: {} expected {}".format( valuez.count(","), ( padding_for_left_file_values+padding_for_right_file_values).count(",") )
    if valuez.count(",") <  ( padding_for_left_file_values+padding_for_right_file_values).count(","):
        print "{}|{}".format( keyz, valuez+';'+padding_for_left_file_values )
    else:
        print "{}|{}".format( keyz, valuez )
