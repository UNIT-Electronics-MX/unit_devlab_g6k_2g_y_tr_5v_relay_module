# Documentation Templates

Este directorio contiene templates y scripts para generar la documentación web automáticamente.

## 📁 Archivos Template

### `index_template.html`
- **Propósito**: Template base para generar `docs/index.html`
- **Características**: 
  - Portal de documentación interactivo
  - Diseño responsivo y moderno
  - Integración automática con GitHub API
  - Enlaces dinámicos a recursos del repositorio

### `generate_index.py`
- **Propósito**: Script para regenerar `index.html` desde el template
- **Uso**: `python generate_index.py`
- **Funcionalidades**:
  - Detecta automáticamente el nombre del repositorio
  - Busca archivos de esquemático en `hardware/`
  - Configura enlaces apropiados
  - Genera el archivo final en `docs/index.html`

## 🔄 Uso Manual

Si el `docs/index.html` se borra accidentalmente, puedes regenerarlo:

```bash
cd software/documentation/
python generate_index.py
```

## 🤖 Integración con CI/CD

El workflow de GitHub Actions (`product_brief.yml`) incluye automáticamente:

1. ✅ Generación del `index.html` desde el template
2. ✅ Configuración automática con archivos del repositorio
3. ✅ Actualización de timestamps
4. ✅ Publicación en GitHub Pages

## 📝 Personalización

### Variables del Template

- `{{REPO_NAME}}`: Reemplazado automáticamente con el nombre del repositorio
- Las configuraciones de archivos se actualizan dinámicamente

### Estilos y Funcionalidad

- **CSS**: Diseño moderno con gradientes y efectos glassmorphism
- **JavaScript**: Integración con GitHub API para cargar recursos dinámicamente
- **Responsive**: Optimizado para móviles y escritorio

## 🛠️ Mantenimiento

### Para agregar nuevos tipos de archivo:

1. Edita `FILE_PATTERNS` en `index_template.html`
2. Actualiza `find_schematic_files()` en `generate_index.py` si es necesario
3. Regenera con `python generate_index.py`

### Para cambiar el diseño:

1. Modifica el CSS en `index_template.html`
2. Regenera el index.html
3. Prueba localmente antes de hacer commit

## 🚨 Recuperación de Emergencia

Si se pierde todo el contenido de `docs/`:

```bash
# 1. Regenerar documentación
cd software/documentation/
python generate_pdf.py
python generate_index.py

# 2. Copiar archivos necesarios
cp build/*.pdf ../../docs/
cp hardware/**/*sch*.pdf ../../docs/ 2>/dev/null || true

# 3. Verificar
ls -la ../../docs/
```

## 📋 Checklist de Verificación

- [ ] `index_template.html` existe y está actualizado
- [ ] `generate_index.py` puede ejecutarse sin errores
- [ ] El `index.html` generado abre correctamente en navegador
- [ ] Los enlaces funcionan correctamente
- [ ] El diseño se ve bien en móvil y escritorio

---

*Templates mantenidos por UNIT Electronics*
