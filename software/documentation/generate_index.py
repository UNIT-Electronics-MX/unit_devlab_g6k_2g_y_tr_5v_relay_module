#!/usr/bin/env python3
"""
Generador de index.html desde template
Este script regenera el index.html para la documentación web usando el template.
"""

import os
import re
import glob
import json
from datetime import datetime

def get_repo_name_from_git():
    """Obtiene el nombre del repositorio desde Git"""
    try:
        import subprocess
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            url = result.stdout.strip()
            # Extraer nombre del repo de URLs como:
            # https://github.com/UNIT-Electronics-MX/unit_relay_module_g6k_2g_y_tr_dc5
            # git@github.com:UNIT-Electronics-MX/unit_relay_module_g6k_2g_y_tr_dc5.git
            match = re.search(r'[:/]([^/]+)\.git$', url)
            if match:
                return match.group(1)
            match = re.search(r'[:/]([^/]+)$', url)
            if match:
                return match.group(1)
    except:
        pass
    
    # Fallback: usar nombre del directorio actual
    return os.path.basename(os.getcwd())

def find_schematic_files():
    """Busca archivos de esquemático en hardware/"""
    schematic_files = []
    patterns = ['**/hardware/**/*sch*.pdf', '**/hardware/**/*schematic*.pdf']
    
    for pattern in patterns:
        files = glob.glob(pattern, recursive=True)
        for file in files:
            filename = os.path.basename(file)
            if filename not in [f['filename'] for f in schematic_files]:
                schematic_files.append({
                    'name': 'Schematic PDF',
                    'filename': filename,
                    'url': filename,  # Asumiendo que estará en docs/
                    'type': 'schematics',
                    'icon': '⚡'
                })
    
    return schematic_files

def generate_index_html(template_path='index_template.html', output_path='../../docs/index.html'):
    """Genera index.html desde el template"""
    
    # Verificar que el template existe
    if not os.path.exists(template_path):
        print(f"❌ Template no encontrado: {template_path}")
        return False
    
    # Obtener información del repositorio
    repo_name = get_repo_name_from_git()
    schematic_files = find_schematic_files()
    
    print(f"📁 Repositorio detectado: {repo_name}")
    print(f"⚡ Esquemáticos encontrados: {len(schematic_files)}")
    
    # Leer el template
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazar variables del template
    content = content.replace('{{REPO_NAME}}', repo_name)
    
    # Agregar archivos de esquemático conocidos al JavaScript
    if schematic_files:
        # Construir la configuración de archivos conocidos
        known_files_js = "[\n"
        known_files_js += "            {\n"
        known_files_js += "                name: 'Product Brief PDF',\n"
        known_files_js += f"                url: `{repo_name}_product_brief.pdf`,\n"
        known_files_js += "                type: 'documentation',\n"
        known_files_js += "                icon: '📋'\n"
        known_files_js += "            }"
        
        for file in schematic_files:
            known_files_js += ",\n"
            known_files_js += "            {\n"
            known_files_js += f"                name: '{file['name']}',\n"
            known_files_js += f"                url: '{file['filename']}',\n"
            known_files_js += f"                type: '{file['type']}',\n"
            known_files_js += f"                icon: '{file['icon']}'\n"
            known_files_js += "            }"
        
        known_files_js += "\n        ];"
        
        # Reemplazar en el template
        old_pattern = r'const KNOWN_FILES = \[[\s\S]*?\];'
        new_pattern = f'const KNOWN_FILES = {known_files_js}'
        content = re.sub(old_pattern, new_pattern, content)
    
    # Crear directorio de salida si no existe
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Escribir el archivo final
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ index.html generado: {output_path}")
    return True

def main():
    """Función principal"""
    print("🔄 Generando index.html desde template...")
    
    # Cambiar al directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    success = generate_index_html()
    
    if success:
        print("🎉 Generación completada exitosamente!")
    else:
        print("❌ Error en la generación")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
