################################################################################
#
#   MRC FGU Computational Genomics Group
#
#   $Id: cgat_script_template.py 2871 2010-03-03 10:20:44Z andreas $
#
#   Copyright (C) 2009 Andreas Heger
#
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 2
#   of the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#################################################################################
'''
cgat.py - Computational Genomics Analysis Tools
===============================================

:Author: Andreas Heger
:Release: $Id$
:Date: |today|
:Tags: Python

The tools are grouped by keywords. For this message 
and a list of available tools type::
    
    cgat --help

For a list of tools matching a certain keyword, type::

   cgat --help <keyword>

Use::

   cgat --help all

for a list of all available tools.

To get help for a specific command, type::

    cgat <command> --help
'''

import os
import sys
import glob
import imp
import collections

def mapKeyword2Script( path ):
    '''collect keywords from scripts.'''
    
    map_keyword2script = collections.defaultdict( list )

    for script in glob.glob( os.path.join( path, "*.py") ):
        s = os.path.basename(script)[:-3]
        with open( script, 'r') as inf:
            data = [ x for x in inf.readlines( 10000 ) if x.startswith(':Tags:') ]
            if data:
                keywords = [x.strip() for x in data[0][5:].split(' ')]
                for x in keywords:
                    map_keyword2script[x].append( s )
    return map_keyword2script

def printListInColumns( l, ncolumns ):
    '''output list *l* in *ncolumns*.'''
    
    ll = len(l)
    max_width = max( [len(x) for x in l ] ) + 3
    n = ll // ncolumns
    if ll % 3 != 0: n += 1
        
    # build columns
    columns = [ l[x*n:x*n+n] for x in range(ncolumns ) ]

    # add empty fields for missing columns in last row
    for x in range( len(l) % ncolumns): columns[-x].append('')

    # convert to rows
    rows = zip( *columns )

    # build pattern for a row
    p = '%-' + str(max_width) + 's' 
    pattern = ' '.join( [ p for x in range(ncolumns) ] )
    
    # put it all together
    return '\n'.join( [ pattern % row for row in rows ] )

def main():

    argv = sys.argv

    path = os.path.abspath( os.path.dirname(__file__) )

    if len(argv) == 1 or argv[1] == "--help" or argv[1] == "-h":
        print(globals()["__doc__"])

        map_keyword2script = mapKeyword2Script( path )

        if len(argv) <= 2:
            
            print('CGAT tools are grouped by keywords. The following keywords')
            print('are available:')
            print("%s\n" % printListInColumns( map_keyword2script.keys(),
                                               3 ))

        if 'all' in argv[2:]:
            print("The list of all available commands is:\n" )
            print("%s\n" % printListInColumns( 
                    sorted([os.path.basename(x)[:-3] \
                                for x in glob.glob( os.path.join( path, "*.py") )]),
                    3 ))

        else:
            for arg in argv[2:]:
                if arg in map_keyword2script:
                    print ( "Tools matching the keyword '%s':\n" % arg )
                    print ( '%s\n' % printListInColumns(
                                        sorted(map_keyword2script[arg]),
                                        3 ) )
        return

    command = argv[1]

    (file, pathname, description ) = imp.find_module( command, [path,] )
    module = imp.load_module( command, file, pathname, description)
    module.main( sys.argv )
    
if __name__ == "__main__":
    sys.exit( main() )
