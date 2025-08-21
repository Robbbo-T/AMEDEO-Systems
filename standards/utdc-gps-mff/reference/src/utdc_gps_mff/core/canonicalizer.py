"""
UTDC-GPS-MFF Canonicalizer Implementation
UTCS-MI: EstándarUniversal:Codigo-Desarrollo-UTDC-01.03-Canonicalizer-0001-v1.0-AerospaceAndQuantumUnitedAdvancedVenture-GeneracionHumana-CROSS-ReferenceImpl-e5f6a7b8-RestoDeVidaUtil
"""

import json
import xml.etree.ElementTree as ET
from typing import Dict, Any, Union
from pathlib import Path


class MFFCanonicalizer:
    """
    UTDC-GPS-MFF Canonicalizer
    
    Provides standardized canonicalization for different file formats
    following UTDC-GPS-MFF specification.
    """
    
    @staticmethod
    def canonicalize_json(data: Union[Dict, str], indent: int = 2) -> str:
        """
        Canonicalize JSON data according to MFF rules:
        - UTF-8 encoding without BOM
        - LF line endings
        - Keys sorted alphabetically  
        - 2-space indentation
        - No trailing comma
        """
        if isinstance(data, str):
            data = json.loads(data)
        
        return json.dumps(
            data,
            ensure_ascii=False,
            indent=indent,
            separators=(',', ': '),
            sort_keys=True
        ).replace('\r\n', '\n').replace('\r', '\n')
    
    @staticmethod
    def canonicalize_xml(xml_content: str) -> str:
        """
        Canonicalize XML content according to MFF rules:
        - UTF-8 encoding without BOM
        - LF line endings
        - Attributes sorted alphabetically
        - 2-space indentation
        - No empty attributes
        """
        try:
            # Parse XML
            root = ET.fromstring(xml_content)
            
            # Sort attributes recursively
            def sort_attributes(elem):
                if elem.attrib:
                    # Sort attributes by key
                    sorted_attribs = sorted(elem.attrib.items())
                    elem.clear()
                    for key, value in sorted_attribs:
                        if value:  # Skip empty attributes
                            elem.set(key, value)
                
                for child in elem:
                    sort_attributes(child)
            
            sort_attributes(root)
            
            # Generate canonical XML
            ET.indent(root, space="  ")
            xml_str = ET.tostring(root, encoding='unicode', xml_declaration=True)
            
            # Ensure proper line endings
            return xml_str.replace('\r\n', '\n').replace('\r', '\n')
            
        except ET.ParseError as e:
            raise ValueError(f"Invalid XML content: {e}")
    
    @staticmethod
    def canonicalize_svg(svg_content: str) -> str:
        """
        Canonicalize SVG content with special handling for metadata
        """
        # SVG is XML, so use XML canonicalization
        return MFFCanonicalizer.canonicalize_xml(svg_content)
    
    @staticmethod
    def canonicalize_file(file_path: Path) -> str:
        """
        Canonicalize file content based on file extension
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        ext = file_path.suffix.lower()
        
        if ext == '.json':
            return MFFCanonicalizer.canonicalize_json(content)
        elif ext in ['.xml', '.svg']:
            return MFFCanonicalizer.canonicalize_xml(content)
        else:
            # For other file types, just normalize line endings
            return content.replace('\r\n', '\n').replace('\r', '\n')
    
    @staticmethod
    def get_canonicalization_rules(file_format: str) -> str:
        """
        Get canonicalization rules string for specific format
        """
        rules_map = {
            'json': 'utf8;lf;keys_sorted=asc;indent=2;no_trailing_comma',
            'xml': 'utf8;lf;attr_order=asc;indent=2;no_empty_attrs',
            'svg': 'utf8;lf;attr_order=asc;indent=2;no_empty_attrs',
            'binary': 'binary;no_canonicalization'
        }
        
        return rules_map.get(file_format.lower(), 'utf8;lf;default')
    
    @staticmethod
    def validate_canonical_form(content: str, expected_rules: str) -> bool:
        """
        Validate that content follows canonicalization rules
        """
        # Basic validation checks
        if 'utf8' in expected_rules:
            try:
                content.encode('utf-8')
            except UnicodeEncodeError:
                return False
        
        if 'lf' in expected_rules:
            if '\r' in content:
                return False
        
        if 'keys_sorted' in expected_rules:
            try:
                data = json.loads(content)
                canonical = MFFCanonicalizer.canonicalize_json(data)
                return content == canonical
            except json.JSONDecodeError:
                pass
        
        return True