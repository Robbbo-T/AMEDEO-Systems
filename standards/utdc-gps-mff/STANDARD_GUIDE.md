# UTDC-GPS-MFF STANDARD GUIDE v1.0
Universal Technical Data and Content Generative Prompting Standard - Machine Final Format

**Document ID:** EstándarUniversal:Especificacion-Desarrollo-UTDC-00.00-StandardGuide-0001-v1.0-AerospaceAndQuantumUnitedAdvancedVenture-GeneracionHumana-CROSS-AmedeoPelliccia-a1b2c3d4-RestoDeVidaUtil

**Effective Date:** 2025-08-21  
**Classification:** CUI (Controlled Unclassified Information)  
**License:** CC BY-SA 4.0

## 1. SCOPE AND PURPOSE

### 1.1 Scope

This standard defines the Machine Final Format (MFF) for the Universal Technical Data and Content Generative Prompting Standard (UTDC-GPS), establishing requirements for:

- Structured data headers (MFF-Header)
- Regulatory-compliant templates (MFF-Template)  
- Validation and canonicalization procedures
- Cryptographic integrity mechanisms
- Repository organization and naming conventions

### 1.2 Purpose

To ensure consistent, traceable, and regulatory-compliant generation of technical content across aerospace, defense, and quantum computing domains, enabling:

- Automated validation against regulatory schemas
- Complete provenance and traceability chains
- Cryptographic integrity assurance
- Multi-format regulatory compliance (S1000D, DO-178C, CS-25, etc.)

## 2. NORMATIVE REFERENCES

- UTCS-MI v5.0+: Universal Technical Content Standard - Machine Interface
- S1000D v5.0: International specification for technical publications
- DO-178C: Software Considerations in Airborne Systems
- CS-25: Certification Specifications for Large Aeroplanes
- ISO/IEC 14496-14: MP4 file format
- W3C SVG 1.1: Scalable Vector Graphics specification
- NIST PQC: Post-Quantum Cryptography standards

## 3. DEFINITIONS AND ACRONYMS

### 3.1 Definitions

- **MFF**: Machine Final Format - the complete structure comprising header and template
- **Sidecar**: Accompanying metadata file stored alongside the primary artifact
- **Canonicalization**: Process of converting data to a standard, normalized form
- **Provenance**: Complete chain of origin and modification history

### 3.2 Acronyms

- **UTDC-GPS**: Universal Technical Data and Content Generative Prompting Standard
- **UTCS-MI**: Universal Technical Content Standard - Machine Interface
- **PQC**: Post-Quantum Cryptography
- **DET**: Digital Evidence Twin
- **SBOM**: Software Bill of Materials

## 4. MFF-HEADER SPECIFICATION

### 4.1 Structure

The MFF-Header SHALL be a JSON document with the following mandatory fields:

```json
{
  "utcmi_id": "<UTCS-MI compliant identifier>",
  "repo_path": "<repository path>",
  "artifact": {
    "uri": "<artifact location>",
    "format": {
      "mime": "<MIME type>",
      "ext": "<file extension>"
    },
    "regulation_schema": {
      "name": "<schema name>",
      "version": "<schema version>"
    },
    "size_bytes": "<integer>",
    "sha256": "<hash>",
    "canonicalization": "<canonicalization rules>"
  },
  "regulation_reference": ["<regulation-1>", "<regulation-2>"],
  "template_ref": {
    "uri": "<template location>",
    "version": "<template version>"
  },
  "generation": {
    "method": "<GeneracionHumana|GeneracionHibrida|GeneracionAuto>",
    "model": "<model identifier>",
    "prompt_hash": "<8-character hash>",
    "parameters": {}
  },
  "provenance": [],
  "compliance": {
    "validators": [],
    "result": "<pending|passed|failed>"
  },
  "security": {
    "classification": "<classification level>",
    "integrity_signature": {}
  },
  "timestamps": {
    "created_utc": "<ISO 8601>",
    "generated_utc": "<ISO 8601>"
  },
  "license": "<license identifier>",
  "i18n": {
    "lang": "<BCP 47 language tag>"
  }
}
```

### 4.2 UTCS-MI Identifier Requirements

The `utcmi_id` field SHALL comply with UTCS-MI v5.0:

**Format:** `EstándarUniversal:<13 fields separated by hyphens>`

**Field Structure:**
1. ClaseArtefacto: {Especificacion|Plantilla|Documento|Codigo|Prueba|Build|Validacion}
2. FaseOrigen: {Desarrollo|Validacion|Certificacion|Operacion}
3. Regulacion: Applicable standard (e.g., S1000D, DO178C, CS25)
4. CapituloSeccion: XX.XX format
5. CategoriaDescriptiva: CamelCase, no acronyms
6. Secuencia: 4-digit zero-padded (0001-9999)
7. Version: vX.Y format
8. ProgramaPortfolio: Full name, no acronyms
9. MetodoGeneracion: {GeneracionHumana|GeneracionHibrida|GeneracionAuto}
10. DominioAplicacion: {AIR|SPACE|DEFENSE|GROUND|CROSS}
11. IdentificadorFisico: Author/System identifier
12. Hash8: 8-character hexadecimal
13. PeriodoValidez: {RestoDeVidaUtil|YYYY-MM-DD}

## 5. VALIDATION PIPELINE

### 5.1 Processing Steps

1. **Input Validation**: Verify prompt structure and parameters
2. **Template Selection**: Choose appropriate regulatory template
3. **Content Generation**: Populate template with validated data
4. **Canonicalization**: Apply format-specific rules
5. **Hash Calculation**: Generate SHA-256 of canonical form
6. **Header Generation**: Create MFF-Header with all metadata
7. **Regulatory Validation**: Validate against schema (XSD, etc.)
8. **UTCS-MI Validation**: Verify identifier compliance
9. **Signature Generation**: Apply PQC signature (Dilithium3/Ed25519)
10. **Storage**: Write artifacts to repository structure

### 5.2 Validation Criteria

- **UTCS-MI compliance**: 100% required
- **Schema validation**: MUST pass without errors
- **Hash verification**: MUST match calculated value
- **Signature verification**: MUST validate with public key

## 6. SECURITY REQUIREMENTS

### 6.1 Cryptographic Signatures

- **Algorithm**: Dilithium3 (PQC) or Ed25519 (transitional)
- **Scope**: Sign the SHA-256 hash of the canonical artifact
- **Storage**: In `integrity_signature` field of MFF-Header

### 6.2 Classification Levels

- **CUI**: Controlled Unclassified Information
- **PUBLIC**: No restrictions
- **CONFIDENTIAL**: Restricted access
- **SECRET**: Classified (special handling required)

## 7. REPOSITORY STRUCTURE

### 7.1 Directory Organization

```
/{repo_path}/
  ├── {hash8}/
  │   ├── {format}/
  │   │   ├── mff_artifact.{ext}      # Primary artifact
  │   │   ├── mff_artifact.mff.json   # MFF-Header sidecar
  │   │   └── mff_artifact.thumb.{svg|png}  # Optional thumbnail
  │   └── meta/
  │       └── provenance.json         # Extended provenance
  └── manifest.json                    # Directory manifest
```

### 7.2 Naming Conventions

- Primary artifact: `mff_artifact.{ext}`
- Sidecar header: `mff_artifact.mff.json`
- Thumbnail: `mff_artifact.thumb.{svg|png}`
- Maximum path length: 255 characters

## 8. CONFORMANCE

### 8.1 Conformance Levels

- **Level 1**: Structure compliance (valid JSON, required fields)
- **Level 2**: UTCS-MI compliance (valid identifier)
- **Level 3**: Regulatory compliance (schema validation)
- **Level 4**: Security compliance (signatures, classification)
- **Level 5**: Full compliance (all requirements met)

### 8.2 Certification

Implementations claiming UTDC-GPS-MFF compliance SHALL:

- Pass all validation criteria in Section 5.2
- Implement all mandatory fields from Section 4.1
- Follow canonicalization rules from reference implementation
- Maintain repository structure per Section 7
- Provide cryptographic signatures per Section 6

## APPENDIX A: CHANGE LOG

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| v1.0 | 2025-08-21 | Initial release | Amedeo Pelliccia |

## APPENDIX B: REFERENCE IMPLEMENTATION

Available at: `standards/utdc-gps-mff/reference/`

---

**END OF DOCUMENT**

**Signature:** EstándarUniversal:UTDC-GPS-MFF-v1.0:sha256:a1b2c3d4