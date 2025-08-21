# UTDC-GPS-MFF API Reference

## Core Classes

### MFFHeader

Main class for managing MFF headers with UTCS-MI compliance.

```python
from utdc_gps_mff import MFFHeader

# Create header
utcmi_id = "EstándarUniversal:Documento-Desarrollo-UTDC-00.00-Example-0001-v1.0-Program-GeneracionHumana-CROSS-Author-12345678-RestoDeVidaUtil"
header = MFFHeader(utcmi_id)

# Set artifact metadata
header.set_artifact(Path("document.xml"), "S1000D", "5.0")

# Set generation metadata
header.set_generation("GeneracionHumana", "Human-Author", "prompt text", temperature=0.7)

# Set security
header.set_security("CUI")

# Set timestamps
header.set_timestamps()

# Save to file
header.save(Path("header.mff.json"))
```

### MFFValidator

Comprehensive validation for MFF artifacts.

```python
from utdc_gps_mff import MFFValidator

validator = MFFValidator()

# Validate header file
result = validator.validate_file(Path("header.mff.json"))
print(f"Valid: {result.is_valid}")
print(f"Coverage: {result.coverage}%")

# Validate regulatory compliance
header = MFFHeader.from_file(Path("header.mff.json"))
reg_result = validator.validate_regulatory_compliance(header, "S1000D")
```

### MFFGenerator

Generate complete MFF artifacts from templates.

```python
from utdc_gps_mff import MFFGenerator

generator = MFFGenerator()

# Generate artifact
content_data = {
    "title": "Safety Assessment",
    "description": "Aircraft safety analysis document"
}

artifact_path, header_path = generator.generate_artifact(
    "s1000d/basic_document",
    content_data,
    Path("output/"),
    regulation="S1000D"
)
```

### MFFSigner

PQC cryptographic signing using AMEDEO SEAL infrastructure.

```python
from utdc_gps_mff import MFFSigner

signer = MFFSigner("Dilithium3")

# Sign header
signature = signer.sign_header(header)

# Verify signature
is_valid = signer.verify_signature(header)
```

### MFFCanonicalizer

Standardized canonicalization for different formats.

```python
from utdc_gps_mff import MFFCanonicalizer

# Canonicalize JSON
canonical = MFFCanonicalizer.canonicalize_json(data)

# Canonicalize XML
canonical = MFFCanonicalizer.canonicalize_xml(xml_content)

# Get canonicalization rules
rules = MFFCanonicalizer.get_canonicalization_rules("json")
```

## Command Line Tools

### validate.py

```bash
python tools/validate.py header1.mff.json header2.mff.json --regulation S1000D --cascade --verbose
```

### generate.py

```bash
python tools/generate.py s1000d/basic_document --output examples/001 --title "Test Doc" --regulation S1000D
```

## Templates

Templates use simple `${VARIABLE}` substitution:

- `${TITLE}`: Document title
- `${DESCRIPTION}`: Document description  
- `${AUTHOR}`: Document author
- `${DATE_UTC}`: Generation timestamp
- `${VERSION}`: Document version

Available templates:
- `s1000d/basic_document`: S1000D XML document
- `svg/technical_diagram`: SVG technical diagram

## Error Handling

All validation methods return `ValidationResult` objects:

```python
class ValidationResult:
    is_valid: bool
    errors: List[str] 
    warnings: List[str]
    coverage: float
```

## Integration with AMEDEO Systems

The UTDC-GPS-MFF implementation integrates with existing AMEDEO infrastructure:

- **SEAL**: PQC signing using existing agents/base_agent.py
- **UTCS-MI**: Full compliance with v5.0+ standard
- **DET**: Evidence trails through provenance chains
- **Validation**: Compatible with existing validation pipeline