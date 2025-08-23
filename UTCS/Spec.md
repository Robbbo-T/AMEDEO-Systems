## **Especificación UTCS-MI v5.0 

### **Campos del Estándar Universal**

| Campo | Descripción Correcta | Ejemplo |
|-------|---------------------|---------|
| **Clase** | Tipo de artefacto | `Documento`, `Configuracion`, `Especificacion` |
| **Fase** | Fase de Origen | `Desarrollo`, `Integracion`, `Operacion` |
| **Reg** | Regulación de Referencia | `DO178C`, `S1000D`, `CS25`, `ISO9001` |
| **Cap** | Capítulo-Sección del marco | `00.00`, `12.34` |
| **Categoria** | Clasificación (sin acrónimos) | `EspecificacionTecnica`, `ManualOperativo` |
| **Seq** | Secuencia | `0001` - `9999` |
| **Ver** | Versión | `v1.0`, `v2.3` |
| **Programa** | Programa del Portfolio (completo) | `AerospaceQuantumUnitedAdvancedVenture` |
| **Metodo** | Método de generación | `GeneracionHumana`, `GeneracionHibrida`, `GeneracionAuto` |
| **Dom** | Dominio operacional | `AIR`, `SPACE`, `DEFENSE`, `GROUND`, `CROSS` |
| **Ident** | Identificador Físico (autor) | `AmedeoPelliccia`, `JuanPerez` |
| **Hash** | Hash único 8 hex | `7f3c9a2b` |
| **Periodo** | Periodo de Validez | `RestoDeVidaUtil`, `Desarrollo,Integracion` |

### **JSON Schema para validación**

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "UTCS-MI v5.0 WAPI Schema",
  "type": "object",
  "required": ["Clase", "Fase", "Reg", "Cap", "Categoria", "Seq", "Ver", "Programa", "Metodo", "Dom", "Ident", "Hash", "Periodo"],
  "properties": {
    "Clase": {
      "type": "string",
      "pattern": "^\\p{Lu}\\p{L}+$",
      "description": "Tipo de artefacto"
    },
    "Fase": {
      "type": "string",
      "enum": ["Desarrollo", "Implementacion", "Integracion", "Verificacion", "Validacion", "Operacion", "Mantenimiento"],
      "description": "Fase de origen del artefacto"
    },
    "Reg": {
      "type": "string",
      "pattern": "^[A-Z0-9]+$",
      "examples": ["DO178C", "S1000D", "CS25", "ISO9001"],
      "description": "Regulación de referencia"
    },
    "Cap": {
      "type": "string",
      "pattern": "^\\d{2}\\.\\d{2}$",
      "description": "Capítulo-Sección del marco regulatorio"
    },
    "Categoria": {
      "type": "string",
      "pattern": "^\\p{Lu}\\p{L}+(\\p{Lu}\\p{L}+)*$",
      "not": {
        "pattern": "^[A-Z]{2,}$"
      },
      "description": "Clasificación sin acrónimos"
    },
    "Seq": {
      "type": "string",
      "pattern": "^\\d{4}$",
      "description": "Número de secuencia"
    },
    "Ver": {
      "type": "string",
      "pattern": "^v\\d+\\.\\d+$",
      "description": "Versión del artefacto"
    },
    "Programa": {
      "type": "string",
      "pattern": "^\\p{Lu}\\p{L}+(\\p{Lu}\\p{L}+)*$",
      "not": {
        "pattern": "^[A-Z]{2,}$"
      },
      "minLength": 10,
      "description": "Programa del portfolio (nombre completo, sin siglas)"
    },
    "Metodo": {
      "type": "string",
      "enum": ["GeneracionHumana", "GeneracionHibrida", "GeneracionAuto"],
      "description": "Método de generación"
    },
    "Dom": {
      "type": "string",
      "enum": ["AIR", "SPACE", "DEFENSE", "GROUND", "CROSS"],
      "description": "Dominio operacional"
    },
    "Ident": {
      "type": "string",
      "pattern": "^\\p{Lu}\\p{L}+(\\p{Lu}\\p{L}+)*$",
      "description": "Identificador físico (autor/contribuyente)"
    },
    "Hash": {
      "type": "string",
      "pattern": "^[0-9a-f]{8}$",
      "description": "Hash único de 8 caracteres hexadecimales"
    },
    "Periodo": {
      "type": "string",
      "pattern": "^(RestoDeVidaUtil|[A-Za-z]+(,[A-Za-z]+)*)$",
      "description": "Periodo de validez (fases o RestoDeVidaUtil)"
    }
  },
  "additionalProperties": false
}
```

### **Middleware Express con validaciones**

```javascript
const express = require('express');
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const app = express();
const ajv = new Ajv({ allErrors: true });
addFormats(ajv);

// Regex para parsear la URL UTCS-MI
const UTCS_REGEX = /^\/EstándarUniversal:(?<Clase>[^-]+)-(?<Fase>[^-]+)-(?<Reg>[A-Z0-9]+)-(?<Cap>\d{2}\.\d{2})-(?<Categoria>[^-]+)-(?<Seq>\d{4})-(?<Ver>v\d+\.\d+)-(?<Programa>[^-]+)-(?<Metodo>GeneracionHumana|GeneracionHibrida|GeneracionAuto)-(?<Dom>AIR|SPACE|DEFENSE|GROUND|CROSS)-(?<Ident>[^-]+)-(?<Hash>[0-9a-f]{8})-(?<Periodo>[^.]+)\.(?<ext>md|ya?ml|json|pdf)$/;

// Validaciones semánticas adicionales
const validacionesSemanticas = {
  // Regla cuántica
  reglaCuantica: (params) => {
    if (params.Categoria === 'CodigoCuantico') {
      if (!['Implementacion', 'Integracion'].includes(params.Fase)) {
        return 'CodigoCuantico solo permitido en fases Implementacion o Integracion';
      }
      if (params.Metodo === 'GeneracionHumana') {
        return 'CodigoCuantico no puede usar GeneracionHumana';
      }
    }
    return null;
  },
  
  // Validar que no hay acrónimos en Programa y Categoria
  noAcronimos: (params) => {
    const tieneAcronimo = (str) => /\b[A-Z]{2,}\b/.test(str);
    
    if (tieneAcronimo(params.Programa)) {
      return `Programa contiene acrónimos prohibidos: ${params.Programa}`;
    }
    if (tieneAcronimo(params.Categoria)) {
      return `Categoria contiene acrónimos prohibidos: ${params.Categoria}`;
    }
    return null;
  },
  
  // Validar coherencia Fase-Periodo
  validarPeriodo: (params) => {
    if (params.Periodo !== 'RestoDeVidaUtil') {
      const fases = params.Periodo.split(',');
      const fasesValidas = ['Desarrollo', 'Implementacion', 'Integracion', 
                           'Verificacion', 'Validacion', 'Operacion', 'Mantenimiento'];
      
      for (const fase of fases) {
        if (!fasesValidas.includes(fase)) {
          return `Fase inválida en Periodo: ${fase}`;
        }
      }
    }
    return null;
  }
};

// Middleware UTCS-MI
app.use((req, res, next) => {
  const match = req.path.match(UTCS_REGEX);
  
  if (!match) {
    return next(); // No es una URL UTCS-MI
  }
  
  const params = match.groups;
  
  // Validaciones adicionales
  const errores = [];
  
  // 1. Validación de hash exactamente 8 caracteres hex
  if (params.Hash.length !== 8) {
    errores.push('Hash debe ser exactamente 8 caracteres hexadecimales');
  }
  
  // 2. Validación de versión comienza con 'v'
  if (!params.Ver.startsWith('v')) {
    errores.push('Version debe comenzar con "v"');
  }
  
  // 3. Validaciones semánticas
  for (const [nombre, validador] of Object.entries(validacionesSemanticas)) {
    const error = validador(params);
    if (error) {
      errores.push(error);
    }
  }
  
  if (errores.length > 0) {
    return res.status(400).json({
      error: 'Validación UTCS-MI falló',
      detalles: errores,
      parametros: params
    });
  }
  
  // Añadir headers para downstream processing
  Object.entries(params).forEach(([key, value]) => {
    req.headers[`x-utcs-${key.toLowerCase()}`] = value;
  });
  
  // Log para auditoría
  console.log(`UTCS-MI Request: ${params.Clase}/${params.Ver} por ${params.Ident}`);
  
  next();
});

// Handler para rutas UTCS-MI válidas
app.get('/EstándarUniversal:*', (req, res) => {
  const formato = req.headers['x-utcs-ext'];
  const contentTypes = {
    'json': 'application/json',
    'yaml': 'application/x-yaml',
    'yml': 'application/x-yaml',
    'md': 'text/markdown',
    'pdf': 'application/pdf'
  };
  
  res.type(contentTypes[formato] || 'application/octet-stream');
  
  // Tu lógica de negocio aquí
  res.json({
    mensaje: 'UTCS-MI v5.0 procesado correctamente',
    parametros: Object.fromEntries(
      Object.entries(req.headers)
        .filter(([key]) => key.startsWith('x-utcs-'))
        .map(([key, value]) => [key.replace('x-utcs-', ''), value])
    )
  });
});

// Error handler
app.use((err, req, res, next) => {
  res.status(500).json({
    error: 'Error interno',
    mensaje: err.message
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`UTCS-MI v5.0 WAPI listening on port ${PORT}`);
});
```

Este middleware Express:
1. ✅ Parsea URLs UTCS-MI v5.0
2. ✅ Valida formato exacto del hash (8 hex)
3. ✅ Verifica que Ver comience con 'v'
4. ✅ Aplica la regla cuántica
5. ✅ Detecta acrónimos prohibidos en Programa y Categoria
6. ✅ Valida coherencia del Periodo
7. ✅ Añade headers X-UTCS-* para procesamiento downstream
8. ✅ Retorna 400 con detalles específicos en violaciones

¿Necesitas ajustes adicionales o integración con otros componentes del sistema?
