#
# This Python script generates a BOM from a KiCad generic netlist using the markdown syntax
#
"""
@package
Generate a BOM list in markdown syntax.
    
Components are sorted by ref and grouped by :
    - Family, Part number, value and footprint
        
Fields are (if exist) :
    - Quantity
    - Ref
    - Description
    - Part number
    - Footprint
    - Value
"""

__version__    = "0.1"
__author__     = "Benoit Frigon"
__license__    = "GPL"
__copyright__  = "Licensed under the GPL license"
__email__      = "benoit@frigon.info"


#=========================================================================================
import sys
import os
from bom_generator import BOM 


#=========================================================================================
class BOM_MARKDOWN( BOM ):
    
    
    #----------------------------------------------------------------------------
    def __init__( self, file_in, file_out ):
        BOM.__init__( self, file_in )
        
        try:
            
            file_out = os.path.join( os.path.dirname( file_in ), file_out )
            output_dir = os.path.dirname( file_out )
            
            #---- Create the output directory if it does not exists ----
            if not os.path.exists( output_dir ):
                os.makedirs( output_dir )
            
            self.f_output = open( file_out, 'w' )
            
        except IOError:
            print( '%s: Can\'t open output file for writing: %s' % ( __file__, file_out ) )
            sys.exit( -1 )
    
    
    #----------------------------------------------------------------------------
    def generate( self ):
        
        self.f_output.write( '### Bill of material ###\n\n' )
        
        #---- Write the title block ----
        self.f_output.write( '```\n' )
        self.f_output.write( 'Date    : %s\n' % ( self.title_block[ 'drawing_date' ] ) )
        self.f_output.write( 'Doc. ID : %s\n' % ( self.title_block[ 'drawing_id' ] ) )
        self.f_output.write( 'Project : %s\n' % ( self.title_block[ 'project' ].title() ) )
        self.f_output.write( 'Title   : %s\n' % ( self.title_block[ 'title' ].title() ) )
        self.f_output.write( '\n' )
        self.f_output.write( 'Part #  : %s\n' % ( self.title_block[ 'part_id' ] ) )
        self.f_output.write( 'REV.    : %s\n' % ( self.title_block[ 'rev' ] ) )
        self.f_output.write( '\n' )
        self.f_output.write( 'Components : %d\n' % ( len( self.components ) ) )
        self.f_output.write( '```\n\n' )
        self.f_output.write( '-' * 120 )
        self.f_output.write( '\n\n\n' )
        
        #---- Build the header ----
        rows = []
        row = [ 
            'Qty', 
            'Ref.', 
            'Description', 
            'Value',
            'Part #', 
            #'Manufacturer', 
            'Footprint'
        ]
        
        columns_width = self.calculate_max_width( [], row )
        rows.append( row )
        
        #---- Group the components ----
        groups = self.group_components()
        
        #---- Build the group list ----
        for group in groups:
            
            row = [
                str( group[ 'qty' ] ),
                self.format_ref_list( group[ 'refs' ] ), 
                group[ 'description' ],
                group[ 'value' ],
                group[ 'part_no' ],
                #group[ 'part_mfg' ],
                group[ 'footprint' ]
            ]
            
            columns_width = self.calculate_max_width( columns_width, row )
            rows.append( row )
        
        #---- Write the header. ----
        self.write_row( rows[0], columns_width )
        
        #---- Write the header separator ----
        self.f_output.write('|')
        for width in columns_width:
            self.f_output.write( '-' * ( width + 2 ) + '|' )
            
        self.f_output.write('\n')
        
        #---- Write the remaining rows ----
        for row in rows[1:]:
            self.write_row( row, columns_width )
    
    
        self.f_output.close()
        

    #----------------------------------------------------------------------------
    def write_row( self, columns, columns_width = [] ):
        
        for index, column in enumerate( columns ):
            columns[ index ] = column.ljust( columns_width[ index ] )
        
        self.f_output.write( '| ' )
        self.f_output.write( ' | '.join( columns ) )
        self.f_output.write( ' |\n' )

    #----------------------------------------------------------------------------
    def calculate_max_width( self, columns_width, columns ):
        
        if( len( columns_width ) == 0 ):
            columns_width = [ 0 for _ in range( len( columns ) ) ]
        
        for index, column in enumerate( columns ):
            columns_width[ index ] = max( len( column ), columns_width[ index ] )
                
        return columns_width



#====================================================================================================

bom = BOM_MARKDOWN( sys.argv[ 1 ], sys.argv[ 2 ] )
bom.generate()




