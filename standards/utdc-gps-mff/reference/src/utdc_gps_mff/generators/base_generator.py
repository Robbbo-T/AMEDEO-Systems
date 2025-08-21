"""
UTDC-GPS-MFF Base Generator Implementation
UTCS-MI: EstándarUniversal:Codigo-Desarrollo-UTDC-01.04-BaseGenerator-0001-v1.0-AerospaceAndQuantumUnitedAdvancedVenture-GeneracionHumana-CROSS-ReferenceImpl-f6a7b8c9-RestoDeVidaUtil
"""

import uuid
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone

from ..core.header import MFFHeader
from ..core.canonicalizer import MFFCanonicalizer
from ..core.signer import MFFSigner


class MFFGenerator:
    """
    UTDC-GPS-MFF Base Generator
    
    Provides comprehensive artifact generation with MFF compliance,
    including header generation, template processing, and validation.
    """
    
    def __init__(self, template_dir: Optional[Path] = None):
        """Initialize generator with template directory"""
        # Default template directory relative to this file
        default_templates = Path(__file__).parents[3] / "templates"
        self.template_dir = template_dir or default_templates
        self.canonicalizer = MFFCanonicalizer()
        self.signer = MFFSigner()
        
    def generate_utcmi_id(
        self, 
        artifact_type: str,
        phase: str = "Desarrollo",
        regulation: str = "UTDC",
        section: str = "00.00",
        category: str = "StandardArtifact",
        sequence: int = 1,
        version: str = "v1.0",
        program: str = "AerospaceAndQuantumUnitedAdvancedVenture",
        method: str = "GeneracionHibrida",
        domain: str = "CROSS",
        author: str = "ReferenceImpl",
        validity: str = "RestoDeVidaUtil"
    ) -> str:
        """Generate UTCS-MI compliant identifier"""
        
        # Generate hash8 from content
        content = f"{artifact_type}-{category}-{sequence}"
        hash8 = str(hash(content) % 100000000).zfill(8)[:8]
        
        parts = [
            artifact_type,      # ClaseArtefacto
            phase,              # FaseOrigen  
            regulation,         # Regulacion
            section,            # CapituloSeccion
            category,           # CategoriaDescriptiva
            f"{sequence:04d}",  # Secuencia
            version,            # Version
            program,            # ProgramaPortfolio
            method,             # MetodoGeneracion
            domain,             # DominioAplicacion
            author,             # IdentificadorFisico
            hash8,              # Hash8
            validity            # PeriodoValidez
        ]
        
        return f"EstándarUniversal:{'-'.join(parts)}"
    
    def create_header(
        self,
        artifact_type: str,
        regulation: str,
        content_data: Dict[str, Any],
        **kwargs
    ) -> MFFHeader:
        """Create MFF header for artifact"""
        
        # Filter kwargs for generate_utcmi_id
        utcmi_kwargs = {}
        for key in ["phase", "section", "sequence", "version", "program", "method", "domain", "author", "validity"]:
            if key in kwargs:
                utcmi_kwargs[key] = kwargs[key]
        
        # Generate UTCS-MI ID
        utcmi_id = self.generate_utcmi_id(
            artifact_type=artifact_type,
            regulation=regulation,
            category=content_data.get("category", "StandardArtifact"),
            **utcmi_kwargs
        )
        
        # Create header
        header = MFFHeader(utcmi_id)
        
        # Set generation metadata
        header.set_generation(
            method=kwargs.get("method", "GeneracionHibrida"),
            model=kwargs.get("model", "UTDC-MFF-Generator"),
            prompt=str(content_data),
            **content_data.get("parameters", {})
        )
        
        # Set timestamps
        header.set_timestamps()
        
        # Set security
        header.set_security(
            classification=kwargs.get("classification", "CUI")
        )
        
        # Set regulation reference
        header.regulation_reference = [regulation]
        if "additional_regulations" in kwargs:
            header.regulation_reference.extend(kwargs["additional_regulations"])
        
        # Set internationalization
        if "language" in kwargs:
            header.i18n = {"lang": kwargs["language"]}
        
        return header
    
    def generate_artifact(
        self,
        template_name: str,
        content_data: Dict[str, Any],
        output_dir: Path,
        regulation: str = "UTDC",
        **kwargs
    ) -> tuple[Path, Path]:
        """
        Generate complete MFF artifact with header
        
        Returns:
            Tuple of (artifact_path, header_path)
        """
        
        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load template
        template_path = self.template_dir / f"{template_name}.j2"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        # Read template
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Process template (simple string replacement for now)
        content = self._process_template(template_content, content_data)
        
        # Determine file extension from template name
        ext = template_name.split('.')[-2] if '.' in template_name else 'txt'
        
        # Create artifact file
        artifact_path = output_dir / f"mff_artifact.{ext}"
        
        # Canonicalize content
        canonical_content = self._canonicalize_by_type(content, ext)
        
        # Write artifact
        with open(artifact_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(canonical_content)
        
        # Create header
        header = self.create_header(
            artifact_type="Documento",
            regulation=regulation,
            content_data=content_data,
            **kwargs
        )
        
        # Set artifact metadata
        header.set_artifact(artifact_path, regulation, "1.0")
        
        # Set template reference
        from ..core.header import TemplateReference
        header.template_ref = TemplateReference(
            uri=str(template_path),
            version="v1.0"
        )
        
        # Set repo path
        header.repo_path = str(output_dir.relative_to(Path.cwd()) if output_dir.is_relative_to(Path.cwd()) else output_dir)
        
        # Set compliance (basic)
        header.set_compliance([
            {"name": "mff-validator", "rule": "UTDC-GPS-MFF-v1.0"}
        ], "pending")
        
        # Sign header
        self.signer.sign_header(header)
        
        # Save header
        header_path = output_dir / "mff_artifact.mff.json"
        header.save(header_path)
        
        return artifact_path, header_path
    
    def _process_template(self, template_content: str, data: Dict[str, Any]) -> str:
        """Process template with data (simple implementation)"""
        result = template_content
        
        # Replace common placeholders
        placeholders = {
            "${TITLE}": data.get("title", "Untitled"),
            "${AUTHOR}": data.get("author", "AMEDEO Systems"),
            "${DATE_UTC}": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "${VERSION}": data.get("version", "1.0"),
            "${CONTENT}": data.get("content", ""),
            "${DESCRIPTION}": data.get("description", ""),
            "${REGULATION}": data.get("regulation", "UTDC"),
        }
        
        for placeholder, value in placeholders.items():
            result = result.replace(placeholder, str(value))
        
        return result
    
    def _canonicalize_by_type(self, content: str, file_type: str) -> str:
        """Canonicalize content based on file type"""
        if file_type == 'json':
            return self.canonicalizer.canonicalize_json(content)
        elif file_type in ['xml', 'svg']:
            return self.canonicalizer.canonicalize_xml(content)
        else:
            # Default: normalize line endings
            return content.replace('\r\n', '\n').replace('\r', '\n')
    
    def generate_example_artifacts(self, output_dir: Path) -> List[tuple[Path, Path]]:
        """Generate example artifacts for testing"""
        examples = []
        
        # Basic XML example
        xml_data = {
            "title": "UTDC-GPS-MFF Example XML",
            "category": "ExampleDocument",
            "description": "Basic XML example following S1000D patterns"
        }
        
        try:
            artifact_path, header_path = self.generate_artifact(
                "s1000d/basic_document",
                xml_data,
                output_dir / "001-basic-xml",
                regulation="S1000D"
            )
            examples.append((artifact_path, header_path))
        except FileNotFoundError:
            # Template doesn't exist yet, skip
            pass
        
        return examples