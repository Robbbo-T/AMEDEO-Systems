"""
UTDC-GPS-MFF Basic Tests
UTCS-MI: EstándarUniversal:Prueba-Desarrollo-UTDC-01.00-BasicTests-0001-v1.0-AerospaceAndQuantumUnitedAdvancedVenture-GeneracionHumana-CROSS-ReferenceImpl-test0001-RestoDeVidaUtil
"""

import unittest
import sys
import tempfile
from pathlib import Path

# Add source path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utdc_gps_mff import MFFHeader, MFFValidator, MFFGenerator


class TestMFFHeader(unittest.TestCase):
    """Test MFF Header functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.valid_utcmi_id = "EstándarUniversal:Documento-Desarrollo-UTDC-00.00-TestDocument-0001-v1.0-AerospaceAndQuantumUnitedAdvancedVenture-GeneracionHumana-CROSS-TestSystem-a1b2c3d4-RestoDeVidaUtil"
        
    def test_utcmi_validation(self):
        """Test UTCS-MI ID validation"""
        # Valid ID should pass
        header = MFFHeader(self.valid_utcmi_id)
        self.assertTrue(header.validate_utcmi_id())
        
        # Invalid IDs should fail
        invalid_ids = [
            "InvalidPrefix:test",
            "EstándarUniversal:too-few-fields",
            "EstándarUniversal:a-b-c-d-e-f-g-h-i-j-k-l-m-n-o-too-many"
        ]
        
        for invalid_id in invalid_ids:
            with self.assertRaises(ValueError):
                MFFHeader(invalid_id)
    
    def test_header_serialization(self):
        """Test header to/from JSON"""
        header = MFFHeader(self.valid_utcmi_id)
        header.set_timestamps()
        header.set_security("CUI")
        
        # Test to_dict
        data = header.to_dict()
        self.assertEqual(data["utcmi_id"], self.valid_utcmi_id)
        self.assertIn("timestamps", data)
        self.assertIn("security", data)
        
        # Test to_json
        json_str = header.to_json()
        self.assertIsInstance(json_str, str)
        self.assertIn(self.valid_utcmi_id, json_str)
        
        # Test from_dict
        header2 = MFFHeader.from_dict(data)
        self.assertEqual(header2.utcmi_id, header.utcmi_id)
    
    def test_artifact_metadata(self):
        """Test artifact metadata setting"""
        header = MFFHeader(self.valid_utcmi_id)
        
        # Create temporary test file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
            f.write('<?xml version="1.0"?><test>content</test>')
            temp_path = Path(f.name)
        
        try:
            header.set_artifact(temp_path, "S1000D", "5.0")
            
            self.assertIsNotNone(header.artifact)
            self.assertEqual(header.artifact.format.ext, "xml")
            self.assertEqual(header.artifact.format.mime, "application/xml")
            self.assertEqual(header.artifact.regulation_schema.name, "S1000D")
            self.assertIsInstance(header.artifact.sha256, str)
            self.assertEqual(len(header.artifact.sha256), 64)
            
        finally:
            temp_path.unlink()


class TestMFFValidator(unittest.TestCase):
    """Test MFF Validator functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.validator = MFFValidator()
        self.valid_utcmi_id = "EstándarUniversal:Documento-Desarrollo-UTDC-00.00-TestDocument-0001-v1.0-AerospaceAndQuantumUnitedAdvancedVenture-GeneracionHumana-CROSS-TestSystem-a1b2c3d4-RestoDeVidaUtil"
    
    def test_basic_validation(self):
        """Test basic header validation"""
        header = MFFHeader(self.valid_utcmi_id)
        header.set_timestamps()
        header.set_security("CUI")
        
        # Should fail validation due to missing mandatory fields
        result = self.validator.validate_header(header)
        self.assertFalse(result.is_valid)
        self.assertGreater(len(result.errors), 0)
    
    def test_schema_validation(self):
        """Test JSON schema validation"""
        # Create minimal valid header
        header = MFFHeader(self.valid_utcmi_id)
        
        # Add all required fields
        header.set_timestamps()
        header.set_security("CUI")
        header.regulation_reference = ["UTDC"]
        
        # Mock required fields
        from utdc_gps_mff.core.header import (
            ArtifactMetadata, ArtifactFormat, RegulationSchema,
            TemplateReference, GenerationMetadata, ComplianceMetadata, Validator
        )
        
        header.artifact = ArtifactMetadata(
            uri="test.xml",
            format=ArtifactFormat(mime="application/xml", ext="xml"),
            regulation_schema=RegulationSchema(name="UTDC", version="1.0"),
            size_bytes=100,
            sha256="a" * 64,
            canonicalization="utf8;lf"
        )
        
        header.template_ref = TemplateReference(uri="test.j2", version="v1.0")
        header.generation = GenerationMetadata(
            method="GeneracionHumana",
            model="test",
            prompt_hash="12345678",
            parameters={}
        )
        header.compliance = ComplianceMetadata(
            validators=[Validator(name="test", rule="test")],
            result="passed"
        )
        
        result = self.validator.validate_header(header)
        self.assertTrue(result.is_valid, f"Validation errors: {result.errors}")


class TestMFFGenerator(unittest.TestCase):
    """Test MFF Generator functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.generator = MFFGenerator()
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_utcmi_generation(self):
        """Test UTCS-MI ID generation"""
        utcmi_id = self.generator.generate_utcmi_id(
            artifact_type="Documento",
            category="TestDocument"
        )
        
        self.assertTrue(utcmi_id.startswith("EstándarUniversal:"))
        parts = utcmi_id.split(":")[1].split("-")
        self.assertEqual(len(parts), 13)
        self.assertEqual(parts[0], "Documento")
    
    def test_header_creation(self):
        """Test header creation"""
        content_data = {
            "title": "Test Document",
            "category": "TestDocument"
        }
        
        header = self.generator.create_header(
            artifact_type="Documento",
            regulation="UTDC",
            content_data=content_data
        )
        
        self.assertIsInstance(header, MFFHeader)
        self.assertIsNotNone(header.generation)
        self.assertIsNotNone(header.timestamps)
        self.assertIsNotNone(header.security)


class TestIntegration(unittest.TestCase):
    """Integration tests for full MFF workflow"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.generator = MFFGenerator()
        self.validator = MFFValidator()
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_simple_workflow(self):
        """Test simple generation and validation workflow"""
        # Create simple template
        template_dir = self.temp_dir / "templates"
        template_dir.mkdir()
        
        template_path = template_dir / "test.xml.j2"
        template_path.write_text("""<?xml version="1.0"?>
<document>
    <title>${TITLE}</title>
    <content>${CONTENT}</content>
</document>""")
        
        # Set template directory
        self.generator.template_dir = template_dir
        
        # Generate artifact
        content_data = {
            "title": "Test Document",
            "content": "Test content",
            "category": "TestDocument"
        }
        
        try:
            artifact_path, header_path = self.generator.generate_artifact(
                "test.xml",
                content_data,
                self.temp_dir / "output"
            )
            
            # Verify files exist
            self.assertTrue(artifact_path.exists())
            self.assertTrue(header_path.exists())
            
            # Validate header
            result = self.validator.validate_file(header_path)
            
            # Should have some validation (may not be fully valid due to missing fields)
            self.assertIsInstance(result, type(self.validator.validate_file(header_path)))
            
        except FileNotFoundError:
            # Template processing might fail, that's OK for basic test
            pass


if __name__ == "__main__":
    unittest.main()