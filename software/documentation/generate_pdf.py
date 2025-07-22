
import os
import re
import subprocess
import markdown2
import yaml
import shutil
import glob
from datetime import datetime
from zoneinfo import ZoneInfo


def markdown_table_to_latex(md_table):
    try:
        lines = [line.strip() for line in md_table.strip().splitlines() if '|' in line]
        header = lines[0].strip('|').split('|')
        rows = [line.strip('|').split('|') for line in lines[2:]]

        # Construir formato: 'c' para todas menos la última como 'X' (mejor distribución)
        col_formats = ["c"] * (len(header) - 1) + [">{\\RaggedRight\\arraybackslash}X"]

        latex = "\\rowcolors{2}{white}{rowalt}\n"
        latex += "\\begin{tabularx}{\\textwidth}{|" + "|".join(col_formats) + "|}\n\\hline\n"
        latex += "\\rowcolor{headergray}\n"
        latex += " & ".join(h.strip() for h in header) + r" \\" + "\n\\hline\n"

        for row in rows:
            row = [cell.strip() for cell in row]
            if len(row) != len(header):
                row += [''] * (len(header) - len(row))
            latex += " & ".join(row) + r" \\" + "\n"

        latex += "\\hline\n\\end{tabularx}\n"
        return latex

    except Exception as e:
        return f"\\textit{{Error parsing table: {str(e)}}}"


        
def markdown_links_to_latex_list(text):
    items = re.findall(r'- \[(.*?)\]\((.*?)\)', text)
    if not items:
        return ""  # <- evita entorno vacío
    return "\\begin{itemize}\n" + "\n".join([f"\\item \\href{{{url}}}{{{label}}}" for label, url in items]) + "\n\\end{itemize}"


def markdown_individual_links_to_latex(text):
    """Maneja enlaces individuales sin viñetas y también enlaces con viñetas"""
    # Primero buscar enlaces con viñetas
    bullet_items = re.findall(r'- \[(.*?)\]\((.*?)\)', text)
    
    # Si encontramos enlaces con viñetas, usamos esos
    if bullet_items:
        return "\\begin{itemize}\n" + "\n".join([f"\\item \\href{{{url}}}{{{label}}}" for label, url in bullet_items]) + "\n\\end{itemize}"
    
    # Si no hay enlaces con viñetas, buscar enlaces individuales
    individual_links = re.findall(r'\[(.*?)\]\((.*?)\)', text)
    if individual_links:
        return "\\begin{itemize}\n" + "\n".join([f"\\item \\href{{{url}}}{{{label}}}" for label, url in individual_links]) + "\n\\end{itemize}"
    
    return ""


def markdown_bullets_to_latex(text):
    lines = text.strip().splitlines()
    items = [
        line.strip()[2:].strip()
        for line in lines
        if line.strip().startswith('-') and len(line.strip()[2:].strip()) > 0
    ]
    if not items:
        return ""
    return "\\begin{itemize}\n" + "\n".join([f"\\item {item}" for item in items]) + "\n\\end{itemize}"


def fix_paragraphs(text):
    return text.replace('\n\n', '\n\n\\par\n\n')

def fix_linebreaks_for_lists(text):
    lines = text.splitlines()
    return "\n".join(line + r"\\ " if line.strip().startswith('-') else line for line in lines)

def extract_section(heading, content):
    pattern = rf'##+\s*{re.escape(heading)}\s+(.*?)(?=\n##|\Z)'
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""

def extract_links_section(heading, content):
    section = extract_section(heading, content)
    return markdown_individual_links_to_latex(section)


def extract_table(heading, content):
    pattern = rf'##+\s*{re.escape(heading)}\s*\n+((?:\|.*\n)+)'
    match = re.search(pattern, content, re.IGNORECASE)
    return markdown_table_to_latex(match.group(1)) if match else "No table."




def format_images_with_titles(content):
    pattern = r'##\s*(.*?)\s*\n\s*!\[.*?\]\((.*?)\)'
    matches = re.findall(pattern, content)
    code = ""
    for i, (title, path) in enumerate(matches):
        code += (
            "\\newpage\n"
            "\\vspace*{3em}\n"  # espacio antes del título
            f"\\section*{{{title}}}\n"
            "\\vspace{1em}\n"
            "\\begin{center}\n"
            f"\\includegraphics[width=0.75\\textwidth,keepaspectratio]{{{path}}}\n"
            "\\end{center}\n"
        )
    return code

def parse_readme_md(path):

        # Obtener fecha local en Ciudad de México
    cdmx_now = datetime.now(ZoneInfo("America/Mexico_City"))
    formatted_date = cdmx_now.strftime("%Y-%m-%d %H:%M")

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    frontmatter_match = re.match(r'^---(.*?)---', content, re.DOTALL)
    frontmatter = yaml.safe_load(frontmatter_match.group(1)) if frontmatter_match else {}
    content = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)

    # Copiar archivos basándose en la configuración YAML
    print("🔄 Procesando archivos configurados en YAML...")
    copied_files = copy_files_from_config(frontmatter)

    # Actualizar enlaces si se copiaron archivos
    if copied_files:
        print("🔄 Actualizando enlaces...")
        content = update_links_from_config(content, copied_files)


    image_matches = re.findall(r'!\[(.*?)\]\((.*?)\)', content)
    image_product = next((path for alt, path in image_matches if "product" in alt.lower()), "")
    image_paths = [path for _, path in image_matches]
    if not image_product and image_paths:
        image_product = image_paths[0]
        if not os.path.exists(image_product):
            print(f"⚠️ Advertencia: La imagen principal no fue encontrada en la ruta: {image_product}")


    pin_table_match = re.search(r'## Pin.*?Layout\n((?:\|.*\n)+)', content)
    pin_table = markdown_table_to_latex(pin_table_match.group(1)) if pin_table_match else "No table."

    downloads = re.findall(r'- \[(.*?)\]\((.*?)\)', content)
    downloads_latex = "\\n".join([f"\\item \\href{{{link}}}{{{text}}}" for text, link in downloads])

    date_used = frontmatter.get("modified", formatted_date)

    data = {
        "LOGO": frontmatter.get("logo", "images/logo_unit.png"),
        "TITLE": frontmatter.get("title", "Untitled"),
        "VERSION": frontmatter.get("version", "v1.0"),
        "DATE": formatted_date,

        "SUBTITLE": frontmatter.get("subtitle", "Product Brief"),
        "INTRODUCTION": fix_paragraphs(extract_section("Introduction", content)),

        "FUNCTIONAL": fix_linebreaks_for_lists(extract_section("Functional Description", content)),
        "ELECTRICAL": fix_linebreaks_for_lists(extract_section("Electrical Characteristics & Signal Overview", content)),
        "FEATURES": fix_linebreaks_for_lists(extract_section("Features", content)),
        "APPLICATIONS": fix_linebreaks_for_lists(extract_section("Applications", content)),

        "PIN_TABLE": extract_table("Pin & Connector Layout", content),
        "R11_TABLE": extract_table(" Current", content),
        "R10_TABLE": extract_table(" Current Limit", content),

        "USAGE": markdown_bullets_to_latex(extract_section("Usage", content)),
        "DOWNLOADS": extract_links_section("Downloads", content),
        "PURCHASE": extract_links_section("Purchase", content),
        "IMAGES": format_images_with_titles(content),

        "IMAGE_PRODUCT": image_product,
        "OUTPUT_NAME": frontmatter.get("output", "generated_product_brief"),
    }
    

    # Agregar tablas personalizadas después de definir 'data'
    custom_tables = {
        "INTERFACE_TABLE": "Interface Overview",
        "SUPPORTS_TABLE": "Supports",
        "AVR_TABLE": "Firmware Modes: AVR Programmer",
        "CMSIS_TABLE": "Firmware Modes: CMSIS-DAP Debugger",
        "CPLD_TABLE": "Firmware Modes: CPLD Programmer"
    }

    for key, title in custom_tables.items():
        data[key] = extract_table(title, content)

    return data


def render_latex(template_path, output_path, replacements):
    with open(template_path, 'r', encoding='utf-8') as f:
        tex = f.read()
    for key, value in replacements.items():
        tex = tex.replace(f'<<{key}>>', value)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(tex)

        
def compile_pdf(tex_file):
    try:
        for _ in range(2):
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', '-output-directory=build', tex_file],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'  # <- esta línea soluciona el problema
            )
            if result.returncode != 0:
                print("⚠️ LaTeX compiló con errores:")
                print(result.stdout)
                print(result.stderr)
                if not os.path.exists("build/" + os.path.splitext(os.path.basename(tex_file))[0] + ".pdf"):
                    raise subprocess.CalledProcessError(result.returncode, result.args)
    except subprocess.CalledProcessError as e:
        print(f"❌ LaTeX falló con código {e.returncode}")
        raise


def clean_aux_files(output_name):
    base = os.path.splitext(output_name)[0]
    exts = [".aux", ".log", ".out", ".toc"]
    for ext in exts:
        path = f"{base}{ext}"
        if os.path.exists(path):
            os.remove(path)


def copy_files_from_config(frontmatter):
    """
    Copia archivos basándose en la configuración en el frontmatter YAML
    """
    copy_files = frontmatter.get("copy_files", [])
    if not copy_files:
        print("ℹ️ No hay archivos configurados para copiar en el YAML")
        return []
    
    copied_files = []
    for file_config in copy_files:
        source = file_config.get("source")
        destination = file_config.get("destination")
        link_name = file_config.get("link_name")
        
        if not all([source, destination, link_name]):
            print(f"⚠️ Configuración incompleta para archivo: {file_config}")
            continue
            
        # Crear la carpeta de destino si no existe
        os.makedirs(destination, exist_ok=True)
        
        # Nombre del archivo de destino
        filename = os.path.basename(source)
        dest_path = os.path.join(destination, filename)
        
        try:
            shutil.copy2(source, dest_path)
            print(f"✅ Archivo copiado: {filename} -> {destination}")
            copied_files.append({
                'filename': filename,
                'link_name': link_name,
                'source': source,
                'destination': dest_path
            })
        except Exception as e:
            print(f"⚠️ Error copiando {source}: {e}")
    
    return copied_files


def update_links_from_config(content, copied_files):
    """
    Actualiza los enlaces en el contenido basándose en los archivos copiados
    """
    updated_content = content
    
    for file_info in copied_files:
        link_name = file_info['link_name']
        
        # Buscar cualquier enlace que apunte a este archivo y actualizarlo
        # Patrón para enlaces con diferentes rutas posibles
        patterns = [
            rf'\[([^\]]*)\]\(\.\./\.\./hardware/{re.escape(link_name)}\)',
            rf'\[([^\]]*)\]\(hardware/{re.escape(link_name)}\)',
            rf'\[([^\]]*)\]\(docs/{re.escape(link_name)}\)',
            rf'\[([^\]]*)\]\([^)]*{re.escape(link_name)}\)'
        ]
        
        for pattern in patterns:
            replacement = rf'[\1]({link_name})'
            updated_content = re.sub(pattern, replacement, updated_content)
    
    return updated_content


def adjust_links_for_final_location(content, copied_files):
    """
    Ajusta los enlaces para que funcionen desde la ubicación final del PDF en docs/
    Ambos archivos (PDF y esquemático) estarán en la misma carpeta docs/
    """
    updated_content = content
    
    for filename in copied_files:
        # Cambiar enlaces de docs/filename a solo filename (misma carpeta)
        docs_pattern = rf'(\[([^\]]*)\])\(docs/{re.escape(filename)}\)'
        same_folder_replacement = rf'\1({filename})'
        updated_content = re.sub(docs_pattern, same_folder_replacement, updated_content)
    
    return updated_content

if __name__ == "__main__":
    data = parse_readme_md("README.md")  # asegúrate de definir 'data' aquí
    output_name = data["OUTPUT_NAME"]    # luego la usas aquí

    output_tex = f"build/{output_name}.tex"
    os.makedirs("build", exist_ok=True)

    render_latex("product_brief_template.tex", output_tex, data)
    compile_pdf(output_tex)
    clean_aux_files(f"build/{output_name}")
    
    print(f"🎉 PDF generado exitosamente: build/{output_name}.pdf")
    print(f"📄 El workflow de GitHub Actions copiará los archivos necesarios a docs/")