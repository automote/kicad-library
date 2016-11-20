#
# This Python script contains the base class for BOM generator, it only parses the 
# XML netlist and store the results in a dictionary. It produces no output.
#
"""
    @package
    Base class for the BOM generator
"""


__version__    = "0.1"
__author__     = "Benoit Frigon"
__license__    = "GPL"
__copyright__  = "Licensed under the GPL license"
__email__      = "benoit@frigon.info"


#=========================================================================================
import os
import sys
import re
import xml.etree.ElementTree as ET


#=========================================================================================
class BOM:
    
    
    
    footprint_replace = {
        'SMT:C-' : 'SMT-',
        'SMT:R-' : 'SMT-',
        'SMT:C-' : 'SMT-',
        'SMT:FER-' : 'SMT-',
        'SMT:CPL-' : 'SMT-',
        'Crystals:' : '',
        'SMT-SOT:SOT-' : 'SOT-',
        'Conn-Hirose:' : '',
        'Conn-IO:' : '',
        'Conn-Header:' : '',
        'Conn-Power:' : '',
        'SMT-SOIC:' : 'SOIC-',
        'SMT-SOP:' : '',
        
    }
    
    
    
    
    #----------------------------------------------------------------------------
    def __init__( self, file_in = "" ):
        self.components = []
        self.libparts = {}
        
        self.group_fields = [ 'family', 'part_no', 'value', 'footprint' ]

        self.file_in = file_in
        if file_in:
            self.parse( file_in )
        
        
    #----------------------------------------------------------------------------
    def parse( self, file_in ):
        try:
            
            tree = ET.parse( file_in )
            root = tree.getroot()
            
            self.parse_title_block( root )
            self.parse_libparts( root )
            self.parse_components( root )
                
            
        except IOError as e:
            print( "%s: %s" % ( __file__, e ) )
            sys.exit( -1 )


    #----------------------------------------------------------------------------
    def parse_title_block( self, root):
        
        elm_design = root.find( 'design' )
        if( elm_design is None):
            return
        
        info = { 'generated' : '',
                 'tool' : '',
                 'title' : '',
                 'company' : '',
                 'rev' : '',
                 'project' : '',
                 'drawing_id' : '',
                 'part_id' : '',
                 'drawing_date' : '' }
        
        
        elm_generated = elm_design.find( 'date' )
        if( elm_generated is not None ):
            info['generated'] = elm_generated.text
            
        elm_tool = elm_design.find( 'tool' )
        if( elm_tool is not None ):
            info['tool'] = elm_tool.text
        
        elm_sheet = elm_design.find( 'sheet' )
        if (elm_sheet is not None ):
            
            elm_title_block = elm_sheet.find('title_block')
            if ( elm_title_block is not None ):
            
                elm_title = elm_title_block.find( 'title' )
                if( elm_title is not None ):
                    info[ 'title' ] = elm_title.text
            
                elm_company = elm_title_block.find( 'company' )
                if( elm_company is not None ):
                    info[ 'company' ] = elm_company.text
            
                elm_rev = elm_title_block.find( 'rev' )
                if( elm_rev is not None ):
                    info[ 'rev' ] = elm_rev.text
            
                elm_date = elm_title_block.find( 'date' )
                if( elm_date is not None ):
                    info[ 'drawing_date' ] = elm_date.text
            
                for elm_comment in elm_title_block.findall( 'comment' ):
                    
                    number = int(elm_comment.get( 'number', '0' ) )
                    
                    if (number == 1):
                        info['part_id'] = elm_comment.get( 'value', '' )
                        
                    if (number == 2):
                        info['drawing_id'] = elm_comment.get( 'value', '' )
                    
                    if (number == 3):
                        info['project'] = elm_comment.get( 'value', '' )

        self.title_block = info

    #----------------------------------------------------------------------------
    def parse_components( self, root ):
        
        self.components = []
        
        elm_components = root.find( 'components' )
        if( elm_components is None):
            return
        
        for elm_comp in elm_components.findall( 'comp' ):
            
            comp = { 'ref'          : elm_comp.get( 'ref' ),
                     'description'  : '',
                     'footprint'    : '',
                     'part_no'      : '',
                     'part_mfg'     : '',
                     'value'        : '',
                     'family'       : '',
                     'lib_source'   : '',
                     'docs'         : '',
                     'installed'    : True }
            
            elm_value = elm_comp.find( 'value' )
            if( elm_value is not None ):
                comp[ 'value' ] = elm_value.text
            
            elm_footprint = elm_comp.find( 'footprint' )
            if( elm_footprint is not None ):
                
                footprint = elm_footprint.text
                
                for search, replace in self.footprint_replace.iteritems():
                    footprint = footprint.replace( search, replace )
                
                comp[ 'footprint' ] = footprint
        
            elm_fields = elm_comp.find( 'fields' )
            if( elm_fields is not None ):
                self.parse_component_fields(elm_fields, comp)
            

            # Get the library part data associated with this component
            elm_libsource = elm_comp.find( 'libsource' )
            if( elm_libsource is not None ):
                
                lib_name = elm_libsource.get( 'lib', '' )
                part_name = elm_libsource.get( 'part', '' )
                comp[ 'lib_source' ] = lib_name + ':' + part_name
                
                libpart = self.libparts[ comp[ 'lib_source' ] ]
                
                
                if( comp[ 'description' ] == '' ):
                    comp[ 'description' ] = libpart[ 'description' ]
                    
                if( comp[ 'part_mfg' ] == '' ):
                    comp[ 'part_mfg' ] = libpart[ 'part_mfg' ]
                    
                if( comp[ 'part_no' ] == '' ):
                    comp[ 'part_no' ] = libpart[ 'part_no' ]
                
                if( comp[ 'family' ] == '' ):
                    comp[ 'family' ] = libpart[ 'family' ]
                    
                if( comp[ 'docs' ] == '' ):
                    comp[ 'docs' ] = libpart[ 'docs' ]


            if( comp[ 'part_mfg' ] == '' ):
                comp[ 'part_mfg' ] = '-'

            if( comp[ 'part_no' ] == ''):
                comp[ 'part_no' ] = '-'
                
            if( comp[ 'value' ] == ''):
                comp[ 'value' ] = '-'

            if( not self.exclude_from_bom( comp ) ):
                self.components.append( comp )

    
    #----------------------------------------------------------------------------            
    def parse_component_fields( self, elm_fields, comp ):
        
        for elm_field in elm_fields.findall( 'field' ):
            
            name = elm_field.get( 'name', '' ).lower()
            value = elm_field.text
            
            if( name == 'family' ):
                comp[ 'family' ] = value.lower()

            if( name == 'mfg' ):
                comp[ 'part_mfg' ] = value
            
            if( name == 'part' ):
                comp[ 'part_no' ] = value
                
            if( name == 'installed' ):
                comp[ 'installed' ] = value.lower().strip() in [ 'true', 'yes', 'y', 't', '1', 'ok', 'installed' ]


        if( comp[ 'family' ] in [ 'ic', 'connector', 'switch' ] ):
            
            if( comp[ 'part_no' ] == "" ):
                comp[ 'part_no' ] = comp[ 'value' ]
                comp[ 'value' ] = "-"           


    #----------------------------------------------------------------------------
    def parse_libparts( self, root ):
        elm_libparts = root.find( 'libparts' )
        if( elm_libparts is None):
            return
        
        for elm_part in elm_libparts.findall( 'libpart' ):
            
            part = { 'library'      : elm_part.get( 'lib', '' ),
                     'name'         : elm_part.get( 'part', '' ),
                     'description'  : '',
                     'docs'         : '',
                     'family'       : '',
                     'part_no'      : '',
                     'part_mfg'     : '' }
            
            elm_desc = elm_part.find( 'description' )
            if( elm_desc is not None ):
                part[ 'description' ] = elm_desc.text
                
            elm_docs = elm_part.find( 'docs' )
            if( elm_docs is not None ):
                part[ 'docs' ] = elm_docs.text
            
            elm_fields = elm_part.find( 'fields' )
            if( elm_fields is not None ):
                self.parse_libpart_fields( elm_fields, part )
            
            
            self.libparts[ part[ 'library' ] + ':' + part[ 'name' ] ] = part

    
    #----------------------------------------------------------------------------
    def parse_libpart_fields( self, elm_fields, part ):
        
        for elm_field in elm_fields.findall( 'field' ):
            
            name = elm_field.get( 'name', '' ).lower()
            value = elm_field.text
            
            if( name == 'family' ):
                part[ 'family' ] = value.lower()

            if( name == 'mfg' ):
                part[ 'part_mfg' ] = value
            
            if( name == 'part' ):
                part[ 'part_no' ] = value
    
    
    #----------------------------------------------------------------------------
    def exclude_from_bom( self, component ):
        
        if( component[ 'installed' ] == False):
            return True
        
        if( component[ 'family' ] == 'virtual' ):
            return True
        
        return False
    
    
    #----------------------------------------------------------------------------
    def group_components( self, fields = [] ):
        
        if( len( fields ) > 0 ):
            self.group_fields = fields
        
        for comp in self.components:
            groupid = ''
           
            for field in self.group_fields:
                if( field in comp ):
                    groupid = groupid + str( comp[ field ] ).strip().lower()

            comp[ '__groupid' ] = groupid
            
        
        sorted_components = sorted( self.components, key=lambda k: k[ '__groupid' ] ) 
        
        cur_group_id = None
        groups = []
        
        for comp in sorted_components:

            if( comp[ '__groupid' ] != cur_group_id ):
                cur_group_id = comp[ '__groupid' ]
                
                group = {}
                groups.append(group)
                
                group[ 'refs' ] = []
                group[ 'qty' ] = 0
                
                
                for key, value in comp.iteritems():
                    if( key in [ '__groupid', 'ref' ] ):
                        continue
                    
                    group[ key ] = value
                
                
            group[ 'qty' ] += 1
            group[ 'refs' ].append( comp[ 'ref' ] )
            
        return groups    
            
   
    #----------------------------------------------------------------------------            
    def format_ref_list( self, refs, group = True ):
        sorted_refs = []
        groups = []
        output = ''
        
        #---- Split the prefix and id of each references. ---- 
        for ref in refs:
            sorted_refs.append( re.findall( r'(\D*)(\d*)', ref )[ 0 ] )

        #---- Sort the reference list ----
        sorted_refs = sorted( sorted_refs, key=lambda k: '%s%05d' % ( k[ 0 ], int( '0' + k[ 1 ] ) ) ) 
   
        group_start = 0
   
        for index, ref in enumerate( sorted_refs ):
            
            ref_prefix = ref[ 0 ]
            ref_id = int( ref[ 1 ] ) if ref[ 1 ].isdigit() else -1
            
            #---- Check if the next item is a consecutive number and have the same prefix. ----
            if( index < len( sorted_refs ) - 1 ):
                next_ref = sorted_refs[ index + 1 ]
                
                next_prefix = next_ref[ 0 ]
                next_id = int( next_ref[ 1 ] ) if next_ref[ 1 ].isdigit() else -1
                
                if ( group == True and ref_id + 1 == next_id and next_prefix == ref_prefix ):
                    continue
            
            #---- Add the first item of the group to the list. ----
            output += ''.join( sorted_refs[ group_start ])
            
            #---- If the group contains more than one item, add the last item to the list. ----
            if( group_start != index ):
                output += '-' + ''.join( sorted_refs[ index ])
            
            if( index < len( sorted_refs ) - 1 ):
                output += ', '
            
            group_start = index + 1
            
        return output


    #----------------------------------------------------------------------------            
    def generate( self ):
        pass        